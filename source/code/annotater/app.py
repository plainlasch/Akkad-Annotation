# Main script integration
import tkinter as tk

if __name__ == "__main__":
    from Annotater import ImageAnnotator  # Assume your main script is saved as `annotator_script.py`
    from Cunei_Converter import CuneiformConverter

    root = tk.Tk()
    annotator_app = ImageAnnotator(root, csv_file="sign_lists/cuneiform_table_1.csv")  # Replace with your actual CSV path
    CuneiformConverter(root, annotator_app, csv_file="sign_lists/cuneiform_table_1.csv")  # Replace with your Cuneiform dictionary CSV
    root.mainloop()