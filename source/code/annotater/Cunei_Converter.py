import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import json
import re

class CuneiformConverter:
    def __init__(self, root, annotator, json_file, font_size):
        self.annotator = annotator  # Reference to the main ImageAnnotator instance
        self.json_file = json_file  # Path to the JSON file containing cuneiform dictionary
        self.dictionary = self.load_json_to_dict()

        # Predefined font families
        self.available_fonts = ['Bisitun', 'Assurbanipal', 'Esagil', 'Persepolis', 'Santakku', 'SantakkuM', 'UllikummiA', 'UllikummiB', 'UllikummiC']
        self.chronologies = ["Neo-Assyrian", "Neo-Babylonian", "Old-Babylonian", "Hittite"]
        # Default selected font
        self.selected_font = self.chronologies[0]  # Default to the first font
        self.selected_font_size = font_size
        # Add buttons to the main interface
        self.cuneiform_button = tk.Button(root, text="Into Cuneiform", command=self.convert_text_to_cuneiform)
        self.cuneiform_button.pack(side=tk.TOP)

        self.font_label = tk.Label(root, text="Choose Font:")
        self.font_label.pack(side=tk.TOP)
        
        self.font_var = tk.StringVar(root)
        self.font_var.set(self.selected_font)  # Default to the first font in the list

        # Create dropdown menu for font selection
        self.font_menu = tk.OptionMenu(root, self.font_var, *self.chronologies, command=self.apply_selected_font)
        self.font_menu.pack(side=tk.TOP, pady=5)

    def load_json_to_dict(self):
        """Load the JSON file into a dictionary."""
        translation_dict = {}
        try:
            with open(self.json_file, 'r', encoding='utf-8') as jsonfile:
                translation_dict = json.load(jsonfile)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {e}")
        return translation_dict

    def find_cuneiform(self, word):
        """Find the best cuneiform match using the JSON dictionary."""
        # Search for exact match or try a pattern match using '.' separator
        if word in self.dictionary:
            return self.dictionary[word]
        
        # If exact match is not found, try splitting by '.' and matching
        pattern = re.sub(r'\.', '.', word)  # This keeps the pattern intact, you can modify to handle complex cases
        for key in self.dictionary.keys():
            if re.match(pattern, key):
                return self.dictionary[key]
        
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

        # Create a Text widget to display the result
        output_text = tk.Text(output_window, wrap=tk.WORD, width=50, height=20)
        output_text.pack(fill=tk.BOTH, expand=True)

        # Try to apply the selected font and size
        try:
            if self.selected_font == "Neo-Assyrian":
                self.selected_font = "Assurbanipal"
            elif self.selected_font == "Neo-Babylonian":
                self.selected_font = "Esagil"
            elif self.selected_font == "Old-Babylonian":
                self.selected_font = "Santakku"
            elif self.selected_font == "Hittite":
                self.selected_font = "UllikummiA"

            font_tuple = (self.selected_font, self.selected_font_size)
            output_text.configure(font=font_tuple)
            print(f"Font applied: {font_tuple}")  # Debug print the applied font

            # Check the font applied on the widget
            applied_font = output_text.cget("font")
            print(f"Actual applied font: {applied_font}")  # This should print the applied font and size
        except Exception as e:
            messagebox.showwarning("Font Warning", f"Error applying the selected font: {e}")
            output_text.configure(font=("Arial", self.selected_font_size))  # Fallback to Arial for testing

        # Insert the cuneiform text
        try:
            output_text.insert(tk.END, cuneiform_text.encode("utf-8").decode("utf-8"))
        except UnicodeEncodeError as e:
            messagebox.showerror("Encoding Error", f"Error displaying cuneiform: {e}")

        output_text.configure(state=tk.DISABLED)  # Make text read-only

        # Add a close button
        close_button = tk.Button(output_window, text="Close", command=output_window.destroy)
        close_button.pack(pady=10)


    def apply_selected_font(self, selected_font):
        """Apply the selected font to the converter."""
        self.selected_font = selected_font
        messagebox.showinfo("Font Selected", f"Font '{selected_font}' selected successfully.")
