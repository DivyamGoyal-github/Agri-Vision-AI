from PIL import Image

def open_image_with_transparency(path):
    img = Image.open(path)
    if img.mode == "P" and "transparency" in img.info:
        img = img.convert("RGBA")
    return img

# Example usage:
# img = open_image_with_transparency("your_image.png")
