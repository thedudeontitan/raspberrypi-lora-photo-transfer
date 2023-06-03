import os
import time
from PIL import Image
import cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil


class NewImageHandler(FileSystemEventHandler):
    def __init__(self, split_function):
        super().__init__()
        self.split_function = split_function

    def on_created(self, event):
        if event.is_directory:
            return

        image_path = event.src_path
        image_name = os.path.basename(image_path)
        self.split_function(image_name, image_path)
        self.move_image(image_path)

    @staticmethod
    def move_image(image_path):
        visited_folder = './visited'
        os.makedirs(visited_folder, exist_ok=True)
        new_image_name = os.path.basename(image_path)
        new_image_path = os.path.join(visited_folder, new_image_name)
        shutil.move(image_path, new_image_path)


def split_images(image_name, image_path):
    subfolder_name = image_name.split('.')[0]
    subfolder_path = os.path.join('./outputs/subimages', subfolder_name)
    os.makedirs(subfolder_path, exist_ok=True)

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (500, 500))
    for i in range(0, image.shape[0], 100):
        for j in range(0, image.shape[1], 100):
            sub_image = image[i:i + 100, j:j + 100, :]
            sub_image_path = os.path.join(subfolder_path, f'subimage_{i}_{j}.png')
            cv2.imwrite(sub_image_path, sub_image)


def monitor_folder(folder_path):
    event_handler = NewImageHandler(split_images)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Provide the path to the 'new' folder you want to monitor
folder_path = './new'
monitor_folder(folder_path)