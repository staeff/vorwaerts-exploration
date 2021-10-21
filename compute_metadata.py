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

Sonntagsausgaben des „Vorwärts“ umfassen.
Die Dateibenennung setzt sich zusammen aus dem Kürzel für die Zeitung (vw),
dem Datum, der Ausgabennummer sowie der Seitenzahl:
vw-jjjj-mm-tt-Ausgabennummer-Seitenzahl.

Die Ausgabennummer kann ein- oder zweistellig sein.
Die Seitenzahl ist dreistellig.
"""

if __name__ == '__main__':
    cwd = Path('.')
    xml_files = list(cwd.glob('xml/*.xml'))

    fixture = []

    for i, xml_file in enumerate(xml_files):
        file_id = xml_file.stem
        _, year, month, day, issue_number, page_number = file_id.split('-')
        fields={}
        page = dict(
            model="vorwaerts.newspaperpage",
            pk = i
            )
        fields["image_name"] = f"{file_id}.jpg"
        fields["publish_date"] = f"{year}-{month}-{day}"
        fields["issue_number"] = int(issue_number)
        fields["page_number"] = int(page_number)
        page["fields"] = fields
        fixture.append(page)

    with open("pages.json", "w") as outfile:
        json.dump(fixture, outfile)
