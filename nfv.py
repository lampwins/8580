import sys
import json
import requests
from flask import Flask, request, jsonify
from router import router
from logger import send_log
app = Flask(__name__)

tenant = None


@app.route('/nfv', methods=['POST'])
def nfv():
    payload = request.json

    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }

    banned_words = [
        "'or 1=1;"
    ]

    if payload['message'] in banned_words:
        send_log(tenant, "nfv", "Bad actor, dropping traffic!")
        return jsonify({"authorized": False})


    send_log(tenant, "nfv", f"Passed inspection, forwarding to host {payload['destination']}")

    host = router['tenants'][payload['destination_tenant']]["hosts"][payload['destination']]['host']
    port = router['tenants'][payload['destination_tenant']]["hosts"][payload['destination']]['port']

    response = requests.post(
        f"http://{host}:{port}/payload",
        headers=headers,
        json=payload
    )

    return response.json()



if __name__ == '__main__':
    tenant = sys.argv[1]
    port = router["tenants"][tenant]["nfv"]["port"]
    app.run(port=port)
