from pathlib import Path
from lxml import etree
import json

NS = '{http://www.loc.gov/standards/alto/ns-v2#}'

"""
[{
    "model": "vorwaerts.newspaperpage",
    "pk": 2,
    "fields": {
        "image_name": "vw-1891-12-20-298-012.jpg"
    }
}, ...]

Sonntagsausgaben des „Vorwärts“ umfassen.
Die Dateibenennung setzt sich zusammen aus dem Kürzel für die Zeitung (vw),
dem Datum, der Ausgabennummer sowie der Seitenzahl:
vw-jjjj-mm-tt-Ausgabennummer-Seitenzahl.
Die Ausgabennummer kann ein- oder zweistellig sein.
Die Seitenzahl ist dreistellig.
"""

def generate_page_data(i, file_id_string):
    """Generate a dictionary with that represents a page instance
    """
    _, year, month, day, issue_number, page_number = file_id_string.split('-')
    fields={}
    page = dict(
        model="vorwaerts.newspaperpage",
        pk = i
        )
    fields["image_name"] = f"{file_id_string}.jpg"
    fields["publish_date"] = f"{year}-{month}-{day}"
    fields["issue_number"] = int(issue_number)
    fields["page_number"] = int(page_number)
    page["fields"] = fields
    return page

def extract_coords(item_attrs):
    """Gets a block node, either TextBlock
        or Illustration and returns a
        dictionary with its attributes
    """
    anzeige = {}
    anzeige['x'] = int(item_attrs['HPOS'])
    anzeige['y'] = int(item_attrs['VPOS'])
    anzeige['width'] = int(item_attrs['WIDTH'])
    anzeige['height'] = int(item_attrs['HEIGHT'])
    return anzeige

def extract_id(block_id_string):
    """Gets something block id string like Page1_Block1
    and returns the remaining number when Page1_Block
    is removed.
    """
    return block_id_string.replace('Page1_Block', '')


if __name__ == '__main__':
    cwd = Path('.')
    xml_files = list(cwd.glob('xml/*.xml'))
    fixture = []
    anzeigen = []

    for i, xml_file in enumerate(xml_files):
        # id string is filename w/o extensions
        file_id_string = xml_file.stem

        # Generate dict with page
        page_data = generate_page_data(i, file_id_string)
        fixture.append(page_data)

        # Parse data into etree
        tree = etree.parse(str(xml_file))
        # Extract all textblocks elements
        textblocks = tree.findall(f'.//{NS}TextBlock')


        for block in textblocks:
            # Assign nodes attributes dict to a var
            item_attrs = block.attrib
            anzeige = extract_coords(item_attrs)
            block_id_string = item_attrs['ID']
            anzeige['id'] = extract_id(block_id_string, file_id_string)
            anzeigen.append(anzeige)

    # Write pages data to fixture file
    with open("pages.json", "w") as outfile:
        json.dump(fixture, outfile)

    # Write advertisement data fo fixture
    with open("advertisments.json", "w") as outfile:
        json.dump(anzeigen, outfile)
