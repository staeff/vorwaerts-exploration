from pathlib import Path
import json

"""
[{
    "model": "vorwaerts.newspaperpage",
    "pk": 2,
    "fields": {
        "image_name": "vw-1891-12-20-298-012.jpg"
    }
}, ...]
"""



if __name__ == '__main__':
    cwd = Path('.')
    xml_files = list(cwd.glob('xml/*.xml'))

    fixture = []

    for i, xml_file in enumerate(xml_files):
        page = dict(
                model="vorwaerts.newspaperpage",
                fields={}
                )
        page["pk"] = i
        page["fields"]["image_name"] = f"{xml_file.stem}.jpg"
        fixture.append(page)

    with open("pages.json", "w") as outfile:
        json.dump(fixture, outfile)
