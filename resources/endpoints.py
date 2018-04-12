"""This module contains set of api endpoints templates."""

api_base_url = 'https://api.nexmo.com/'
rest_base_url = 'https://rest.nexmo.com/'

verify_url = api_base_url + 'verify/{}?api_key={}&api_secret={}&brand={}&number={}'
check_url = api_base_url + 'verify/check/{}?api_key={}&api_secret={}&request_id={}&code={}'
control_url = api_base_url + 'verify/control/{}?api_key={}&api_secret={}&request_id={}&cmd={}'
search_url = api_base_url + 'verify/search/{}?api_key={}&api_secret={}'
balance_url = rest_base_url + 'account/get-balance?api_key={}&api_secret={}'
verify_url_without_apikey = api_base_url + 'verify/{}?api_secret={}&brand={}&number={}'
verify_url_without_apisecret = api_base_url + 'verify/{}?api_key={}&brand={}&number={}'
number_insight_url = api_base_url + 'ni/{}/{}?api_key={}&api_secret={}&number={}'
async_number_insight_url = api_base_url + 'ni/advanced/async/{}?api_key={}&api_secret={}&number={}&callback={}'

insight_webhook_url = 'Replace with your webhoor url, for example, use local flask server and ngrok'
