import requests
import time
import pytest

from helpers.terminate_workflow import terminate_workflow
from resources.endpoints import *
from resources.inputs import *
from resources.messages import *


class TestVerifyApiJson(object):
    """This class contains only JSON format API testcases."""

    def test_cancel_of_default_verify_request(self, cred):
        """Test Verify Cancel request full cycle.
        Before 30 sec. passed should fail with status code 19,
        After 30 sec. passed should be successful,
        Next cancel request should fail with status code 6.
        """
        # make the initial request
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '0'
        assert len(resp.json()['request_id']) <= 32
        request_id = resp.json()['request_id']
        # perform cancel before 30 seconds limit
        time.sleep(10)
        resp = requests.get(control_url.format('json', cred[0], cred[1],
                                               request_id, 'cancel'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '19'
        assert resp.json()['error_text'] == request_cannot_be_cancelled_msg.format(request_id)
        # perform cancel before 30 seconds limit
        time.sleep(20)
        resp = requests.get(control_url.format('json', cred[0], cred[1],
                                               request_id, 'cancel'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '0'
        assert resp.json()['command'] == 'cancel'
        assert 'error_text' not in resp.json().keys()
        # try to cancel already cancelled request
        resp = requests.get(control_url.format('json', cred[0], cred[1],
                                               request_id, 'cancel'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '6'
        assert resp.json()['error_text'] == request_not_exist_or_active_msg.format(request_id)

    def test_trigger_next_event_three_times(self, cred):
        """Test Verify Control trigger_next_event request.
        Should work successfully two times, after that should
        fail with status code 19.
        """
        # make the initial request
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        # make two trigger_next_event requests with small pauses
        for i in range(0, 2):
            time.sleep(10)
            resp = requests.get(control_url.format('json', cred[0], cred[1],
                                                   request_id, 'trigger_next_event'))
            assert resp.status_code == 200
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json()['status'] == '0'
            assert resp.json()['command'] == 'trigger_next_event'
        # perform third trigger_next_event request
        time.sleep(10)
        resp = requests.get(control_url.format('json', cred[0], cred[1],
                                               request_id, 'trigger_next_event'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '19'
        assert resp.json()['error_text'] == no_more_event_to_execute_msg.format(request_id)
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']

    @pytest.mark.parametrize('cmd', invalid_cmd)
    def test_invalid_cmd_for_verify_control(self, cred, cmd):
        """Test Verify Control request with some invalid cmd values.
        Each one should fail with status code 3.
        """
        resp = requests.get(verify_url.format('json', cred[0], cred[1],
                                              'TestApp', test_number))
        assert resp.status_code == 200
        assert resp.json()['status'] == '0'
        request_id = resp.json()['request_id']
        resp = requests.get(control_url.format('json', cred[0], cred[1],
                                               request_id, cmd))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == '3'
        assert resp.json()['error_text'] == invalid_parameter_found_msg.format('cmd')
        # terminate verification process
        assert 'Workflow terminated' in \
               terminate_workflow(cred[0], cred[1], request_id).json()['error_text']
