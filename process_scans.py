from pathlib import Path
from PIL import Image
from lxml import etree
import json
import os

NS = '{http://www.loc.gov/standards/alto/ns-v2#}'

def crop_image(im, anzeige):
    """Gets coordinates"""
    file_id = anzeige['file_id']
    outpath = f'ads/{file_id}/'
    create_path(outpath)
    cropped = im.crop(anzeige['coords'])
    cropped.save(f'{outpath}{file_id}-{anzeige["block_id"]}.jpg')

def extract_id(block_id_string):
    """Gets something block id string like Page1_Block1
    and returns the remaining number when Page1_Block
    is removed.
    """
    return block_id_string.replace("Page1_Block", "")

def get_adv_coords(item_attrs):
    """
    """
    x0 = int(item_attrs['HPOS'])
    y0 = int(item_attrs['VPOS'])
    x1 = int(item_attrs['WIDTH']) + x0
    y1 = int(item_attrs['HEIGHT']) + y0
    return (x0, y0, x1, y1)

def create_path(path):
    """Create folder if does not exists"""
    current_dir = Path.cwd()
    dirname = current_dir / path
    if not dirname.exists():
        os.mkdir(dirname)

if __name__ == "__main__":
    cwd = Path(".")
    xml_files = sorted(list(cwd.glob("xml/*.xml")))

    create_path('ads')

    for i, xml_file in enumerate(xml_files):
        # parse XML file into etree
        tree = etree.parse(str(xml_file))

        # id string is filename w/o extensions
        file_id_string = xml_file.stem

        # Create PIL Image object
        im = Image.open(f'images/{file_id_string}.jpg')

        # Extract all textblocks elements
        textblocks = tree.findall(f".//{NS}TextBlock")

        for block in textblocks:
            # Assign nodes attributes dict to a var
            anzeige = {}
            item_attrs = block.attrib
            anzeige['coords'] = get_adv_coords(item_attrs)
            anzeige["block_id"] = extract_id(item_attrs['ID'])
            anzeige["file_id"] = file_id_string

            crop_image(im, anzeige)
