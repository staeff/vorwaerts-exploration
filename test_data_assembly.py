import pytest
from lxml import etree
from data_assembly import generate_page_dict
from data_assembly import generate_page_fields
from data_assembly import get_page_coords
from data_assembly import get_adv_coords
from data_assembly import get_adv_text
from data_assembly import extract_id
from data_assembly import NS

XML_PAGE_COORDS = """
<alto xmlns="http://www.loc.gov/standards/alto/ns-v2#">
  <Page ID="Page1" PHYSICAL_IMG_NR="1" HEIGHT="5132" WIDTH="3504"/>
</alto>
"""

XML_TextLine_CONTENT = """
<alto xmlns="http://www.loc.gov/standards/alto/ns-v2#">
  <TextLine>
    <String CONTENT="Andreas,"/>
    <String CONTENT="Alexander" SUBS_TYPE="HypPart1" SUBS_CONTENT="Alexanderstraße" />
  </TextLine>
  <TextLine>
    <String CONTENT="straße" SUBS_TYPE="HypPart2" SUBS_CONTENT="Alexanderstraße" />
  </TextLine>
</alto>
"""

def test_generate_page_dict():
    i = 10

    result = generate_page_dict(i)

    assert len(result) == 2
    assert result['pk'] == 10
    assert result['model'] == "vorwaerts.newspaperpage"

def test_generate_page_fields():
    file_id_string = 'vw-1891-12-20-298-012'

    fields = generate_page_fields(file_id_string)

    assert len(fields) == 4
    assert fields['file_id'] == "vw-1891-12-20-298-012"
    assert fields["publish_date"] == "1891-12-20"
    assert fields["issue_number"] == 298
    assert fields["page_number"] == 12

def test_get_page_coords():
    tree = etree.fromstring(XML_PAGE_COORDS)

    result = get_page_coords(tree)
    assert len(result) == 2
    assert result['height'] == "5132"
    assert result['width'] == "3504"

def test_get_adv_text():
    tree = etree.fromstring(XML_TextLine_CONTENT)

    result = get_adv_text(tree, NS)
    assert result == 'Andreas, Alexanderstraße'

def test_get_adv_coords():
    item_attrs = dict(HPOS='100',VPOS='200',WIDTH='22',HEIGHT='12')

    result = get_adv_coords(item_attrs)

    assert len(result) == 4
    assert result['x'] == 100
    assert result['y'] == 200
    assert result['width'] == 22
    assert result['height'] == 12

def test_extract_id():
    block_id_string = 'Page1_Block25'

    result = extract_id(block_id_string)

    assert result == '25'
