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

def process_item(item):
    """Gets a block node, either TextBlock
        or Illustration and returns a
        dictionary with its attributes
    """
    attributes = item.attrib
    anzeige = {}
    anzeige['id'] = extract_id(attributes['ID'])
    anzeige['x'] = int(attributes['HPOS'])
    anzeige['y'] = int(attributes['VPOS'])
    anzeige['width'] = int(attributes['WIDTH'])
    anzeige['height'] = int(attributes['HEIGHT'])
    return anzeige

def extract_id(identifier, xml_file):
    """Gets something like Page1_Block1

    Return last digit
    """
    text_nr = identifier.replace('Page1_Block', '')
    return f"{xml_file.stem}-{text_nr}"

if __name__ == '__main__':
    cwd = Path('.')
    xml_files = list(cwd.glob('xml/*.xml'))
    fixture = []

    for i, xml_file in enumerate(xml_files):
        file_id_string = xml_file.stem
        page_data = generate_page_data(i, xml_file)
        fixture.append(page_data)

    with open("pages.json", "w") as outfile:
        json.dump(fixture, outfile)

    for xml_file in enumerate(xml_files):
        tree = etree.parse(xml_file)

        # Extract all textblocks
        textblocks = tree.findall(f'.//{NS}TextBlock')

        anzeigen = ''
        # Start with 1 because thats aligns with the Id
        # we get from the xml for the img
        for i, block in enumerate(textblocks, 1):
            anzeige = process_item(block)


        svg_output = svg_shell.format(anzeigen)
        with open('overlay.svg', 'w') as outfile:
            outfile.write(svg_output)
