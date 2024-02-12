#!/home/linuxbrew/.linuxbrew/bin/python3
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

def place_images_on_pdf(images, output_pdf_path, margin):
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    page_width, page_height = A4
    x, y = margin, page_height - margin  # Начальные координаты с учетом отступа
    max_row_height = 0

    for path, img_width, img_height in images:
        if x + img_width > page_width - margin:
            x = margin  # Сброс X с учетом отступа
            y -= max_row_height + 10
            max_row_height = 0
        if y - img_height < margin:  # Проверяем, достаточно ли места с учетом нижнего отступа
            c.showPage()
            x, y = margin, page_height - margin
            max_row_height = 0
        c.drawImage(path, x, y - img_height, width=img_width, height=img_height)
        x += img_width + 10
        max_row_height = max(max_row_height, img_height)
    c.save()

if __name__ == "__main__":
    directory = "photos"
    max_width_cm, max_height_cm = 5, 10
    margin = cm_to_points(0.3)  # Например, 1 см отступ
    output_pdf_path = "output_images.pdf"
    images = collect_and_resize_images(directory, max_width_cm, max_height_cm)
    place_images_on_pdf(images, output_pdf_path, margin)
    print(f"PDF document '{output_pdf_path}' has been created with images.")
