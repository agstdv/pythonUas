import os
import io
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageColor
from rembg import remove

# ------------------------------------------------------------
# Fungsi Simpan
# ------------------------------------------------------------
def save_with_custom_name(image, default_name="output.png"):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")],
        initialfile=default_name,
        title="Simpan Gambar Sebagai"
    )
    if file_path:
        image.save(file_path)
        messagebox.showinfo("Sukses", f"Gambar disimpan di:\n{file_path}")
        return file_path
    else:
        return None

# ------------------------------------------------------------
# Fungsi untuk menghapus background dan menyimpan hasil
# ------------------------------------------------------------
def remove_background(image_path):
    with open(image_path, "rb") as inp:
        result = remove(inp.read())
    return Image.open(io.BytesIO(result)).convert("RGBA")

#tiyas
# ------------------------------------------------------------
# Fungsi untuk mengganti background dengan warna
# ------------------------------------------------------------
def change_background_color(image_path):
    if not image_path:
        messagebox.showwarning("Peringatan", "Pilih gambar terlebih dahulu.")
        return None

    try:
        color_hex = colorchooser.askcolor(title="Pilih Warna Background")[1]
        if not color_hex:
            return

        with open(image_path, "rb") as inp:
            result = remove(inp.read())

        image = Image.open(io.BytesIO(result)).convert("RGBA")

        bg_color = ImageColor.getrgb(color_hex)
        background = Image.new("RGBA", image.size, bg_color + (255,))
        combined = Image.alpha_composite(background, image)

        save_with_custom_name(combined.convert("RGB"), f"colored_bg_{os.path.basename(image_path)}")
        messagebox.showinfo("Sukses", "Warna background berhasil diganti.")
        return combined

    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengganti background: {e}")
        return None


# ------------------------------------------------------------
# GUI
# ------------------------------------------------------------
root = tk.Tk()
root.title("Remove Background App")
root.geometry("600x800")
root.configure(bg="#121212")

# Scrollable canvas
canvas = tk.Canvas(root, bg="#121212", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#121212")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Judul
tk.Label(
    scrollable_frame, text="✨ Remove Background App ✨",
    bg="#121212", fg="white", font=("Segoe UI", 20, "bold")
).grid(row=0, column=0, pady=20, sticky="n")

# Tombol pilih gambar
tk.Button(
    scrollable_frame, text="📂 Pilih Gambar",
    command=open_image, bg="#2196f3", fg="white",
    font=("Segoe UI", 11, "bold"), relief="flat", padx=15, pady=5
).grid(row=1, column=0, pady=10)

# Input preview
input_label = tk.Label(scrollable_frame, bg="#1e1e1e")
input_label.grid(row=2, column=0, pady=10)

# Tombol operasi
btn_frame = tk.Frame(scrollable_frame, bg="#121212")
btn_frame.grid(row=3, column=0, pady=10)

tk.Button(
    btn_frame, text="🧹 Hapus Background",
    command=lambda: threaded_process(remove_background, selected_path),
    bg="#4caf50", fg="white", font=("Segoe UI", 10, "bold"),
    relief="flat", padx=10, pady=5, width=22
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    btn_frame, text="🎨 Ganti Warna Background",
    command=lambda: threaded_process(change_background_color, selected_path),
    bg="#ff9800", fg="white", font=("Segoe UI", 10, "bold"),
    relief="flat", padx=10, pady=5, width=22
).grid(row=1, column=0, padx=5, pady=5)

# Preview hasil
tk.Label(
    scrollable_frame, text="📷 Preview Hasil:",
    bg="#121212", fg="#aaaaaa", font=("Segoe UI", 12, "bold")
).grid(row=4, column=0, pady=(20, 10))

preview_label = tk.Label(scrollable_frame, bg="#1e1e1e")
preview_label.grid(row=5, column=0, pady=10)

# Tombol simpan
save_button = tk.Button(
    scrollable_frame, text="💾 Simpan Gambar",
    command=save_with_custom_name,
    bg="#00bcd4", fg="white", font=("Segoe UI", 11, "bold"),
    relief="flat", padx=15, pady=5, state="disabled"
)
save_button.grid(row=6, column=0, pady=15)

# Label loading
loading_label = tk.Label(
    scrollable_frame, text="⏳ Memproses...",
    bg="#121212", fg="white", font=("Segoe UI", 14, "italic")
)
loading_label.place_forget()

root.mainloop()