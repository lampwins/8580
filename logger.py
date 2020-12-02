import sys
import json
from flask import Flask, request, jsonify
from router import router
import requests
app = Flask(__name__)

def send_log(tenant, host, message):
    _host = router['logger']['host']
    _port = router['logger']['port']

    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }

    payload = {
        "tenant": tenant,
        "host": host,
        "message": message
    }

    response = requests.post(
        f"http://{_host}:{_port}/log",
        headers=headers,
        json=payload
    )

@app.route('/log', methods=['POST'])
def log():
    payload = request.json
    
    with open("log.txt", "w+") as f:
        f.write(f"TENANT {payload['tenant'].upper()}: {payload['host'].upper()}: {payload['message']}\n")

    return {}


if __name__ == '__main__':
    port = router["logger"]["port"]
    app.run(port=port)