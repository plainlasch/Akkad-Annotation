import tkinter as tk
from tkinter import messagebox
import csv
import re
from tkinter.font import Font

class CuneiformConverter:
    def __init__(self, root, annotator, csv_file):
        self.annotator = annotator  # Reference to the main ImageAnnotator instance
        self.csv_file = csv_file
        self.dictionary = self.load_csv_to_dict()

        # Add "Into Cuneiform" button to the main interface
        self.cuneiform_button = tk.Button(root, text="Into Cuneiform", command=self.convert_text_to_cuneiform)
        self.cuneiform_button.pack(side=tk.TOP)

    def load_csv_to_dict(self):
        """Load the CSV file into a dictionary."""
        translation_dict = []
        try:
            with open(self.csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 2:  # Ensure there are at least two columns
                        plain_text, cuneiform_symbol = row
                        translation_dict.append((plain_text.strip(), cuneiform_symbol.strip()))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")
        return translation_dict

    def find_cuneiform(self, word):
        """Find the best cuneiform match using regex search."""
        for pattern, cuneiform in self.dictionary:
            if re.fullmatch(pattern, word, re.IGNORECASE):  # Perform a regex match
                return cuneiform
        return f"[{word}]"  # Return the word in brackets if no match is found

    def convert_text_to_cuneiform(self):
        """Convert text in the annotation text area to cuneiform while preserving lines."""
        input_text = self.annotator.annotation_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("No Text", "The annotation field is empty.")
            return

        # Split the input text into lines to preserve line structure
        lines = input_text.splitlines()
        translated_lines = []

        for line in lines:
            # Process each word and attempt translation for each word in the line
            words = line.split()
            translated_words = [self.find_cuneiform(word) for word in words]
            translated_line = " ".join(translated_words)
            translated_lines.append(translated_line)

        # Combine the translated lines back with line breaks
        cuneiform_text = "\n".join(translated_lines)

        # Show the cuneiform output with line breaks preserved
        self.show_cuneiform_output(cuneiform_text)

    def show_cuneiform_output(self, cuneiform_text):
        """Show the cuneiform result in a new popup window."""
        output_window = tk.Toplevel()
        output_window.title("Cuneiform Translation")
        output_window.geometry("500x400")  # Set a reasonable default size

        # Create a Text widget to display the result with Noto Sans font
        output_text = tk.Text(output_window, wrap=tk.WORD, width=50, height=20)
        output_text.pack(fill=tk.BOTH, expand=True)

        # Try to load Noto Sans font
        try:
            noto_font = Font(family="Noto Sans Cuneiform", size=14)
            output_text.configure(font=noto_font)
        except Exception as e:
            messagebox.showwarning("Font Warning", f"Noto Sans Cuneiform font not found. Using default font.\nError: {e}")

        # Insert the cuneiform text and ensure proper encoding
        try:
            output_text.insert(tk.END, cuneiform_text.encode("utf-8").decode("utf-8"))
        except UnicodeEncodeError as e:
            messagebox.showerror("Encoding Error", f"Error displaying cuneiform: {e}")

        output_text.configure(state=tk.DISABLED)  # Make text read-only

        # Add a close button
        close_button = tk.Button(output_window, text="Close", command=output_window.destroy)
        close_button.pack(pady=10)


