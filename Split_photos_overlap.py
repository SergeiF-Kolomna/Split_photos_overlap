import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

class ImageMergerApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Merger")

        self.image_files = []

        self.label = tk.Label(master, text="Select images to merge:")
        self.label.pack()

        self.select_button = tk.Button(master, text="Select Images", command=self.select_images)
        self.select_button.pack()

        self.merge_button = tk.Button(master, text="Merge Images", command=self.merge_images)
        self.merge_button.pack()

    def select_images(self):
        file_paths = filedialog.askopenfilenames(title="Select images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.image_files = sorted(file_paths, key=lambda x: os.path.getctime(x), reverse=True)
        print("Selected files:", self.image_files)

    def merge_images(self):
        if not self.image_files:
            print("Please select images first.")
            return

        merged_image = self.merge_images_in_order()
        if merged_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPG files", "*.jpg")])
            if save_path:
                merged_image.save(save_path)
                print(f"Merged image saved at {save_path}")

    #def merge_images_in_order(self):
    #    if not self.image_files:
    #        return None

    #    overlap_pixels = 20         # нахлёст верхнего на нижнее
    #    shift_pixels = 30           # сдвиг вправо

    #    merged_height = sum(Image.open(img).height for img in self.image_files) - (len(self.image_files) - 1) * overlap_pixels
    #    merged_width = max(Image.open(img).width for img in self.image_files) + shift_pixels
    #    merged_image = Image.new("RGB", (merged_width, merged_height), (255, 255, 255))

    #    current_height = 0
    #    for i, img_path in enumerate(self.image_files):
    #        img = Image.open(img_path)
    #        if i > 0:
    #            current_height -= overlap_pixels
    #        merged_image.paste(img, (shift_pixels, current_height))
    #        current_height += img.height

    #    return merged_image

    def merge_images_in_order(self):
        if not self.image_files:
            return None

        overlap_pixels = 20         # нахлёст верхнего на нижнее
        shift_pixels = 30           # сдвиг вправо
        target_short_side = 500     # размер короткой стороны при сжатии

        compressed_images = []

        for img_path in self.image_files:
            img = Image.open(img_path)
            # Resize the image to have a short side of 500 pixels
            short_side = min(img.width, img.height)
            scale_factor = target_short_side / short_side
            new_width = round(img.width * scale_factor)
            new_height = round(img.height * scale_factor)
            compressed_img = img.resize((new_width, new_height), Image.LANCZOS)
            compressed_images.append(compressed_img)

        merged_height = sum(img.height for img in compressed_images) - (len(compressed_images) - 1) * overlap_pixels
        merged_width = max(img.width for img in compressed_images) + shift_pixels
        merged_image = Image.new("RGB", (merged_width, merged_height), (255, 255, 255))

        current_height = 0
        for i, img in enumerate(compressed_images):
            if i > 0:
                current_height -= overlap_pixels
            merged_image.paste(img, (shift_pixels, current_height))
            current_height += img.height

        return merged_image

def main():
    root = tk.Tk()
    app = ImageMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

