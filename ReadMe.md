# Desktop Cleaner GUI 🗂️

A powerful, user-friendly graphical interface for automatically organizing and cleaning desktop files. Built with Python's tkinter, this application provides an intuitive way to sort files into categorized folders with real-time logging and progress tracking.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-tkinter-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### 📁 **Smart File Organization**
- **Automated Categorization**: Intelligently sorts files by type (Music, SFX, Videos, Images, Documents)
- **Size-based Classification**: Separates audio files by size (music vs sound effects)
- **Safe File Handling**: Preserves existing files with unique naming
- **Dry Run Mode**: Preview changes before actual file movement

### 🖥️ **Intuitive GUI Interface**
- **Modern Design**: Clean, responsive interface using ttk themed widgets
- **Directory Browser**: Easy point-and-click directory selection
- **Real-time Progress**: Visual progress bar and status updates
- **Configurable Settings**: Adjustable thresholds and logging levels

### 📊 **Advanced Logging System**
- **Live Log Display**: Real-time logging in scrollable text widget
- **Multiple Log Levels**: DEBUG, INFO, WARNING, ERROR support
- **Thread-safe Logging**: Custom TextHandler for GUI log integration
- **Persistent History**: Full operation history with timestamps

### ⚙️ **Flexible Configuration**
- **Custom Destinations**: Set specific folders for each file type
- **Size Thresholds**: Configurable audio file size limits
- **Default Presets**: Quick-load common directory structures
- **Validation**: Input validation with helpful error messages

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- `desktop_cleaner_bot` module

