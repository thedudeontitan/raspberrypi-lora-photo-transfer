from PIL import Image
import cv2

def compress():
    image = Image.open("photo.jpg")

    image.save("image-file-compressed.jpg",
               "JPEG",
               optimize=True,
               quality=10)
