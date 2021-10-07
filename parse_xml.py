from lxml import etree
from pathlib import Path
from PIL import Image
import os

tree = etree.parse('data.xml')
root = tree.getroot()
NS = '{http://www.loc.gov/standards/alto/ns-v2#}'

anzeigen = []

def process_item(item):
    """Gets a block node, either TextBlock
        or Illustration and returns a
        dictionary with its attributes
    """
    anzeige = {}
    anzeige['id'] = extract_id(item.attrib['ID'])
    anzeige['coords'] = extract_coords(item.attrib)
    return anzeige

def extract_id(identifier):
    """Gets something like Page1_Block1

    Return last digit
    """
    return identifier.replace('Page1_Block', '')

def extract_coords(attributes):
    """Gets an attribute dictionary with entries
        with HPOS, VPOS, WIDTH, HEIGHT

        returns tuple of coordinates (x0, y0, x1, y1)
        x0 = HPOS
        y0 = VPOS
        x1 = WIDTH + HPOS
        y1 = HEIGHT + VPOS
    """
    x0 = int(attributes['HPOS'])
    y0 = int(attributes['VPOS'])
    x1 = int(attributes['WIDTH']) + x0
    y1 = int(attributes['HEIGHT']) + y0

    return (x0, y0, x1, y1)

def extract_text(xml_node):
    pass

def crop_image(im, anzeige):
    """Gets coordinates"""
    cropped = im.crop(anzeige['coords'])
    cropped.save(f"out/{anzeige['id']}-{anzeige['type']}.jpg")

if __name__ == '__main__':
    # Preliminaries

    # Create out folder if it not exists
    current_dir = Path.cwd()
    dirname = current_dir / 'out'

    if not dirname.exists():
        os.mkdir(dirname)

    # hardcode image file
    im = Image.open('scan.jpg')

    # Extract all textblock images
    textblocks = tree.findall(f'.//{NS}TextBlock')

    for block in textblocks:
        anzeige = process_item(block)
        anzeige['type'] = 'textblock'
        crop_image(im, anzeige)
        anzeigen.append(anzeige)

    # Extract all illustration images,
    # this does not seem to be necessary, the same ads are also
    # repesented as textblock.
    illustrations = tree.findall(f'.//{NS}Illustration')

    for illu in illustrations:
        anzeige = process_item(illu)
        anzeige['type'] = 'illustration'
        crop_image(im, anzeige)
        anzeigen.append(anzeige)