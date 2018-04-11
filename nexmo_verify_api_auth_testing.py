import requests
import pytest

from resources.endpoints import *
from resources.inputs import *
from resources.messages import *


class TestVerifyApiAuthJson(object):
    """This class contains only JSON format API testcases."""

    def test_empty_apikey(self, cred):
        """Test Verify Request with empty api_key value and
        without api_key parm in the query string at all.
        Each request should fail with status code 2.
        """
        resp = requests.get(verify_url.format('json', '', cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '2'
        assert resp.json()['error_text'] == missing_apikey_msg
        resp = requests.get(verify_url_without_apikey.format('json', cred[1],
                                                             'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '2'
        assert resp.json()['error_text'] == missing_apikey_msg

    def test_empty_apisecret(self, cred):
        """Test Verify Request with empty api_secret value and
        without api_secret parm in the query string at all.
        Each request should fail with status code 2.
        """
        resp = requests.get(verify_url.format('json', cred[0], '',
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '2'
        assert resp.json()['error_text'] == missing_mandatory_parms_msg
        resp = requests.get(verify_url_without_apisecret.format('json', cred[0],
                                                                'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '2'
        assert resp.json()['error_text'] == missing_mandatory_parms_msg

    def test_swapped_apikey_and_apisecret(self, cred):
        """Test Verify Request with swapped values of api_secret
        an api_key values. Should fail with status code 4.
        """
        resp = requests.get(verify_url.format('json', cred[1], cred[0],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '4'
        assert resp.json()['error_text'] == bad_credentials_msg

    @pytest.mark.parametrize('api_key', invalid_creds)
    @pytest.mark.parametrize('api_secret', invalid_creds)
    def test_invalid_credentials(self, api_key, api_secret):
        """Test Verify Request with various invalid credentials
        Each request should fail with status code 4.
        """
        resp = requests.get(verify_url.format('json', api_key, api_secret,
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '4'
        assert resp.json()['error_text'] == bad_credentials_msg
