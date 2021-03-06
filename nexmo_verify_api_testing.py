import requests
import pytest
from xml.etree import ElementTree

from helpers.terminate_workflow import terminate_workflow
from resources.endpoints import *
from resources.inputs import *
from resources.messages import *


class TestVerifyApiJson(object):
    """This class contains only JSON format API testcases."""

    def test_default_unsuccessful_verify_request(self, cred):
        """Test correct verification request with three
        unsuccessful attempts for verification
        """
        # make the initial request
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '0'
        assert len(resp.json()['request_id']) <= 32
        # now enter invalid verify code 3 times to terminate verification process
        # first invalid code check
        request_id = resp.json()['request_id']
        resp = requests.get(check_url.format('json', cred[0], cred[1],
                                             request_id, '00000'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '16'
        assert resp.json()['request_id'] == request_id
        assert resp.json()['error_text'] == code_does_not_match_msg
        # second invalid check
        resp = requests.get(check_url.format('json', cred[0], cred[1],
                                             request_id, '00000'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '16'
        assert resp.json()['request_id'] == request_id
        assert resp.json()['error_text'] == code_does_not_match_msg
        # third invalid check
        resp = requests.get(check_url.format('json', cred[0], cred[1],
                                             request_id, '00000'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '17'
        assert 'request_id' not in resp.json().keys()
        assert resp.json()['error_text'] == workflow_terminated_msg

    @pytest.mark.parametrize('request_id', verified_request_id)
    def test_verify_of_already_verified_request(self, cred, request_id):
        """Test Verify Check request of already verified request.
        Should fail with status code 6.
        """
        resp = requests.get(check_url.format('json', cred[0], cred[1],
                                             request_id, '0000'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '6'
        assert resp.json()['error_text'] == request_not_found_or_verified_msg.format(request_id)

    def test_verify_balance_behaviour(self, cred):
        """Test Verify Request to be free of charge if not verified.
        Balance is expected to remain the same after Verify Request
        and three unsuccessful Verify Check requests.
        """
        # check the initial balance
        resp = requests.get(balance_url.format(cred[0], cred[1]))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json;charset=UTF-8'
        start_balance = resp.json()['value']
        # now init the verification process
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        resp = requests.get(balance_url.format(cred[0], cred[1]))
        assert resp.status_code == 200
        assert start_balance == resp.json()['value']
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']
        resp = requests.get(balance_url.format(cred[0], cred[1]))
        assert resp.status_code == 200
        assert start_balance == resp.json()['value']

    def test_concurrent_verify_requests(self, cred):
        """Test concurrent Verify Request requests. Each subsequent
        request with the same number after the origin one should
        fail with status code 10.
        """
        # make the initial verification request
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        # try to repeate verification request three times
        for i in range(0, 3):
            resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                                  'TestApp', test_number))
            assert resp.status_code == 200
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json()['status'] == '10'
            assert resp.json()['request_id'] == request_id
            assert resp.json()['error_text'] == concurrent_verifications_msg
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']

    def test_concurrent_verify_requests_with_different_number_format(self, cred):
        """Test concurrent Verify Request requests. Each subsequent
        request with the same number with slightly different representation
        after the origin one should fail with status code 10.
        """
        # make the initial verification request
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        # try to repeat verification request three times
        for number in valid_numbers:
            resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                                  'TestApp', number))
            assert resp.status_code == 200
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json()['status'] == '10'
            assert resp.json()['request_id'] == request_id
            assert resp.json()['error_text'] == concurrent_verifications_msg
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']

    @pytest.mark.parametrize('number', invalid_numbers)
    def test_invalid_number_format(self, cred, number):
        """Test Verify Request with invalid phone number format.
        Each request should fail with status code 3.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '3'
        assert resp.json()['error_text'] == invalid_value_msg.format('number')

    def test_very_long_requests(self):
        """Test very long requests: around 8K and 16K size
        Should fail with HTTP response code 413 and 414 correspondingly.
        """
        api_key = api_secret = ''.join(['-' * 4000])
        resp = requests.get(verify_url.format('json', api_key, api_secret,
                                              'TestApp', test_number))
        assert resp.status_code == 413
        api_key = api_secret = ''.join(['-' * 8000])
        resp = requests.get(verify_url.format('json', api_key, api_secret,
                                              'TestApp', test_number))
        assert resp.status_code == 414

    def test_if_brand_is_missing(self, cred):
        """Test Verify request with missing brand value
        Should fail with status code 2.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              '', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '2'
        assert resp.json()['error_text'] == missing_specific_mandatory_parm_msg.format('brand')

    def test_if_number_is_missing(self, cred):
        """Test Verify request with missing number value
        Should fail with status code 2.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', ''))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '2'
        assert resp.json()['error_text'] == missing_specific_mandatory_parm_msg.format('number')

    @pytest.mark.parametrize('brand', valid_brands)
    def test_valid_brand_format(self, cred, brand):
        """Test Verify request with various valid brand values.
        Each request should be successful with status code 0.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              brand, test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']

    @pytest.mark.parametrize('brand', invalid_brands)
    def test_valid_brand_format(self, cred, brand):
        """Test Verify request with various invalid brand values.
        Each request should fail with status code 3.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              brand, test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '3'
        assert resp.json()['error_text'] == parameter_is_too_long_msg.format('brand')

    @pytest.mark.parametrize('country', valid_country)
    def test_valid_country_format(self, cred, country):
        """Test Verify request with various valid country values.
        Each request should be successful with status code 0.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number), params={'country': country})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']

    @pytest.mark.parametrize('country', invalid_country)
    def test_invalid_country_format(self, cred, country):
        """Test Verify request with various invalid country values.
        Each request should fail with status code 3.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number), params={'country': country})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '3'
        assert resp.json()['error_text'] == invalid_value_msg.format('country')

    @pytest.mark.parametrize('code_length', valid_code_length)
    def test_valid_code_length_format(self, cred, code_length):
        """Test Verify request with various valid numeric code_length values.
        Each request should be successful with status code 0.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number), params={'code_length': code_length})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']

    @pytest.mark.parametrize('code_length', invalid_numeric_code_length)
    def test_invalid_numeric_code_length_format(self, cred, code_length):
        """Test Verify request with various invalid numeric code_length values.
        Each request should fail with status code 3.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number), params={'code_length': code_length})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '3'
        assert resp.json()['error_text'] == allowed_code_length_values_msg

    @pytest.mark.parametrize('code_length', invalid_nonnumeric_code_length)
    def test_invalid_nonnumeric_code_length_format(self, cred, code_length):
        """Test Verify request with various invalid non-numeric code_length values.
        Each request should fail with status code 3.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number), params={'code_length': code_length})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '3'
        assert resp.json()['error_text'] == invalid_value_msg.format('code_length')

    @pytest.mark.parametrize('sender_id', valid_sender_id)
    def test_valid_code_length_format(self, cred, sender_id):
        """Test Verify request with various valid sender_id values.
        Each request should be successful with status code 0.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number), params={'sender_id': sender_id})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']

    @pytest.mark.parametrize('sender_id', invalid_sender_id)
    def test_invalid_numeric_code_length_format(self, cred, sender_id):
        """Test Verify request with improper sender_id value.
        Each request should fail with status code 3.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number), params={'sender_id': sender_id})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '3'
        assert resp.json()['error_text'] == parameter_is_too_long_msg.format('sender_id')

    @pytest.mark.parametrize('language', invalid_language)
    def test_invalid_numeric_code_length_format(self, cred, language):
        """Test Verify request with improper language values.
        Each request should fail with status code 3.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number), params={'lg': language})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '3'
        assert resp.json()['error_text'] == invalid_value_msg.format('lg')

    def test_invalid_verify_post_request(self, cred):
        """Test restricted POST request for Verify API.
        Should fail with HTTP response code 400.
        """
        resp = requests.post(verify_url.format('json', cred[0], cred[1],
                                               'TestApp', test_number))
        assert resp.status_code == 400

    def test_invalid_verify_put_request(self, cred):
        """Test restricted PUT request for Verify API.
        Should fail with HTTP response code 403.
        """
        resp = requests.put(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 403

    def test_invalid_verify_patch_request(self, cred):
        """Test restricted PATCH request for Verify API.
        Should fail with HTTP response code 403.
        """
        resp = requests.patch(verify_url.format('json', cred[0], cred[1],
                                                'TestApp', test_number))
        assert resp.status_code == 403

    def test_invalid_verify_delete_request(self, cred):
        """Test restricted DELETE request for Verify API.
        Should fail with HTTP response code 403.
        """
        resp = requests.delete(verify_url.format('json', cred[0], cred[1],
                                                 'TestApp', test_number))
        assert resp.status_code == 403

    def test_empty_code_for_verification(self, cred):
        """Test Verify Check request with empty code.
        Should fail with status code 2.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        resp = requests.get(check_url.format('json', cred[0], cred[1],
                                             request_id, ''))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '2'
        assert resp.json()['error_text'] == missing_specific_mandatory_parm_msg.format('code')
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']

    @pytest.mark.parametrize('code', invalid_code)
    def test_invalid_format_code_for_verification(self, cred, code):
        """Test Verify Check request with various invalid non-numeric
        code values. Each one should fail with status code 3.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        resp = requests.get(check_url.format('json', cred[0], cred[1],
                                             request_id, code))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '3'
        assert resp.json()['error_text'] == code_invalid_characters_msg
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']


class TestVerifyApiXml(object):
    """This class contains only XML format API testcases."""

    def test_default_unsuccessful_verify_request(self, cred):
        """Test correct verification request with three
        unsuccessful attempts for verification
        """
        # make the initial request
        resp = requests.get(verify_url.format('xml', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        assert tree[0].tag == 'request_id' and len(tree[0].text) <= 32
        assert tree[1].tag == 'status' and tree[1].text == '0'
        # now enter invalid verify code 3 times to terminate verification process
        # first invalid code check
        request_id = tree[0].text
        resp = requests.get(check_url.format('xml', cred[0], cred[1],
                                             request_id, '00000'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        assert tree[0].tag == 'request_id' and tree[0].text == request_id
        assert tree[1].tag == 'status' and tree[1].text == '16'
        assert tree[2].tag == 'error_text' and tree[2].text == code_does_not_match_msg
        # second invalid check
        resp = requests.get(check_url.format('xml', cred[0], cred[1],
                                             request_id, '00000'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        assert tree[0].tag == 'request_id' and tree[0].text == request_id
        assert tree[1].tag == 'status' and tree[1].text == '16'
        assert tree[2].tag == 'error_text' and tree[2].text == code_does_not_match_msg
        # third invalid check
        resp = requests.get(check_url.format('xml', cred[0], cred[1],
                                             request_id, '00000'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'text/plain'
        assert resp.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')
        tree = ElementTree.fromstring(resp.text)
        # assert 'request_id' not in [child.tag for child in tree]
        assert tree[1].tag == 'status' and tree[1].text == '17'
        assert tree[2].tag == 'error_text' and tree[2].text == workflow_terminated_msg
