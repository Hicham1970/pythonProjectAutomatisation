import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import io
from contextlib import redirect_stdout

from wealth_calculator import (
    calculate_wealth_by_year,
    calculate_years_till_freedom,
)


class WealthCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculateur de Patrimoine")
        self.geometry("640x560")
        self.resizable(True, True)

        # Etat/mode
        self.mode_var = tk.StringVar(value="returns")

        # Variables de saisie communes
        self.current_wealth_var = tk.StringVar()
        self.rate_of_return_var = tk.StringVar()
        self.monthly_savings_var = tk.StringVar()

        # Variables spécifiques aux modes
        self.years_var = tk.StringVar()          # pour returns
        self.target_wealth_var = tk.StringVar()  # pour freedom

        self._build_ui()
        self._toggle_mode()  # appliquer l'état initial

    def _build_ui(self):
        # Section: choix du mode
        mode_frame = tk.LabelFrame(self, text="Mode de calcul")
        mode_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Radiobutton(mode_frame, text="returns (projection par années)", variable=self.mode_var, value="returns", command=self._toggle_mode).pack(anchor="w", padx=10, pady=2)
        tk.Radiobutton(mode_frame, text="freedom (années jusqu'à l'objectif)", variable=self.mode_var, value="freedom", command=self._toggle_mode).pack(anchor="w", padx=10, pady=2)

        # Section: entrées
        inputs_frame = tk.LabelFrame(self, text="Entrées")
        inputs_frame.pack(fill=tk.X, padx=10, pady=10)

        # Champs communs
        self._add_labeled_entry(inputs_frame, "Patrimoine actuel", self.current_wealth_var, row=0, placeholder="ex: 10000")
        self._add_labeled_entry(inputs_frame, "Taux de rendement (%)", self.rate_of_return_var, row=1, placeholder="ex: 7")
        self._add_labeled_entry(inputs_frame, "Épargne mensuelle", self.monthly_savings_var, row=2, placeholder="ex: 200")

        # Frames spécifiques aux modes pour faciliter l'affichage/masquage
        self.returns_frame = tk.Frame(inputs_frame)
        self.returns_frame.grid(column=0, row=3, columnspan=2, sticky="ew", pady=(8, 0))
        self._add_labeled_entry(self.returns_frame, "Période (années)", self.years_var, row=0, placeholder="ex: 10")

        self.freedom_frame = tk.Frame(inputs_frame)
        self.freedom_frame.grid(column=0, row=4, columnspan=2, sticky="ew", pady=(8, 0))
        self._add_labeled_entry(self.freedom_frame, "Objectif de patrimoine", self.target_wealth_var, row=0, placeholder="ex: 500000")

        # Section: actions
        actions_frame = tk.Frame(self)
        actions_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(actions_frame, text="Calculer", command=self._on_calculate).pack(side=tk.LEFT, padx=5)
        tk.Button(actions_frame, text="Effacer", command=self._on_clear).pack(side=tk.LEFT, padx=5)
        tk.Button(actions_frame, text="Quitter", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        # Section: résultats
        output_frame = tk.LabelFrame(self, text="Résultats")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.output = ScrolledText(output_frame, wrap=tk.WORD, height=18)
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _add_labeled_entry(self, parent, label_text, variable, row=0, placeholder=None):
        label = tk.Label(parent, text=label_text)
        label.grid(column=0, row=row, sticky="w", padx=10, pady=4)
        entry = tk.Entry(parent, textvariable=variable)
        entry.grid(column=1, row=row, sticky="ew", padx=10, pady=4)
        parent.grid_columnconfigure(1, weight=1)
        if placeholder is not None:
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, v=variable: self._clear_placeholder(e, v))

    def _clear_placeholder(self, event, variable):
        # Efface le placeholder à la première prise de focus s'il n'y a pas encore eu de saisie
        if variable.get() and any(c.isalpha() for c in variable.get()):
            variable.set("")

    def _toggle_mode(self):
        mode = self.mode_var.get()
        if mode == "returns":
            self.returns_frame.grid()
            self.freedom_frame.grid_remove()
        else:
            self.freedom_frame.grid()
            self.returns_frame.grid_remove()

    def _on_clear(self):
        self.output.delete("1.0", tk.END)

    def _parse_float(self, value_str, field_name):
        try:
            return float(value_str)
        except (TypeError, ValueError):
            raise ValueError(f"Champ invalide: {field_name}. Veuillez saisir un nombre valide.")

    def _parse_int(self, value_str, field_name):
        try:
            return int(value_str)
        except (TypeError, ValueError):
            raise ValueError(f"Champ invalide: {field_name}. Veuillez saisir un entier valide.")

    def _on_calculate(self):
        self.output.delete("1.0", tk.END)
        mode = self.mode_var.get()
        try:
            current_wealth = self._parse_float(self.current_wealth_var.get(), "Patrimoine actuel")
            rate_of_return = self._parse_float(self.rate_of_return_var.get(), "Taux de rendement (%)")
            monthly_savings = self._parse_float(self.monthly_savings_var.get(), "Épargne mensuelle")

            buf = io.StringIO()
            with redirect_stdout(buf):
                if mode == "returns":
                    years = self._parse_int(self.years_var.get(), "Période (années)")
                    calculate_wealth_by_year(current_wealth, rate_of_return, monthly_savings, years)
                else:
                    target_wealth = self._parse_float(self.target_wealth_var.get(), "Objectif de patrimoine")
                    calculate_years_till_freedom(current_wealth, rate_of_return, monthly_savings, target_wealth)

            output_text = buf.getvalue().strip()
            if not output_text:
                output_text = "Aucun résultat produit par la fonction."
            self.output.insert(tk.END, output_text + "\n")
        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")


def main():
    app = WealthCalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