### Installation
1. Clone or download the application files
2. Ensure the `desktop_cleaner_bot.py` module is in the same directory
3. Run the application:
   ```bash
   python desktop_cleaner_gui.py

Copy

Insert

Basic Usage
Launch the application
Select directories using the Browse buttons or click "Load Defaults"
Configure settings (SFX threshold, log level, dry run mode)
Click "Organize Files" to start the process
Monitor progress in the real-time log display
📋 Detailed Features
Directory Configuration
Source DirectoryFolder to organizeUser's DesktopMusic DirectoryDestination for music filesDesktop/Organized/MusicSFX DirectoryDestination for sound effectsDesktop/Organized/SFXVideo DirectoryDestination for video filesDesktop/Organized/VideosImage DirectoryDestination for image filesDesktop/Organized/ImagesDocuments DirectoryDestination for documentsDesktop/Organized/Documents
Settings Panel
SFX Size Threshold: Audio files smaller than this size (MB) are classified as sound effects
Log Level: Controls verbosity of logging output (DEBUG/INFO/WARNING/ERROR)
Dry Run Mode: Preview mode that shows what would happen without moving files
Control Buttons
🗂️ Organize Files: Start the file organization process
🗑️ Clear Log: Clear the log display area
📁 Load Defaults: Auto-populate with standard directory structure
🔧 Technical Architecture
Core Components
DesktopCleanerGUI Class
Main application class that handles:

GUI layout and widget management
User input validation
Threading for background operations
Event handling and callbacks
TextHandler Class
Custom logging handler that:

Redirects log messages to GUI text widget
Ensures thread-safe GUI updates using tkinter.after()
Manages text widget state (normal/disabled)
Auto-scrolls to show latest entries
Threading Model
Main Thread: Handles GUI events and user interactions
Worker Thread: Executes file organization operations
Thread Safety: Uses tkinter.after() for safe GUI updates from worker threads
File Organization Logic
Leverages the desktop_cleaner_bot module:

OrganizerConfig: Configuration dataclass for organization parameters
organize(): Core function that performs file categorization and movement
setup_logging(): Configures logging system with specified level
📁 File Type Support
Audio Files
Music: .mp3, .wav, .flac, .aac, .ogg, .m4a
SFX: Same extensions but below size threshold
Video Files
Formats: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm
Image Files
Formats: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg
Document Files
Text: .txt, .doc, .docx, .pdf, .rtf
Spreadsheets: .xls, .xlsx, .csv
Presentations: .ppt, .pptx
🛡️ Safety Features
Input Validation
Verifies all required directories are specified
Checks source directory exists before processing
Validates numeric inputs (size thresholds)
Error Handling
Comprehensive exception handling with user-friendly messages
Graceful handling of file access errors
Continues processing even if individual files fail
File Safety
Dry Run Mode: Preview changes without moving files
Unique Naming: Prevents overwriting existing files
Symlink Handling: Skips symbolic links for safety
Detailed Logging: Complete audit trail of all operations
🎨 User Interface Details
Layout Structure
┌─ Title Bar ─────────────────────────────────┐
├─ Directory Configuration ───────────────────┤
│  ├─ Source Directory      [Browse]          │
│  ├─ Music Directory       [Browse]          │
│  ├─ SFX Directory         [Browse]          │
│  ├─ Video Directory       [Browse]          │
│  ├─ Image Directory       [Browse]          │
│  └─ Documents Directory   [Browse]          │
├─ Settings ─────────────────────────────────┤
│  ├─ SFX Size Threshold (MB)                 │
│  ├─ Log Level                               │
│  └─ ☑ Dry Run (Preview only)               │
├─ Controls ─────────────────────────────────┤
│  [🗂️ Organize] [🗑️ Clear Log] [📁 Defaults] │
├─ Progress Bar ─────────────────────────────┤
├─ Log Output ───────────────────────────────┤
│  │ Scrollable log display area             │
│  │ Real-time operation feedback            │
└─ Status Bar ───────────────────────────────┘

Copy

Insert

Visual Feedback
Progress Bar: Indeterminate progress during organization
Status Bar: Current operation status
Button States: Disabled during processing to prevent conflicts
Color Coding: Different log levels with appropriate formatting
🔍 Logging System
Log Levels
DEBUG: Detailed information for troubleshooting
INFO: General information about operations
WARNING: Important notices that don't stop processing
ERROR: Error conditions that may affect results
Log Format
2024-01-15 10:30:45 INFO Starting file organization...
2024-01-15 10:30:45 INFO Source: /Users/username/Desktop
2024-01-15 10:30:45 INFO Music: /Users/username/Desktop/Organized/Music
2024-01-15 10:30:46 INFO Moved file to Music: song.mp3

Copy

Insert

🚨 Troubleshooting
Common Issues
"Source directory does not exist"

Verify the source path is correct and accessible
Check directory permissions
"Permission denied" errors

Run with appropriate file system permissions
Check if files are in use by other applications
GUI becomes unresponsive

This shouldn't happen due to threading, but if it does, restart the application
Check system resources if processing very large directories
Files not moving in dry run mode

This is expected behavior - dry run only previews changes
Uncheck "Dry Run" to perform actual file movements
Performance Tips
Use dry run mode first to preview large operations
Close other applications if processing thousands of files
Monitor the log output for any error messages
🤝 Contributing
Development Setup
Fork the repository
Create a feature branch
Make your changes
Test thoroughly with various file types
Submit a pull request
Code Style
Follow PEP 8 Python style guidelines
Use meaningful variable and function names
Add docstrings for new classes and methods
Maintain thread safety for GUI operations
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Built with Python's tkinter for cross-platform compatibility
Uses threading for responsive user interface
Integrates with custom desktop_cleaner_bot module for core functionality
Made with ❤️ for organized desktops everywhere!

==================================================================================


# Wealth Calculator GUI

A comprehensive financial planning tool with a user-friendly graphical interface built using Python's Tkinter library. This application helps users calculate wealth projections and determine the time needed to reach financial freedom goals.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Application Modes](#application-modes)
- [File Structure](#file-structure)
- [Code Architecture](#code-architecture)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **Dual Calculation Modes**: Switch between wealth projection and financial freedom calculations
- **Interactive GUI**: Clean, intuitive interface with organized sections
- **Real-time Results**: Instant calculations with detailed year-by-year breakdowns
- **Input Validation**: Comprehensive error handling and user-friendly error messages
- **Placeholder Text**: Helpful examples in input fields
- **Scrollable Results**: Large output area with scrolling capability

### User Interface Features
- **Responsive Design**: Resizable window (640x560 default)
- **Mode Toggle**: Radio buttons to switch between calculation modes
- **Clear Organization**: Labeled frames for different sections
- **Action Buttons**: Calculate, Clear, and Quit functionality
- **French Interface**: Localized text in French

## 🔧 Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)
- Standard Python libraries:
  - `io`
  - `contextlib`

## 📦 Installation

1. **Clone or download the project files**:
   ```bash
   git clone <repository-url>
   cd wealth-calculator
   ```

2. **Ensure you have both required files**:
   - `wealth_calculator_gui.py` (GUI application)
   - `wealth_calculator.py` (calculation logic)

3. **Run the application**:
   ```bash
   python wealth_calculator_gui.py
   ```

## 🚀 Usage

### Starting the Application
```bash
python wealth_calculator_gui.py
```

### Basic Workflow
1. **Select Calculation Mode**:
   - **Returns Mode**: Project wealth over a specific number of years
   - **Freedom Mode**: Calculate years needed to reach a target wealth

2. **Enter Common Parameters**:
   - Current wealth (e.g., 10000)
   - Rate of return percentage (e.g., 7)
   - Monthly savings amount (e.g., 200)

3. **Enter Mode-Specific Parameters**:
   - **Returns Mode**: Investment period in years
   - **Freedom Mode**: Target wealth amount

4. **Calculate**: Click the "Calculer" button to see results

5. **View Results**: Detailed calculations appear in the scrollable output area

### Example Usage

#### Returns Mode Example
- Current Wealth: €10,000
- Rate of Return: 7%
- Monthly Savings: €200
- Investment Period: 10 years

**Result**: Year-by-year wealth projection showing compound growth

#### Freedom Mode Example
- Current Wealth: €10,000
- Rate of Return: 7%
- Monthly Savings: €200
- Target Wealth: €500,000

**Result**: Number of years needed to reach financial freedom

## 🎯 Application Modes

### 1. Returns Mode (Projection par années)
Calculates wealth accumulation over a specified time period.

**Formula**: 
- Annual Interest = Current Wealth × (Rate of Return / 100)
- New Wealth = Current Wealth + Annual Interest + (Monthly Savings × 12)

**Output**: Year-by-year breakdown showing wealth growth

### 2. Freedom Mode (Années jusqu'à l'objectif)
Determines how long it takes to reach a target wealth amount.

**Process**: 
- Iteratively calculates wealth growth year by year
- Stops when target wealth is exceeded
- Returns the number of years required

**Output**: Time to financial freedom message

## 📁 File Structure

```
wealth-calculator/
│
├── wealth_calculator_gui.py    # Main GUI application
├── wealth_calculator.py       # Core calculation functions
└── README.md                  # This documentation
```

### Key Files Description

#### `wealth_calculator_gui.py`
- **WealthCalculatorApp Class**: Main application window
- **UI Components**: Input fields, buttons, output area
- **Event Handlers**: Button clicks, mode switching
- **Input Validation**: Error checking and user feedback

#### `wealth_calculator.py`
- **calculate_wealth_by_year()**: Returns mode calculation
- **calculate_years_till_freedom()**: Freedom mode calculation
- **Command-line interface**: Alternative text-based interface

## 🏗️ Code Architecture

### Class Structure

```python
class WealthCalculatorApp(tk.Tk):
    def __init__(self):
        # Initialize window and variables
        
    def _build_ui(self):
        # Create all UI components
        
    def _toggle_mode(self):
        # Switch between calculation modes
        
    def _on_calculate(self):
        # Handle calculation button click
        
    def _parse_float(self, value_str, field_name):
        # Validate and convert input to float
