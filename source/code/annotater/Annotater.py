import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import Image, ImageTk
import csv
import json
import io
import base64
from Sign_Detect import SignDetect

class ImageAnnotator:
    def __init__(self, root, json_file):
        self.root = root
        self.root.title("Akkad Annotator")

        # Main layout: Canvas on the left, Text widget on the right
        self.canvas = tk.Canvas(root, width=800, height=600, bg="gray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.text_frame = tk.Frame(root)
        self.text_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.annotation_text = tk.Text(self.text_frame, width=30, height=40, wrap=tk.WORD)
        self.annotation_text.pack(fill=tk.BOTH, expand=True)
        self.annotation_text.insert(tk.END, "Annotations will appear here...")

        # Buttons
        self.btn_load = tk.Button(root, text="Load Image", command=self.load_image)
        self.btn_load.pack(side=tk.TOP)

        self.btn_save = tk.Button(root, text="Save Annotations", command=self.save_annotations)
        self.btn_save.pack(side=tk.TOP)

        self.btn_load_annotations = tk.Button(root, text="Load Annotations", command=self.load_annotations)
        self.btn_load_annotations.pack(side=tk.TOP)

        # Add the Sign Detect button
        self.btn_sign_detect = tk.Button(root, text="Sign Detect", command=self.open_sign_detect)
        self.btn_sign_detect.pack(side=tk.TOP, pady=10)
        
        #Annotations
        self.annotations = []  # This will contain annotation data including cuneiform text
        self.translated_cuneiform_text = ""  # Store cuneiform translation

        # Edit Rectangles
        self.selected_rectangle = None
        self.rect_start_x = None
        self.rect_start_y = None

        # Bind additional events for moving and deleting
        self.canvas.bind("<ButtonPress-3>", self.start_move_or_delete)  # Right-click to start move/delete
        self.canvas.bind("<B3-Motion>", self.move_rectangle)  # Right-click drag to move
        self.canvas.bind("<ButtonRelease-3>", self.stop_move)

        # Variables
        self.image = None
        self.image_tk = None
        self.rectangles = []
        self.selected_rectangle = None
        self.annotations = []
        self.start_x = None
        self.start_y = None
        self.current_label = ""
        self.json_file = json_file

        # Undo stack for annotation actions
        self.undo_stack = []

        # Load labels from the CSV file
        self.labels = self.load_labels_from_json()

        # Bind Events
        self.canvas.bind("<ButtonPress-1>", self.start_draw_or_select)
        self.canvas.bind("<B1-Motion>", self.drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Bind Ctrl+Z for undo functionality
        self.root.bind("<Control-z>", self.undo)

    def load_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
        if filepath:
            self.image = Image.open(filepath)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.rectangles = []
            self.annotations = []
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.update_annotation_text()

    def load_labels_from_json(self):
        """Load labels from the lookup-dict.json"""
        labels = []
        with open(self.json_file, encoding="utf-8") as f:
            file = json.load(f)
            for key, value in file.items():
                labels.append(key)
        return sorted(labels)

    def start_draw_or_select(self, event):
        """Handle clicking to either select a rectangle or start a new one."""
        for rect_id, annotation in self.rectangles:
            x1, y1, x2, y2 = annotation["rectangle"]
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.select_rectangle(rect_id, annotation)
                return

        self.start_x, self.start_y = event.x, event.y
        self.current_rectangle = None

    def drawing(self, event):
        """Draw the rectangle dynamically while dragging the mouse."""
        if self.start_x and self.start_y:
            if self.current_rectangle:
                self.canvas.delete(self.current_rectangle)
            self.current_rectangle = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y, outline="red"
            )

    def stop_draw(self, event):
        """Finalize the rectangle and show the dropdown for label selection."""
        if self.start_x and self.start_y and self.current_rectangle:
            x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y
            rect_id = self.current_rectangle
            self.show_label_options(rect_id, x1, y1, x2, y2)

        self.start_x = None
        self.start_y = None
        self.current_rectangle = None

    def show_label_options(self, rect_id, x1, y1, x2, y2):
        """Show dropdown and entry field with an automatically opening, searchable dropdown menu."""
        # Create a frame for the dropdown and search entry
        label_frame = tk.Frame(self.root)
        label_frame.pack(side=tk.TOP, padx=10, pady=5)

        # Search entry for filtering labels
        search_entry = tk.Entry(label_frame)
        search_entry.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        search_entry.insert(0, "Search...")

        # Dropdown for labels
        dropdown_var = tk.StringVar()
        dropdown = ttk.Combobox(label_frame, textvariable=dropdown_var, values=self.labels, state="normal")
        dropdown.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        # Entry field for custom label
        custom_label_entry = tk.Entry(label_frame)
        custom_label_entry.pack(side=tk.TOP, padx=5, pady=5)

        # Automatically open the dropdown
        def open_dropdown():
            dropdown.event_generate("<Down>")

        # Add search functionality
        def filter_labels(event=None):
            search_term = search_entry.get().lower()
            filtered_labels = [label for label in self.labels if search_term in label.lower()]
            dropdown["values"] = filtered_labels
            if filtered_labels:
                open_dropdown()  # Automatically open the dropdown if there are results

        def clear_search(event):
            if search_entry.get() == "Search...":
                search_entry.delete(0, tk.END)

        # Events for filtering and clearing placeholder text
        search_entry.bind("<KeyRelease>", filter_labels)
        search_entry.bind("<FocusIn>", clear_search)

        # Dropdown selection handler
        def on_select(event=None):
            label = dropdown_var.get()
            if label:
                annotation = {"rectangle": (x1, y1, x2, y2), "label": label}
                self.rectangles.append((rect_id, annotation))
                self.annotations.append(annotation)
                self.update_annotation_text()
                self.undo_stack.append(('add', rect_id, annotation))  # Push to undo stack
                label_frame.destroy()  # Hide the label options after selection

        # Custom label entry handler
        def on_custom_label_entry(event):
            custom_label = custom_label_entry.get()
            if custom_label:
                annotation = {"rectangle": (x1, y1, x2, y2), "label": custom_label}
                self.rectangles.append((rect_id, annotation))
                self.annotations.append(annotation)
                self.update_annotation_text()
                self.undo_stack.append(('add', rect_id, annotation))  # Push to undo stack
                label_frame.destroy()  # Hide the label options after selection

        # Bind events
        dropdown.bind("<<ComboboxSelected>>", on_select)
        custom_label_entry.bind("<Return>", on_custom_label_entry)  # Allow custom label on "Enter"

    def undo(self, event=None):
        """Undo the last annotation action."""
        if not self.undo_stack:
            return  # No actions to undo

        last_action, rect_id, annotation = self.undo_stack.pop()

        if last_action == 'add':
            # Undo the addition of a rectangle
            self.canvas.delete(rect_id)
            self.rectangles = [(r_id, ann) for r_id, ann in self.rectangles if r_id != rect_id]
            self.annotations = [ann for ann in self.annotations if ann != annotation]
            self.update_annotation_text()

    def select_rectangle(self, rect_id, annotation):
        """Highlight selected rectangle and show/edit its label."""
        # Highlight the selected rectangle on the canvas
        self.canvas.itemconfig(rect_id, outline="blue")

        # Find the corresponding label in the text field
        self.highlight_annotation_text(annotation["label"])

        # Prompt to edit the label
        label = simpledialog.askstring(
            "Edit Label", "Current label: {}".format(annotation["label"])
        )
        if label:
            annotation["label"] = label
            self.update_annotation_text()

        # Reset the rectangle outline to red
        self.canvas.itemconfig(rect_id, outline="red")
    
    def highlight_annotation_text(self, label):
        """Highlight the line containing the given label in the text field."""
        # Clear previous highlights
        self.annotation_text.tag_remove("highlight", "1.0", tk.END)

        # Search for the label in the text field
        start_index = "1.0"
        while True:
            start_index = self.annotation_text.search(label, start_index, stopindex=tk.END)
            if not start_index:
                break  # No more matches

            # Find the end of the word
            end_index = f"{start_index}+{len(label)}c"

            # Add a tag to highlight the text
            self.annotation_text.tag_add("highlight", start_index, end_index)
            start_index = end_index  # Move to the next match

        # Configure the tag for highlighting
        self.annotation_text.tag_config("highlight", background="yellow", foreground="black")

    def update_annotation_text(self):
        """Update the text area with the current annotations grouped by lines."""
        self.annotation_text.delete(1.0, tk.END)  # Clear existing text
        if not self.annotations:
            self.annotation_text.insert(tk.END, "No annotations yet...")
            return

        lines = []
        line_tolerance = 20  # Adjust tolerance for grouping

        sorted_annotations = sorted(self.annotations, key=lambda a: a["rectangle"][1])

        for annotation in sorted_annotations:
            y1 = annotation["rectangle"][1]
            label = annotation["label"]

            added_to_line = False
            for line in lines:
                if abs(line["y"] - y1) <= line_tolerance:
                    line["labels"].append((annotation["rectangle"][0], label))
                    added_to_line = True
                    break

            if not added_to_line:
                lines.append({"y": y1, "labels": [(annotation["rectangle"][0], label)]})

        for line in lines:
            line["labels"].sort(key=lambda l: l[0])  # Sort by x-coordinate
            labels = [label for _, label in line["labels"]]
            self.annotation_text.insert(tk.END, " ".join(labels) + "\n")

    def save_annotations(self):
        """Save annotations and the image to a JSON file."""
        if self.image is None:
            messagebox.showwarning("Save Error", "No image loaded to save.")
            return

        # Convert the image to a base64 string
        buffer = io.BytesIO()
        self.image.save(buffer, format="PNG")  # Save the image in PNG format
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Create data structure
        data = {
            "image": encoded_image,
            "annotations": self.annotations
        }

        # Save to file
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filepath:
            with open(filepath, "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Save Successful", "Annotations and image saved!")

    def load_annotations(self):
        """Load annotations and the image from a JSON file."""
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            with open(filepath, "r") as f:
                data = json.load(f)

            # Decode the image
            encoded_image = data.get("image")
            if encoded_image:
                image_data = base64.b64decode(encoded_image)
                buffer = io.BytesIO(image_data)
                self.image = Image.open(buffer)
                self.image_tk = ImageTk.PhotoImage(self.image)
                self.canvas.delete("all")  # Clear the canvas
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

            # Load annotations
            self.annotations = data.get("annotations", [])
            self.redraw_annotations()

    def redraw_annotations(self):
        """Redraw all saved rectangles and their labels."""
        self.rectangles = []
        for annotation in self.annotations:
            x1, y1, x2, y2 = annotation["rectangle"]
            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")
            self.rectangles.append((rect_id, annotation))
        self.update_annotation_text()
    
    def start_move_or_delete(self, event):
        """Handle right-click to select a rectangle for moving or deleting."""
        for rect_id, annotation in self.rectangles:
            x1, y1, x2, y2 = annotation["rectangle"]
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.selected_rectangle = (rect_id, annotation)
                self.rect_start_x = event.x
                self.rect_start_y = event.y

                # Show a popup menu for deletion
                popup = tk.Menu(self.root, tearoff=0)
                popup.add_command(label="Delete Rectangle", command=self.delete_selected_rectangle)
                try:
                    popup.tk_popup(event.x_root, event.y_root)
                finally:
                    popup.grab_release()
                return

    def move_rectangle(self, event):
        """Move the selected rectangle dynamically."""
        if self.selected_rectangle:
            rect_id, annotation = self.selected_rectangle
            dx = event.x - self.rect_start_x
            dy = event.y - self.rect_start_y
            self.rect_start_x = event.x
            self.rect_start_y = event.y

            x1, y1, x2, y2 = annotation["rectangle"]
            new_coords = (x1 + dx, y1 + dy, x2 + dx, y2 + dy)
            annotation["rectangle"] = new_coords

            self.canvas.coords(rect_id, *new_coords)
            self.update_annotation_text()

    def stop_move(self, event):
        """Finalize the move operation."""
        self.selected_rectangle = None
        self.rect_start_x = None
        self.rect_start_y = None

    def delete_selected_rectangle(self):
        """Delete the selected rectangle and update annotations."""
        if self.selected_rectangle:
            rect_id, annotation = self.selected_rectangle
            
            # Delete the rectangle from the canvas
            self.canvas.delete(rect_id)
            
            # Remove the rectangle and its annotation from their respective lists
            self.rectangles = [(r_id, ann) for r_id, ann in self.rectangles if r_id != rect_id]
            self.annotations = [ann for ann in self.annotations if ann != annotation]
            
            # Update the annotations display
            self.update_annotation_text()
            
            # Clear the selected rectangle
            self.selected_rectangle = None

    def open_sign_detect(self):
        """Invoke SignDetect functionality."""
        try:
            # Provide the necessary file paths for SignDetect
            sign_detector = SignDetect(
                lookup_file="dictionary/lookup_dict.json",  # Update with your actual paths
                radical_file="dictionary/nb_radical_counts.json",
                custom_font="Esagil"
            )
            sign_detector.search_signs()  # Launch the SignDetect pop-up
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root, json_file="sign_lists/cuneiform_table_1.json")  # Specify your JSON file path
    root.mainloop()
