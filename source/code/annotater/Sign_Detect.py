from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, Listbox
from tkinter import font as tkfont  # For handling custom fonts
import json
import pyperclip

class SignDetect:
    def __init__(self, lookup_file, radical_file, custom_font):
        # Load JSON files
        with open(lookup_file, "r", encoding="utf-8") as file:
            self.lookup_dict = json.load(file)

        with open(radical_file, "r", encoding="utf-8") as file:
            self.radical_dict = json.load(file)

        # Create a custom font using the font path
        self.custom_font = custom_font

    def search_signs(self):
        """Prompt user for radicals in a structured input window."""
        root = Tk()
        root.withdraw()  # Hide the main Tkinter window

        radical_counts = self.get_radical_counts(root)
        if radical_counts is None:
            return  # User canceled the dialog

        vert, hor, diag, wedge, extra = radical_counts

        # Find matches
        matching_signs = self.find_matches(vert, hor, diag, wedge, extra)
        if not matching_signs:
            messagebox.showinfo("No Matches", "No signs found for the given radicals.")
            return

        # Display matches
        self.display_matches(matching_signs, root)

    def get_radical_counts(self, parent):
        """Create a dialog window for entering radical counts."""
        counts = {}

        def submit():
            try:
                counts["𒀸"] = int(entries["𒀸"].get() or 0)
                counts["𒀹"] = int(entries["𒀹"].get() or 0)
                counts["𒀺"] = int(entries["𒀺"].get() or 0)
                counts["𒁹"] = int(entries["𒁹"].get() or 0)
                counts["𒌋"] = int(entries["𒌋"].get() or 0)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integer values.")

        dialog = Toplevel(parent)
        dialog.title("Enter Radical Counts")

        entries = {}
        for i, radical in enumerate(["𒀸", "𒀹", "𒀺", "𒁹", "𒌋"]):
            Label(dialog, text=f"{radical}:", font="Assurbanipal").grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(dialog)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[radical] = entry

        submit_button = Button(dialog, text="Submit", command=submit)
        submit_button.grid(row=len(entries), column=0, columnspan=2, pady=10)

        dialog.wait_window()  # Wait for the dialog to close

        if counts:
            return counts["𒀸"], counts["𒀹"], counts["𒀺"], counts["𒁹"], counts["𒌋"]
        return None

    def find_matches(self, vert, hor, diag, wedge, extra):
        """Filter signs based on radical counts."""
        matches = []
        for sign, radicals in self.radical_dict.items():
            if (
                radicals.get("𒀸", 0) == vert
                and radicals.get("𒀹", 0) == hor
                and radicals.get("𒀺", 0) == diag
                and radicals.get("𒁹", 0) == wedge
                and radicals.get("𒌋", 0) == extra
            ):
                matches.append(sign)
        return matches

    def display_matches(self, matching_signs, root):
        """Create a GUI for displaying and selecting matches."""
        result_window = Toplevel(root)
        result_window.title("Matching Signs")

        # Use the custom font in the Listbox
        listbox = Listbox(result_window, font=(self.custom_font, 30))
        for sign in matching_signs:
            listbox.insert("end", sign)
        listbox.pack(fill="both", expand=True)

        def select_sign():
            """Handle sign selection and fetch transliteration."""
            selection = listbox.curselection()
            popup = Toplevel()
            popup.title("Sign Selected")

            # Set the font to Assurbanipal, adjust size as needed
            font_style = ("Assurbanipal", 20)
            if selection:
                selected_sign = listbox.get(selection[0])
                # Reverse lookup: Find the transliteration for the selected sign
                transliteration = self.reverse_lookup(selected_sign)
                label_text = f"Sign: {selected_sign}\nTransliteration: {transliteration if transliteration else 'Unknown'}"
                label = Label(popup, text=label_text, font=font_style)
                label.pack(padx=20, pady=20)

                # Function to copy transliteration to clipboard
                def copy_to_clipboard():
                    pyperclip.copy(transliteration)  # Copy the transliteration to clipboard

                # Add the copy button
                copy_button = Button(popup, text="Copy to clipboard", command=copy_to_clipboard)
                copy_button.pack(pady=10)

            popup.mainloop()
            result_window.destroy()

        select_button = Button(result_window, text="Select Sign", command=select_sign)
        select_button.pack()


    def reverse_lookup(self, sign):
        """Reverse lookup: Find the transliteration for a given cuneiform sign."""
        # Loop through the lookup_dict to find the transliteration for the sign
        for transliteration, cuneiform_sign in self.lookup_dict.items():
            if cuneiform_sign == sign:
                return transliteration
        return None  # Return None if no match is found

# Main Execution
if __name__ == "__main__":
    lookup_file = "dictionary/lookup_dict.json"  # Replace with your lookup dictionary path
    radical_file = "dictionary/na_radical_counts.json"     # Replace with your radicals JSON file path

    detector = SignDetect(lookup_file, radical_file)
    detector.search_signs()
