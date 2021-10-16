from pathlib import Path

cwd = Path('.')
xml_files = list(cwd.glob('xml/*.xml'))

for xml_file in xml_files:
     print(xml_file.stem)
