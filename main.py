from PIL import Image
import cv2

def compress():
    image = Image.open("photo.jpg")

    image.save("image-file-compressed.jpg",
               "JPEG",
               optimize=True,
               quality=10)

compress()


def split_images():
    img_arr = []
    # for image_path in image_paths:
    image = cv2.imread("photo.jpg", cv2.IMREAD_COLOR)  # read in image
    for i in range(0, image.shape[0], 33):  # loop through height-wise pixels of image, striding by 33
        for j in range(0, image.shape[1], 33):  # loop through width-wise pixels of image, striding by 33
            images = image[i:i + 33, j:j + 33, :]  # creating label image from h,w pixel to 33 pixels to the right and down
            img_arr.append(images)  # create list from label images
            # write images
            cv2.imwrite(f"../outputs/subimages/subimage{i}_{j}.png", images)

    print({"images": img_arr})
    return {"images": img_arr}

split_images()