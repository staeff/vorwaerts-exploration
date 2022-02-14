# Exploration of the Vorwärts-Kleinanzeigen data set

## Setup

Create a virtual environment, activate it and install the requirements.

```sh
    pip install -r requirements.txt
```

## What does data_assembly.py do

* should we call it pipeline.py?

* data_assembly generates a json file, that can function as a fixture for Django, i.e.
  it can be loaded into Django easily

## Usage

For now everything is hard coded and only running with single example files.

```shell
python parse_xml.py
```

`scan.jpg` and `data.xml` need to correspond, i.e. the right image and the related
xml file need to be picked from the data set.

## Open tasks

* Allow folder with serveral image and xml files as input

* Map image file name automatically to xml file name. Everything before the file extension is the same.

* Gather important data that is available an needs to be exported

* Output information about the Ad as json

* automate the download an prep of the data (https://download.codingdavinci.de/s/7rTJnf5dP3nKJYp/download) with `make` (first step!)



## Advertisments fixture
