import csv
import shutil

with open('vorwaerts-metadaten.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)

csvReader
with open('vorwaerts-metadaten.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        if csvReader.line_num == 1:
            continue
        else:
            new_file_name = '{}.xml'.format(row[5].split('.')[0])
            shutil.move(row[6], new_file_name)
