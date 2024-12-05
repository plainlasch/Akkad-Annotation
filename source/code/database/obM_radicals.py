"""Old-Babylonian Monumental Radical annotation"""
import tkinter as tk
from tkinter import messagebox
import json
import os

# Input file and output file
LOOKUP_DICT_FILE = "dictionary/lookup_dict.json"
RADICAL_COUNTS_FILE = "dictionary/obM_radical_counts.json"

# Load the lookup dictionary
with open(LOOKUP_DICT_FILE, "r", encoding="utf-8") as f:
    lookup_dict = json.load(f)

# Load or initialize the radical counts
if os.path.exists(RADICAL_COUNTS_FILE):
    try:
        with open(RADICAL_COUNTS_FILE, "r", encoding="utf-8") as f:
            radical_counts = json.load(f)
        # Check if the file is valid (non-empty and a dictionary)
        if not isinstance(radical_counts, dict):
            raise ValueError("Invalid data structure")
    except (json.JSONDecodeError, ValueError):
        # Reset if the file is empty or invalid
        radical_counts = {}
else:
    radical_counts = {}

# Radicals to annotate
radicals = ["𒀸", "𒀹", "𒀺", "𒁹", "𒌋"]

# Function to save progress
def save_progress():
    with open(RADICAL_COUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(radical_counts, f, ensure_ascii=False, indent=4)

# Main application
class AnnotatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cuneiform Annotator")

        # Center the window
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Find next sign to annotate
        self.keys = list(lookup_dict.keys())
        self.index = next((i for i, key in enumerate(self.keys) if lookup_dict[key] not in radical_counts), len(self.keys))
        
        if self.index >= len(self.keys):
            messagebox.showinfo("Info", "All signs are already annotated!")
            root.destroy()
            return

        self.current_sign = self.keys[self.index]

        # UI Setup
        self.label = tk.Label(root, text="Annotate the Radical Counts for Old-Babylonian Monumental", font=("Arial", 24))
        self.label.pack(pady=20)

        self.cuneiform_label = tk.Label(root, text=lookup_dict[self.current_sign], font=("SantakkuM", 60))
        self.cuneiform_label.pack(pady=30)

        self.entries = {}
        for radical in radicals:
            frame = tk.Frame(root)
            frame.pack(pady=10)

            tk.Label(frame, text=radical, font=("Assurbanipal", 24)).pack(side=tk.LEFT, padx=10)
            entry = tk.Entry(frame, font=("Arial", 18), width=10)
            entry.pack(side=tk.LEFT, padx=10)
            self.entries[radical] = entry

        self.submit_button = tk.Button(root, text="Submit", command=self.submit, font=("Arial", 20))
        self.submit_button.pack(pady=30)

        # Bind the Enter key to the submit function
        root.bind("<Return>", lambda event: self.submit())

    def submit(self):
        # Gather input
        try:
            counts = {radical: int(self.entries[radical].get()) for radical in radicals}
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers for all radicals.")
            return

        # Save to radical_counts
        radical_counts[lookup_dict[self.current_sign]] = counts
        save_progress()

        # Move to the next sign
        self.index += 1
        if self.index >= len(self.keys):
            messagebox.showinfo("Info", "All signs have been annotated!")
            self.root.destroy()
        else:
            self.current_sign = self.keys[self.index]
            self.update_ui()

    def update_ui(self):
        # Update the UI for the next sign
        self.cuneiform_label.config(text=lookup_dict[self.current_sign])
        for entry in self.entries.values():
            entry.delete(0, tk.END)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AnnotatorApp(root)
    root.mainloop()