```

### Key Methods

| Method | Purpose |
|--------|---------|
| `_build_ui()` | Creates all GUI components and layout |
| `_toggle_mode()` | Shows/hides mode-specific input fields |
| `_on_calculate()` | Processes inputs and displays results |
| `_add_labeled_entry()` | Helper for creating labeled input fields |
| `_clear_placeholder()` | Removes placeholder text on focus |
| `_parse_float()/_parse_int()` | Input validation and conversion |

### UI Components

1. **Mode Selection Frame**: Radio buttons for choosing calculation mode
2. **Input Frame**: All input fields with labels and placeholders
3. **Action Frame**: Calculate, Clear, and Quit buttons
4. **Output Frame**: Scrollable text area for results

## 🎨 User Interface Design

### Layout Structure
```
┌─────────────────────────────────────┐
│ Mode Selection (Radio Buttons)      │
├─────────────────────────────────────┤
│ Input Fields                        │
�� ├─ Current Wealth                   │
│ ├─ Rate of Return                   │
│ ├─ Monthly Savings                  │
│ └─ Mode-specific field              │
├─────────────────────────────────────┤
│ [Calculate] [Clear]        [Quit]   │
├─────────────────────────────────────┤
│ Results (Scrollable Text Area)      │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

### Color Scheme & Styling
- Clean, professional appearance
- Standard Tkinter widgets with proper spacing
- Organized sections with labeled frames
- Responsive layout that adapts to window resizing

## 🔍 Error Handling

The application includes comprehensive error handling:

### Input Validation
- **Type Checking**: Ensures numeric inputs are valid
- **Field Validation**: Checks all required fields are filled
- **Range Validation**: Prevents negative or unrealistic values

### Error Messages
- **User-Friendly**: Clear, descriptive error messages in French
- **Field-Specific**: Identifies which field has the invalid input
- **Modal Dialogs**: Error messages appear in popup windows

### Exception Handling
```python
try:
    # Calculation logic
except ValueError as e:
    messagebox.showerror("Erreur de saisie", str(e))
except Exception as e:
    messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] Both calculation modes work correctly
- [ ] Input validation catches invalid entries
- [ ] Mode switching shows/hides appropriate fields
- [ ] Clear button empties the output area
- [ ] Window resizing works properly
- [ ] Placeholder text functions correctly

### Test Cases

#### Valid Inputs
- Positive numbers for all financial fields
- Reasonable percentages for rate of return
- Integer values for years

#### Invalid Inputs
- Non-numeric text in number fields
- Negative values
- Empty required fields

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test all new features thoroughly
- Update documentation as needed

## 📝 Future Enhancements

### Potential Features
- **Data Export**: Save calculations to CSV/PDF
- **Charts & Graphs**: Visual representation of wealth growth
- **Multiple Scenarios**: Compare different investment strategies
- **Inflation Adjustment**: Account for inflation in calculations
- **Currency Support**: Multiple currency options
- **Dark Mode**: Alternative UI theme
- **Localization**: Support for multiple languages

### Technical Improvements
- **Database Integration**: Store calculation history
- **Configuration File**: User preferences and settings
- **Unit Tests**: Automated testing suite
- **Logging**: Application activity logging

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support +212 663 796 930 or EmailMe : h.garoum@gmail.com

For questions, issues, or contributions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

---

**Note**: This application is for educational and planning purposes only. Always consult with financial professionals for investment advice.