from flask import Flask, request, abort, jsonify

app = Flask(__name__)

last_requests = []


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def webhook_for_async_number_insight():
    """This method serves as a callback function (webhook) for
    Nexmo Number Insight Advanced Async API. The easiest way to use
    it is to run locally and then use 'ngrok' tool to expose your local
    server behind NATs and firewalls to the public internet access.
    """
    global last_requests
    if request.method == 'POST':
        last_requests.append(request.json)
        return jsonify({'Status': 'Success'}), 200
    elif request.method == 'GET':
        if last_requests:
            return jsonify(last_requests), 200
        else:
            return jsonify({'Status': 'No previous request'}), 200
    elif request.method == 'DELETE':
        del last_requests[:]
        return jsonify({'Status': 'Success'}), 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run()
