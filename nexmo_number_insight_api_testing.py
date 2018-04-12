import requests
import pytest
import time
import math

from resources.endpoints import insight_webhook_url, async_number_insight_url, \
    balance_url, number_insight_url
from resources.inputs import valid_numbers_for_insight_api, test_number
from resources.prices import insight_cost_standard, insight_cost_advanced


class TestNumberInsightApiJson(object):
    """This class contains only JSON format API testcases."""

    @pytest.mark.parametrize('numbers', (valid_numbers_for_insight_api,), ids=["list_of_valid_numbers"])
    def test_advanced_async_request(self, cred, numbers):
        """Test Async Advanced Number Insight API request. Run
        request several times, each request should return some basic info:
        request_id, number, remaining_balance, request_price, status.
        Thorough information about each number will be send to the provided
        callback API (webhook). After that all the information should be
        successfully retrieved using GET request towards our webhook.
        """
        # at first, clear the list of requests on our webhook server
        resp = requests.delete(insight_webhook_url)
        assert resp.status_code == 200
        assert resp.json()['Status'] == 'Success'
        # submit requests for all given numbers
        submitted_requests = []
        for number in numbers:
            resp = requests.get(async_number_insight_url.format('json', cred[0],
                                                                cred[1], number, insight_webhook_url))
            assert resp.status_code == 200
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json()['status'] == 0
            assert resp.json()['request_price'] == '0.03000000'
            assert resp.json()['number'] == number
            assert 'remaining_balance' in resp.json().keys()
            submitted_requests.append(resp.json()['request_id'])
        # make a small delay for all the requests to be served
        time.sleep(5)
        # now make GET request to our webhook API and check all requests
        resp = requests.get(insight_webhook_url)
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert sorted(submitted_requests) == sorted([request['request_id'] for request in resp.json()])

    def test_number_insight_balance_behaviour(self, cred):
        """Test all four versions of Number Insight API (Basic, Standard,
        Advanced, Advanced Async) in terms of pricing. First one should be free,
        second costs 0.005 EUR, third and fourth cost 0.03 EUR.
        """
        # check the initial balance
        resp = requests.get(balance_url.format(cred[0], cred[1]))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json;charset=UTF-8'
        current_balance = resp.json()['value']
        # now make Basic request
        resp = requests.get(number_insight_url.format('basic', 'json', cred[0], cred[1], test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == 0
        assert current_balance == requests.get(balance_url.format(cred[0], cred[1])).json()['value']
        # now make Standard request
        resp = requests.get(number_insight_url.format('standard', 'json', cred[0], cred[1], test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == 0
        new_balance = requests.get(balance_url.format(cred[0], cred[1])).json()['value']
        assert math.isclose(current_balance, new_balance + insight_cost_standard, abs_tol=0.000001)
        current_balance = new_balance
        # now make Advanced request
        resp = requests.get(number_insight_url.format('advanced', 'json', cred[0], cred[1], test_number))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == 0
        new_balance = requests.get(balance_url.format(cred[0], cred[1])).json()['value']
        assert math.isclose(current_balance, new_balance + insight_cost_advanced, abs_tol=0.000001)
        current_balance = new_balance
        # now make Advanced Async
        resp = requests.get(async_number_insight_url.format('json', cred[0],
                                                            cred[1], test_number, insight_webhook_url))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == 0
        new_balance = float(resp.json()['remaining_balance'])
        assert new_balance == requests.get(balance_url.format(cred[0], cred[1])).json()['value']
        assert math.isclose(current_balance, new_balance + insight_cost_advanced, abs_tol=0.000001)

    @pytest.mark.parametrize('number', valid_numbers_for_insight_api)
    def test_advanced_request_with_cname_for_nonus_numbers(self, cred, number):
        """Test Advanced Number Insight API with cname=true parameter
        against non-US numbers: information about caller should not
        be provided.
        """
        resp = requests.get(number_insight_url.format('advanced', 'json', cred[0],
                                                      cred[1], number), params={'cname': 'true'})
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json()['status'] == 0
        assert all(field not in resp.json().keys() for field in
                   ('first_name', 'last_name', 'caller_name', 'caller_type'))
