import io
from lxml import etree


def validate_xml(xmldoc, xsdschema):
    """This is helper function for xml response validation
    using xsd schema and lxml library.

    Args:
        xmldoc: XML document itself.
        xsdschema: corresponding XSD schema for validation.

    Returns:
        Boolean validation result.
    """
    xmlschema_doc = etree.parse(io.StringIO(xsdschema))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    valid = io.StringIO(xmldoc[len('<?xml version="1.0" encoding="UTF-8"?>'):])
    doc = etree.parse(valid)
    return xmlschema.validate(doc)
