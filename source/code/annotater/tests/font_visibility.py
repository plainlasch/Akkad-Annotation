from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import Toplevel, Listbox

# Example with PIL for rendering text
def render_text_with_pil(text):
    font_path = "C:\\Users\\schla\\Downloads\\Noto_Sans_Cuneiform\\NotoSansCuneiform-Regular.ttf"
    font = ImageFont.truetype(font_path, 24)
    img = Image.new('RGB', (500, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 25), text, font=font, fill=(0, 0, 0))
    img.show()

# Call it with text containing cuneiform
render_text_with_pil("𒀸 𒀹 𒀺")  # Example cuneiform characters