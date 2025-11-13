import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from rembg import remove
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os
import io
import webbrowser
import numpy as np
from scipy.ndimage import gaussian_laplace, gaussian_filter
import threading
import sys
from about_window import show_about_window  # ✅ import About terpisah


class RemoveBGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧹 Remove Background App")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # === Background Gradient ===
        self.gradient_bg()

        self.image_data = None
        self.removed_image = None

        # === FRAME UTAMA ===
        main_frame = tk.Frame(root, bg="#000000", relief="flat")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # === LABEL JUDUL ===
        title = tk.Label(
            main_frame,
            text="🧹 Remove Background App",
            font=("Segoe UI", 20, "bold"),
            bg="#e3f2fd",
            fg="#0d47a1"
        )
        title.grid(row=0, column=0, columnspan=3, pady=20)

        # === PREVIEW AREA ===
        self.preview_label = tk.Label(
            main_frame,
            text="Preview Gambar",
            width=80,
            height=20,
            bg="#fafafa",
            fg="#616161",
            relief="ridge"
        )
        self.preview_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # === TEXT LOADING ===
        self.loading_text = tk.Label(
            self.preview_label,
            text="⏳ Sedang menghapus background, tunggu sebentar…",
            bg="#fafafa",
            fg="black",
            font=("Segoe UI", 12, "italic")
        )
        self.loading_text.place_forget()

        # ✅ Tombol baru: fungsi Aan
        tk.Button(
            main_frame, text="🖼️ Ganti BG Gambar", command=self.replace_background_with_image,
            bg="#26a69a", fg="white", font=("Segoe UI", 10, "bold"),
            width=20, relief="flat"
        ).grid(row=3, column=1, padx=10, pady=5)

        # ✅ Tentang / README
        tk.Button(
            main_frame, text="📘 Tentang / README", command=lambda: show_about_window(self.root),
            bg="#8d6e63", fg="white", font=("Segoe UI", 10, "bold"),
            width=20, relief="flat"
        ).grid(row=3, column=2, padx=10, pady=5)

        # === CREDIT BAWAH ===
        credit = tk.Label(
            root,
            text="© 2025 - Tim RemoveBG Project",
            font=("Segoe UI", 9),
            bg="#e3f2fd",
            fg="#0d47a1"
        )
        credit.pack(side="bottom", pady=5)

    # ------------------------------------------------------------
    #  Fungsi untuk mengganti background dengan gambar lain
    #  Aan
    # ------------------------------------------------------------
    def replace_background_with_image(self):
        """
        Menghapus background gambar utama, lalu menggantinya
        dengan gambar background lain yang dipilih pengguna.
        """
        if not self.removed_image:
            messagebox.showwarning("Peringatan", "Hapus background dulu sebelum ganti BG gambar!")
            return

        bg_path = filedialog.askopenfilename(
            title="Pilih Gambar Background",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if not bg_path:
            return

        try:
            bg_image = Image.open(bg_path).convert("RGBA")
            bg_image = bg_image.resize(self.removed_image.size)

            combined = Image.new("RGBA", self.removed_image.size)
            combined.paste(bg_image, (0, 0))
            combined.paste(self.removed_image, (0, 0), self.removed_image)

            self.display_image(combined)
            self.removed_image = combined

            messagebox.showinfo("Sukses", "Background berhasil diganti dengan gambar lain!")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengganti background: {e}")



    def display_image(self, img):
        """
        display_image(img)
        """
        max_width, max_height = 700, 500
        w, h = img.size

        if w > max_width or h > max_height:
            ratio = min(max_width / w, max_height / h)
            new_size = (int(w * ratio), int(h * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=img_tk, text="")
        self.preview_label.image = img_tk
        self.preview_label.config(width=img.width, height=img.height)


if __name__ == "__main__":
    root = tk.Tk()
    app = RemoveBGApp(root)
    root.mainloop()
