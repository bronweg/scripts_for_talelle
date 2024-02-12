#!/usr/bin/python3.10
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
import os

def cm_to_points(cm):
    inches = cm / 2.54
    return inches * 72

def resize_image(image_path, max_width_points, max_height_points):
    with Image.open(image_path) as img:
        img_ratio = img.width / img.height
        if img.width / img.height > max_width_points / max_height_points:
            new_width = min(img.width, max_width_points)
            new_height = int(new_width / img_ratio)
        else:
            new_height = min(img.height, max_height_points)
            new_width = int(new_height * img_ratio)

        # Возвращаем новые размеры для использования при размещении
        return image_path, new_width, new_height

def collect_and_resize_images(directory, max_width_cm, max_height_cm):
    max_width_points = cm_to_points(max_width_cm)
    max_height_points = cm_to_points(max_height_cm)
    images = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                path = os.path.join(root, filename)
                images.append(resize_image(path, max_width_points, max_height_points))
    # sort the list here
    images.sort(reverse=True, key=lambda image : image[2])
    return images

def place_images_on_pdf(images, output_pdf_path, margin_points):
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    page_width, page_height = A4
    margin = margin_points
    x, y = margin, page_height - margin
    max_row_height = 0

    for path, img_width, img_height in images:
        if x + img_width > page_width - margin:
            x = margin
            y -= max_row_height + margin
            max_row_height = 0
        if y - img_height < margin:
            c.showPage()
            x, y = margin, page_height - margin
            max_row_height = 0
        c.drawImage(path, x, y - img_height, width=img_width, height=img_height)
        x += img_width + margin
        max_row_height = max(max_row_height, img_height)
    c.save()

# Графический интерфейс пользователя
def create_gui():
    root = tk.Tk()
    root.title("Images to PDF Converter")

    # Локализация
    languages = {'English': {'choose_directory': "Choose Directory...",
                             'output_file': "Choose Output PDF...",
                             'max_width': "Max Image Width (cm):",
                             'max_height': "Max Image Height (cm):",
                             'margin': "Margin (cm):",
                             'process_images': "Process Images",
                             'directory_does_not_exist': "The selected directory does not exist.",
                             'file_cannot_be_created': "The output file cannot be created.",
                             'scale_exceeds_a4': "The given scale exceeds the size of A4 paper.",
                             'success': "PDF has been created successfully!"},
                  'עברית': {'choose_directory': "בחר תיקייה...",
                            'output_file': "בחר קובץ PDF לפלט...",
                            'max_width': "רוחב מקסימלי לתמונה (ס\"מ):",
                            'max_height': "גובה מקסימלי לתמונה (ס\"מ):",
                            'margin': "שוליים (ס\"מ):",
                            'process_images': "עבד תמונות",
                            'directory_does_not_exist': "התיקייה שנבחרה לא קיימת.",
                            'file_cannot_be_created': "לא ניתן ליצור את הקובץ המבוקש.",
                            'scale_exceeds_a4': "המידות שהוזנו גדולות ממידות דף A4.",
                            'success': "ה-PDF נוצר בהצלחה!"}}

    current_language = tk.StringVar(value='English')  # Default language

    # def update_texts():
    #     lang = current_language.get()
    #     for widget, text_id in widgets_to_update:
    #         widget.config(text=texts[lang][text_id])

    # Функция обновления текстов с учетом направления письма
    def update_texts():
        lang = current_language.get()
        is_rtl = lang == 'עברית'  # Проверяем, является ли текущий язык языком с написанием справа налево
        for widget, text_id in widgets_to_update:
            text = texts[lang][text_id]
            if is_rtl:
                text = get_display(text)  # Преобразование текста для отображения справа налево
            widget.config(text=text)

    def choose_directory():
        directory = filedialog.askdirectory()
        if not os.path.exists(directory):
            messagebox.showerror("Error", texts[current_language.get()]["directory_does_not_exist"])
            return
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

    def choose_output_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, file_path)

    def save_settings():
        directory = directory_entry.get()
        output_pdf_path = file_path_entry.get()
        max_width_cm = float(max_width_entry.get())
        max_height_cm = float(max_height_entry.get())
        margin_cm = float(margin_entry.get())
        margin_points = cm_to_points(margin_cm)

        # Проверки
        if not os.path.isdir(directory):
            messagebox.showerror("Error", texts[current_language.get()]["directory_does_not_exist"])
            return
        if not os.access(os.path.dirname(output_pdf_path), os.W_OK):
            messagebox.showerror("Error", texts[current_language.get()]["file_cannot_be_created"])
            return
        if cm_to_points(max_width_cm) > A4[0] or cm_to_points(max_height_cm) > A4[1]:
            messagebox.showerror("Error", texts[current_language.get()]["scale_exceeds_a4"])
            return

        images = collect_and_resize_images(directory, max_width_cm, max_height_cm)
        place_images_on_pdf(images, output_pdf_path, margin_points)
        messagebox.showinfo("Success", texts[current_language.get()]["success"])

    # Widgets
    lang_label = tk.Label(root, text="Language:")
    lang_label.pack()
    lang_combobox = ttk.Combobox(root, textvariable=current_language, values=list(languages.keys()), state="readonly")
    lang_combobox.pack()
    lang_combobox.bind('<<ComboboxSelected>>', lambda event: update_texts())

    directory_label = tk.Label(root, text="Directory with Images:")
    directory_entry = tk.Entry(root, width=50)
    choose_dir_button = tk.Button(root, text="Choose...", command=choose_directory)

    file_path_label = tk.Label(root, text="Output PDF Path (with filename):")
    file_path_entry = tk.Entry(root, width=50)
    choose_file_button = tk.Button(root, text="Choose...", command=choose_output_file)

    max_width_label = tk.Label(root, text="Max Image Width (cm):")
    max_width_entry = tk.Entry(root)
    max_height_label = tk.Label(root, text="Max Image Height (cm):")
    max_height_entry = tk.Entry(root)
    margin_label = tk.Label(root, text="Margin (cm):")
    margin_entry = tk.Entry(root)
    margin_entry.insert(0, "0.3")  # Default margin

    process_button = tk.Button(root, text="Process Images", command=save_settings)

    # Layout
    directory_label.pack()
    directory_entry.pack()
    choose_dir_button.pack()

    file_path_label.pack()
    file_path_entry.pack()
    choose_file_button.pack()

    max_width_label.pack()
    max_width_entry.pack()
    max_height_label.pack()
    max_height_entry.pack()
    margin_label.pack()
    margin_entry.pack()

    process_button.pack()

    # To update texts when changing language
    widgets_to_update = [
        (choose_dir_button, 'choose_directory'),
        (choose_file_button, 'output_file'),
        (max_width_label, 'max_width'),
        (max_height_label, 'max_height'),
        (margin_label, 'margin'),
        (process_button, 'process_images')
    ]

    texts = languages  # Assign localized texts based on selected language
    update_texts()  # Update texts to current language

    root.mainloop()

if __name__ == "__main__":
    create_gui()
