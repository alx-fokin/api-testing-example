import requests
from resources.endpoints import check_url


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
