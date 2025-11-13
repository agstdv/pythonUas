import os
import io
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageColor
from rembg import remove


# ------------------------------------------------------------
# Fungsi untuk menghapus background dan menyimpan hasil
# ------------------------------------------------------------
def remove_background(image_path):
    with open(image_path, "rb") as inp:
        result = remove(inp.read())
    return Image.open(io.BytesIO(result)).convert("RGBA")


# ------------------------------------------------------------
# GUI utama
# ------------------------------------------------------------
def start_app():
    global label_img

    root = tk.Tk()
    root.title("Remove Background App")
    root.geometry("420x620")
    root.configure(bg="#1e1e1e")

    label_title = tk.Label(
        root, text="Remove Background", fg="white", bg="#1e1e1e",
        font=("Segoe UI", 16, "bold")
    )
    label_title.pack(pady=20)

    btn_open = tk.Button(
        root, text="Pilih Gambar", command=open_image,
        width=20, bg="#00bfff", fg="white", font=("Segoe UI", 11)
    )
    btn_open.pack(pady=10)

    label_img = tk.Label(root, bg="#1e1e1e")
    label_img.pack(pady=10)

    btn_remove = tk.Button(
        root, text="Hapus Background",
        command=lambda: remove_background(getattr(label_img, "path", None)),
        width=20, bg="#32cd32", fg="white", font=("Segoe UI", 11)
    )
    btn_remove.pack(pady=10)

    root.mainloop()


# ------------------------------------------------------------
# Eksekusi utama
# ------------------------------------------------------------
if __name__ == "__main__":
    start_app()