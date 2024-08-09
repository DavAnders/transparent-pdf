import fitz
import tkinter as tk
from tkinter import filedialog, simpledialog
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
        self.alpha = 0.5 # Default transparency
        self.geometry("+100+100")  # Initial window position
        self.img = render_pdf_page(pdf_path, page_num)
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.geometry(f"{self.img.width}x{self.img.height}")
        self.update_alpha(self.alpha)
        
        # Separate window for the slider to not be affected by transparency
        self.slider_window = tk.Toplevel(self)
        self.slider_window.title("Transparency")
        self.slider_window.geometry("200x50+100+50")  # Positioning it near the main window
        self.slider_window.attributes("-topmost", True)
        self.slider_window.wm_transient(self)

        # Force the slider window to be on top, might be temporary
        self.slider_window.lift()
        self.slider_window.attributes("-topmost", True)
        self.slider_window.after(10, lambda: self.slider_window.lift())
        
        self.slider = tk.Scale(self.slider_window, from_=0.1, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, command=self.update_alpha)
        self.slider.set(self.alpha)
        self.slider.pack(fill=tk.X)

    def update_alpha(self, value):
        self.alpha = float(value)
        self.attributes("-alpha", self.alpha)

def main():
    root = tk.Tk()
    root.withdraw()  # Hiding the root window

    pdf_path = filedialog.askopenfilename(
        title="Select PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not pdf_path:
        print("No file selected. Exiting.")
        return
    
    page_num = simpledialog.askinteger("Page Number", "Enter the page number:", minvalue=1)

    if page_num is None:
        print("No page number provided. Exiting.")
        return
    
    root.destroy()  # Close hidden root window -- Behavior needs changing to fix slider attach to main

    app = TransparentPDF(pdf_path, page_num - 1)
    app.mainloop()



if __name__ == '__main__':
    main()