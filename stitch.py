import cv2
import os
import numpy as np

def stitch_images():
    image_files = os.listdir("./outputs/subimages")
    image_files.sort()

    if len(image_files) == 0:
        print("No sub-images found.")
        return None

    sub_images = []
    for image_file in image_files:
        image_path = os.path.join("./outputs/subimages", image_file)
        sub_image = cv2.imread(image_path)
        sub_images.append(sub_image)

    if len(sub_images) == 0:
        print("No sub-images found.")
        return None

    # Determine the dimensions of the stitched image
    rows = int(np.sqrt(len(sub_images)))
    cols = len(sub_images) // rows

    sub_height, sub_width, _ = sub_images[0].shape

    stitched_height = rows * sub_height
    stitched_width = cols * sub_width

    # Create the stitched image with black background
    stitched_image = np.zeros((stitched_height, stitched_width, 3), dtype=np.uint8)

    # Stitch the sub-images into the stitched image
    index = 0
    for i in range(rows):
        for j in range(cols):
            sub_image = sub_images[index]
            stitched_image[i * sub_height: (i + 1) * sub_height,
                           j * sub_width: (j + 1) * sub_width] = sub_image
            index += 1

    cv2.imwrite("stitched_image.jpg", stitched_image)
    return stitched_image

stitch_images()
