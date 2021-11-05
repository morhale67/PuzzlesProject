from pathlib import Path


def get_pic(image_name):
    path_images = Path(r'C:\Users\user\Desktop\PuzzleProject\Pictures')
    image_to_open = path_images / image_name
    return image_to_open
