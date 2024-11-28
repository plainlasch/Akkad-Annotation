import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import platform
import subprocess

def install_font(font_file):
    """Installs a font by copying it to the appropriate system font directory."""
    system_platform = platform.system()

    if system_platform == "Windows":
        fonts_dir = os.path.join(os.environ['WINDIR'], "Fonts")
    elif system_platform == "Darwin":  # macOS
        fonts_dir = "/Library/Fonts"  # System-wide fonts folder
    elif system_platform == "Linux":
        fonts_dir = "/usr/share/fonts"  # Common system-wide fonts folder
    else:
        messagebox.showerror("Unsupported OS", f"{system_platform} is not supported for font installation.")
        return False

    # Make sure the fonts directory exists
    if not os.path.exists(fonts_dir):
        messagebox.showerror("Error", f"Fonts directory not found: {fonts_dir}")
        return False

    try:
        # Copy the font file to the system fonts folder
        shutil.copy(font_file, fonts_dir)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to install font {font_file}. Error: {e}")
        return False

def is_font_installed(font_name):
    """Checks if a font is already installed on the system."""
    try:
        test_font = Font(family=font_name)
        if test_font.actual("family") == font_name:
            return True
    except Exception:
        pass
    return False

def install_fonts_from_folder(font_folder):
    """Installs all .ttf fonts from the specified folder if not already installed."""
    if not os.path.exists(font_folder):
        messagebox.showerror("Error", f"Font folder '{font_folder}' not found.")
        return

    ttf_files = [f for f in os.listdir(font_folder) if f.endswith(".ttf")]

    if not ttf_files:
        messagebox.showerror("Error", "No .ttf files found in the specified folder.")
        return

    installed_fonts = []
    for ttf_file in ttf_files:
        font_name = os.path.splitext(ttf_file)[0]  # Remove the file extension
        if is_font_installed(font_name):
            installed_fonts.append(font_name)
        else:
            font_file_path = os.path.join(font_folder, ttf_file)
            if install_font(font_file_path):
                installed_fonts.append(font_name)

    if installed_fonts:
        messagebox.showinfo("Font Installation", f"Installed the following fonts: {', '.join(installed_fonts)}")
    else:
        messagebox.showinfo("Font Installation", "No new fonts were installed. All fonts were already installed.")

# Example usage
if __name__ == "__main__":
    # Ask the user to select the folder containing the .ttf files
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    font_folder = "source/fonts"

    if font_folder:
        install_fonts_from_folder(font_folder)
    else:
        messagebox.showwarning("No Folder Selected", "No folder was selected. Please select a folder containing .ttf fonts.")
