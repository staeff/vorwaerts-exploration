from pathlib import Path
from PIL import Image
import shutil

def get_img_size(img_path):
    im = Image.open(img_path)
    return im.size

def is_adjacent(num1, num2):
    return abs(num1 - num2) <= 3


if __name__ == '__main__':

    cwd = Path(".")
    quad = Path('./quadratic')
    img_files = sorted(list(cwd.glob("ads/**/*.jpg")))
    for img in img_files:
        width, height = get_img_size(img)

        if width > 500 and is_adjacent(width, height):
            shutil.copyfile(img, quad / img.name)
            print(img)
            print(f'width: {width}')
            print(f'height: {height}')
