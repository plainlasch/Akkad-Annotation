import tkinter.font as tkFont
import tkinter as tk

root = tk.Tk()
families = list(tkFont.families())
families.sort()
print(families)