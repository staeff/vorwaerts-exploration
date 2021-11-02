from pathlib import Path
from lxml import etree
import json

NS = "{http://www.loc.gov/standards/alto/ns-v2#}"

def generate_page_dict(i):
    """Generate a dictionary with that represents a minimal page instance"""
    return dict(model="vorwaerts.newspaperpage", pk=i)

def generate_page_fields(file_id_string):
    _, year, month, day, issue_number, page_number = file_id_string.split("-")
    fields = {}
    fields["file_id"] = file_id_string
    fields["publish_date"] = f"{year}-{month}-{day}"
    fields["issue_number"] = int(issue_number)
    fields["page_number"] = int(page_number)
    return fields

def get_page_coords(tree, NS):
    page_elem = tree.find(f".//{NS}Page")
    coords = {}
    coords['height'] = page_elem.attrib['HEIGHT']
    coords['width'] = page_elem.attrib['WIDTH']
    return coords

def get_adv_coords(item_attrs):
    """Gets a block node, either TextBlock
    or Illustration and returns a
    dictionary with its attributes
    """
    anzeige = {}
    anzeige["x"] = int(item_attrs["HPOS"])
    anzeige["y"] = int(item_attrs["VPOS"])
    anzeige["width"] = int(item_attrs["WIDTH"])
    anzeige["height"] = int(item_attrs["HEIGHT"])
    return anzeige

def get_adv_text(xml_node, NS):
    """copied from alto-tools

    https://github.com/cneud/alto-tools
    """
    text = ''

    # Use XPath here to simplify?
    for lines in xml_node.findall(f'.//{NS}TextLine'):
        for line in lines.findall(f'.//{NS}String'):
            # Check if there are no hyphenated words
            # We dont want to have the CONTENT of nodes, that have the
            # Attributes SUBS_CONTENT of SUBS_TYPE
            if ('SUBS_CONTENT' not in line.attrib and 'SUBS_TYPE' not in line.attrib):
                text += f"{line.attrib.get('CONTENT')} "
            else:
                # If a node has the Attribut SUBS_TYPE we check if
                # it is HypPart1 and add its SUBCONTENT_VALUE to text/
                if ('HypPart1' in line.attrib.get('SUBS_TYPE')):
                    text += f"{line.attrib.get('SUBS_CONTENT')} "
                    # This doesnt do shit!
                    if ('HypPart2' in line.attrib.get('SUBS_TYPE')):
                        pass
    return text.strip()

def extract_id(block_id_string):
    """Gets something block id string like Page1_Block1
    and returns the remaining number when Page1_Block
    is removed.
    """
    return block_id_string.replace("Page1_Block", "")


if __name__ == "__main__":
    cwd = Path(".")
    xml_files = sorted(list(cwd.glob("xml/*.xml")))
    fixture = []
    anzeigen = []

    for i, xml_file in enumerate(xml_files):
        # parse XML file into etree
        tree = etree.parse(str(xml_file))

        # id string is filename w/o extensions
        file_id_string = xml_file.stem

        # Generate dict with page
        page_dict = generate_page_dict(i)
        fields_dict = generate_page_fields(file_id_string)
        coords_dict = get_page_coords(tree, NS)
        # Merge fields and coords dict
        fields = {**fields_dict, **coords_dict}
        page_dict['fields'] = fields
        fixture.append(page_dict)

        # Extract all textblocks elements
        textblocks = tree.findall(f".//{NS}TextBlock")

        for block in textblocks:
            # Assign nodes attributes dict to a var
            item_attrs = block.attrib
            anzeige = get_adv_coords(item_attrs)
            block_id_string = item_attrs["ID"]
            anzeige["block_id"] = extract_id(block_id_string)
            anzeige["file_id"] = file_id_string
            anzeige["text"] = get_adv_text(block)
            anzeige["newspaper_page"] = i
            anzeigen.append(anzeige)

    # Write pages data to fixture file
    with open("pages.json", "w") as outfile:
        json.dump(fixture, outfile)

    # # Write advertisement data fo fixture
    # with open("advertisments.json", "w") as outfile:
    #     json.dump(anzeigen, outfile)
