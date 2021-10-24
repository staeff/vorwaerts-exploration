from lxml import etree

svg_shell = """<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 3504 5132">
<image width="3504" height="5132" xlink:href="img/scan.jpg"></image>
{0}
</svg>
"""

ads_svg_template = """<a xlink:href="./{id}.html">
<rect x="{x}" y="{y}" fill="#fff" opacity="0" width="{width}" height="{height}"></rect>
</a>"""

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

def extract_id(identifier):
    """Gets something like Page1_Block1

    Return last digit
    """
    return identifier.replace('Page1_Block', '')

if __name__ == '__main__':
    # Preliminaries
    tree = etree.parse('data.xml')
    NS = '{http://www.loc.gov/standards/alto/ns-v2#}'

    
    # Extract all textblocks
    textblocks = tree.findall(f'.//{NS}TextBlock')

    anzeigen = ''
    # Start with 1 because thats aligns with the Id
    # we get from the xml for the img
    for i, block in enumerate(textblocks, 1):
        anzeige = process_item(block)
        anzeigen += ads_svg_template.format(**anzeige)

    svg_output = svg_shell.format(anzeigen)
    with open('overlay.svg', 'w') as outfile:
        outfile.write(svg_output)
