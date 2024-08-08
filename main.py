import fitz
import tkinter as tk
from PIL import Image, ImageTk

def render_pdf_page(pdf_path, page_num):
    document = fitz.open(pdf_path)
    page = document.load_page(page_num)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return img

class TransparentPDF(tk.Tk):
    def __init__(self, pdf_path, page_num):
        super().__init__()
        self.attributes("-topmost", True)  # Always on top
        self.attributes("-alpha", 0.5)  # Transparency
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.img = render_pdf_page(pdf_path, page_num)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.geometry(f"{self.img.width}x{self.img.height}")

def main():
    print("Enter the path to the PDF file:")
    pdf_path = input()
    print("Enter the page number:")
    page_num = int(input()) - 1

    app = TransparentPDF(pdf_path, page_num)
    app.mainloop()



if __name__ == '__main__':
    main()