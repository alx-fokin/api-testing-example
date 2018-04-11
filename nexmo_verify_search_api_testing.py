import requests
import pytest
import jsonschema
from xml.etree import ElementTree

from helpers.validate_xml import validate_xml
from resources.xml_schemas import *
from resources.endpoints import *
from resources.inputs import *
from resources.json_schemas import *
from resources.messages import *


class TestVerifySearchApiJson(object):
    """This class contains only JSON format API testcases."""

    @pytest.mark.parametrize('request_id', valid_request_ids)
    def test_search_existing_requestid(self, cred, request_id):
        """Test Verify Search request with a valid request_id value.
        Should return all the information for a specific id.
        """
        resp = requests.get(search_url.format('json', cred[0], cred[1]),
                            params={'request_id': request_id})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['request_id'] == request_id
        jsonschema.validate(resp.json(), verify_search_requestid_schema)

    @pytest.mark.parametrize('request_id', invalid_request_ids)
    def test_search_nonexisting_requestid(self, cred, request_id):
        """Test Verify Search request against non-existing
        request_id value. Should fail with status code 101.
        """
        resp = requests.get(search_url.format('json', cred[0], cred[1]),
                            params={'request_id': request_id})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '101'
        assert resp.json()['error_text'] == no_response_found_msg

    @pytest.mark.parametrize('request_ids', (valid_request_ids,), ids=["list of request_ids"])
    def test_search_existing_requestids(self, cred, request_ids):
        """Test Verify Search request with several request_ids values
        Information should be retrieved for each mentioned id.
        """
        resp = requests.get(search_url.format('json', cred[0], cred[1]),
                            params={'request_ids': request_ids})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert len(resp.json()['verification_requests']) == len(request_ids)
        for request in resp.json()['verification_requests']:
            assert request['request_id'] in request_ids
        jsonschema.validate(resp.json(), verify_search_requestids_schema)

    @pytest.mark.parametrize('request_ids', (valid_request_ids,), ids=["list of request_ids"])
    def test_search_requestid_and_requestids(self, cred, request_ids):
        """Test Verify Search request with both request_id
        and request_ids values specified. Information should be retrieved
        only for the request_id value.
        """
        resp = requests.get(search_url.format('json', cred[0], cred[1]),
                            params={'request_id': request_ids[0],
                                    'request_ids': request_ids[1]})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['request_id'] == request_ids[0]
        jsonschema.validate(resp.json(), verify_search_requestid_schema)
        resp = requests.get(search_url.format('json', cred[0], cred[1]),
                            params={'request_ids': request_ids[0],
                                    'request_id': request_ids[1]})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['request_id'] == request_ids[1]
        jsonschema.validate(resp.json(), verify_search_requestid_schema)

    @pytest.mark.parametrize('request_id', (valid_request_ids,), ids=["list of request_ids"])
    def test_search_several_existing_requestid(self, cred, request_id):
        """Test Verify Search request with several request_id
        values. Information should be retrieved only for the first value.
        """
        resp = requests.get(search_url.format('json', cred[0], cred[1]),
                            params={'request_id': request_id})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['request_id'] == request_id[0]
        jsonschema.validate(resp.json(), verify_search_requestid_schema)


class TestVerifySearchApiXml(object):
    """This class contains only XML format API testcases."""

    @pytest.mark.parametrize('request_id', valid_request_ids)
    def test_search_existing_requestid(self, cred, request_id):
        """Test Verify Search request with a valid request_id value.
        Should return all the information for a specific id.
        """
        resp = requests.get(search_url.format('xml', cred[0], cred[1]),
                            params={'request_id': request_id})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        assert tree[0].tag == 'request_id' and tree[0].text == request_id
        assert validate_xml(resp.text, verify_search_requestid_xsd_schema)

    @pytest.mark.parametrize('request_id', invalid_request_ids)
    def test_search_nonexisting_requestid(self, cred, request_id):
        """Test Verify Search request against non-existing
        request_id value. Should fail with status code 101.
        """
        resp = requests.get(search_url.format('xml', cred[0], cred[1]),
                            params={'request_id': request_id})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        assert tree[1].tag == 'status' and tree[1].text == '101'
        assert tree[2].tag == 'error_text' and tree[2].text == no_response_found_msg

    @pytest.mark.parametrize('request_ids', (valid_request_ids,), ids=["list of request_ids"])
    def test_search_existing_requestids(self, cred, request_ids):
        """Test Verify Search request with several request_ids values
        Information should be retrieved for each mentioned id.
        """
        resp = requests.get(search_url.format('xml', cred[0], cred[1]),
                            params={'request_ids': request_ids})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        assert len(tree) == len(request_ids)
        for i in range(0, len(tree)):
            assert tree[2][0].tag == 'request_id' and tree[2][0].text in request_ids
        assert validate_xml(resp.text, verify_search_requestids_xsd_schema)

    @pytest.mark.parametrize('request_ids', (valid_request_ids,), ids=["list of request_ids"])
    def test_search_requestid_and_requestids(self, cred, request_ids):
        """Test Verify Search request with both request_id
        and request_ids values specified. Info should be retrieved
        only for the request_id value.
        """
        resp = requests.get(search_url.format('xml', cred[0], cred[1]),
                            params={'request_id': request_ids[0],
                                    'request_ids': request_ids[1]})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        assert tree[0].tag == 'request_id' and tree[0].text == request_ids[0]
        assert validate_xml(resp.text, verify_search_requestid_xsd_schema)
        resp = requests.get(search_url.format('xml', cred[0], cred[1]),
                            params={'request_ids': request_ids[0],
                                    'request_id': request_ids[1]})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        assert tree[0].tag == 'request_id' and tree[0].text == request_ids[1]
        assert validate_xml(resp.text, verify_search_requestid_xsd_schema)

    @pytest.mark.parametrize('request_id', (valid_request_ids,), ids=["list of request_ids"])
    def test_search_several_existing_requestid(self, cred, request_id):
        """Test Verify Search request with several request_id
        values. Information should be retrieved only for the first value.
        """
        resp = requests.get(search_url.format('xml', cred[0], cred[1]),
                            params={'request_id': request_id})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        assert tree[0].tag == 'request_id' and tree[0].text == request_id[0]
        assert validate_xml(resp.text, verify_search_requestid_xsd_schema)
