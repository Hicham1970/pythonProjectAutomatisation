import logging
import os
import shutil
from dataclasses import dataclass
from os import scandir
from os.path import exists, isdir, join, splitext

# Known extensions (normalized to lowercase)
AUDIO_EXTENSIONS = {
    ".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"
}

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi",
    ".png", ".gif", ".webp", ".tiff", ".tif", ".psd",
    ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp",
    ".dib", ".heif", ".heic", ".ind", ".indd", ".indt",
    ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2",
    ".svg", ".svgz", ".ai", ".eps", ".ico"
}

VIDEO_EXTENSIONS = {
    ".mp4", ".m4v", ".mov", ".wmv", ".avi", ".mkv",
    ".flv", ".webm", ".ts", ".m2ts", ".3gp"
}

DOC_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt",
    ".csv", ".tsv", ".xls", ".xlsx", ".ppt", ".pptx",
    ".md", ".json", ".yaml", ".yml", ".xml"
}

TEN_MB = 10 * 1024 * 1024


@dataclass
class OrganizerConfig:
    source_dir: str
    dest_dir_music: str
    dest_dir_sfx: str
    dest_dir_video: str
    dest_dir_image: str
    dest_dir_documents: str
    sfx_size_threshold: int = TEN_MB
    dry_run: bool = False


def make_unique_name(dest: str, name: str) -> str:
    """
    Generate a unique file name in 'dest' by appending '(n)' before the extension
    if a collision exists. Preserves existing files without renaming them.
    """
    base, ext = splitext(name)
    candidate = name
    i = 1
    while exists(join(dest, candidate)):
        candidate = f"{base}({i}){ext}"
        i += 1
    return candidate


def safe_move_entry(entry: os.DirEntry, dest_dir: str, name: str, dry_run: bool = False) -> str:
    """
    Move the DirEntry to dest_dir using a unique name. Creates the dest_dir if needed.
    Returns the destination path (or the would-be path for dry-run).
    """
    os.makedirs(dest_dir, exist_ok=True)
    target_name = make_unique_name(dest_dir, name)
    src_path = entry.path
    dst_path = join(dest_dir, target_name)

    if dry_run:
        logging.info("[dry-run] Would move: %s -> %s", src_path, dst_path)
        return dst_path

    shutil.move(src_path, dst_path)
    return dst_path


def determine_destination(name_lower: str, ext_lower: str, size_bytes: int, cfg: OrganizerConfig) -> str | None:
    """
    Determine the destination directory for the given file details.
    Routes audio files smaller than threshold or containing 'sfx' in their name to SFX.
    """
    if ext_lower in AUDIO_EXTENSIONS:
        if size_bytes < cfg.sfx_size_threshold or "sfx" in name_lower:
            return cfg.dest_dir_sfx
        return cfg.dest_dir_music

    if ext_lower in VIDEO_EXTENSIONS:
        return cfg.dest_dir_video

    if ext_lower in IMAGE_EXTENSIONS:
        return cfg.dest_dir_image

    if ext_lower in DOC_EXTENSIONS:
        return cfg.dest_dir_documents

    return None


def organize(cfg: OrganizerConfig) -> None:
    """
    Scan the source directory and move supported files to their destinations.
    - Skips non-files and symlinks
    - Uses normalized lowercase extension checks
    - Preserves existing files by generating unique names
    - Wraps moves with error handling and logging
    """
    if not isdir(cfg.source_dir):
        raise NotADirectoryError(f"Source directory does not exist or is not a directory: {cfg.source_dir}")

    with scandir(cfg.source_dir) as entries:
        for entry in entries:
            try:
                # Filter: only regular files (no dirs, no symlinks)
                if not entry.is_file(follow_symlinks=False):
                    logging.debug("Skipping non-file: %s", entry.path)
                    continue

                name = entry.name
                name_lower = name.lower()
                ext_lower = splitext(name_lower)[1]

                if not ext_lower:
                    logging.debug("Skipping file with no extension: %s", name)
                    continue

                try:
                    st = entry.stat(follow_symlinks=False)
                except FileNotFoundError:
                    # The file may have been removed or moved during scanning
                    logging.warning("File disappeared during scan, skipping: %s", entry.path)
                    continue

                dest_dir = determine_destination(name_lower, ext_lower, st.st_size, cfg)
                if not dest_dir:
                    logging.debug("Skipping unsupported extension (%s): %s", ext_lower, name)
                    continue

                safe_move_entry(entry, dest_dir, name, cfg.dry_run)
                if cfg.dry_run:
                    logging.info("[dry-run] Would move file to %s: %s", dest_dir, name)
                else:
                    logging.info("Moved file to %s: %s", dest_dir, name)

            except Exception:
                # Keep processing other entries even if one fails
                logging.exception("Failed processing entry: %s", getattr(entry, "path", entry))
                continue


def setup_logging(level: str = "INFO") -> None:
    lvl = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s %(levelname)s %(message)s"
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Organize files by type and size safely.")
    parser.add_argument("--source", required=True, help="Source directory to scan")
    parser.add_argument("--music-dir", required=True, help="Destination for music files")
    parser.add_argument("--sfx-dir", required=True, help="Destination for SFX/short audio files")
    parser.add_argument("--video-dir", required=True, help="Destination for video files")
    parser.add_argument("--image-dir", required=True, help="Destination for image files")
    parser.add_argument("--docs-dir", required=True, help="Destination for document files")
    parser.add_argument("--sfx-size-mb", type=float, default=10.0, help="Size threshold in MB for routing audio to SFX")
    parser.add_argument("--dry-run", action="store_true", help="Do not move files; only log actions")
    parser.add_argument("--log-level", default="INFO", help="Logging level: DEBUG, INFO, WARNING, ERROR")

    args = parser.parse_args()
    setup_logging(args.log_level)

    cfg = OrganizerConfig(
        source_dir=args.source,
        dest_dir_music=args.music_dir,
        dest_dir_sfx=args.sfx_dir,
        dest_dir_video=args.video_dir,
        dest_dir_image=args.image_dir,
        dest_dir_documents=args.docs_dir,
        sfx_size_threshold=int(args.sfx_size_mb * 1024 * 1024),
        dry_run=args.dry_run,
    )

    organize(cfg)


if __name__ == "__main__":
    main()