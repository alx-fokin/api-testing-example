import requests
import io
from lxml import etree
from constants import check_url


def terminate_workflow(api_key, api_secret, request_id):
    """This is helper function just to terminate initiated
    verification process by entering wrong code three times
    in a row.

    Args:
        api_key: credentials for api invocation.
        api_secret: credentials for api invocation.
        request_id: id of initiated verification process.

    Returns:
        Last response object.
    """
    resp = 0
    for i in range(0, 3):
        resp = requests.get(check_url.format('json', api_key, api_secret,
                                             request_id, '00000'))
    return resp


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
