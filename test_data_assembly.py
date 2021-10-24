import pytest
from data_assembly import generate_page_data
from data_assembly import extract_coords
from data_assembly import extract_id


def test_generate_page_data():
    i = 10
    file_id_string = 'vw-1891-12-20-298-012'

    result = generate_page_data(i, file_id_string)
    fields = result['fields']

    assert len(result) == 3
    assert result['pk'] == 10
    assert result['model'] == "vorwaerts.newspaperpage"
    assert len(fields) == 4
    assert fields['file_id'] == "vw-1891-12-20-298-012"
    assert fields["publish_date"] == "1891-12-20"
    assert fields["issue_number"] == 298
    assert fields["page_number"] == 12

def test_extract_coords():
    item_attrs = dict(HPOS='100',VPOS='200',WIDTH='22',HEIGHT='12')

    result = extract_coords(item_attrs)

    assert len(result) == 4
    assert result['x'] == 100
    assert result['y'] == 200
    assert result['width'] == 22
    assert result['height'] == 12

def test_extract_id():
    block_id_string = 'Page1_Block25'

    result = extract_id(block_id_string)

    assert result == '25'
