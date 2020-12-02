import sys
import json
import requests
from flask import Flask, request, jsonify
from router import router
from logger import send_log
app = Flask(__name__)

tenant = None

def rulebase_lookup(payload):
    # Read rule base
    with open('rulebase.json', 'r') as f:
        rulebase = json.load(f)

        # Loop over all rules
        for rule in rulebase:

            # check rule match
            if match(payload, rule):

                if rule['destination_tenant'] == tenant:
                    if rule['nfv']:
                        method = 'nfv'
                    else:
                        method = 'direct'
                else:
                    method = 'route'
    
                return True, method

        return False, None

def match(payload, rule):
    if (
        payload['source_tenant'] == rule['source_tenant']
        and payload['source'] == rule['source']
        and payload['destination_tenant'] == rule['destination_tenant']
        and payload['destination'] == rule['destination']
    ):
        return True
    return False

@app.route('/session-authorization', methods=['POST'])
def session_authorization():
    payload = request.json

    authorized, method = rulebase_lookup(request.json)

    send_log(tenant, "pep", f"Authorization request from tenant {payload['source_tenant']} host {payload['source']} to tenant {payload['destination_tenant']} host {payload['destination']} - result {authorized}")

    # Default to unauthorized
    return jsonify({'authorized': authorized, 'method': method})


@app.route('/proxy', methods=['POST'])
def proxy():
    payload = request.json

    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }

    if payload['destination_tenant'] == tenant:
        # inbound to the tenant, make the direct connection after rule match

        authorized, method = rulebase_lookup(request.json)
        if not authorized:
            return jsonify({'authorized': False})

        send_log(tenant, "router", f"Authorized, forwarding to host {payload['destination']}")

        host = router['tenants'][payload['destination_tenant']]["hosts"][payload['destination']]['host']
        port = router['tenants'][payload['destination_tenant']]["hosts"][payload['destination']]['port']

        response = requests.post(
            f"http://{host}:{port}/payload",
            headers=headers,
            json=payload
        )

        return response.json()

    else:
        # outbound from the tenant, query the global pep and make the request to the other pep

        send_log(tenant, 'router', "Making session authorization request to global PEP")

        host = router['global_pep']['host']
        port = router['global_pep']['port']

        # query the global pep
        response = requests.post(
            f"http://{host}:{port}/session-authorization",
            headers=headers,
            json={
                "source_tenant": payload['source_tenant'],
                "destination_tenant": payload['destination_tenant'],
            }
        )

        if not response.json()['authorized']:
            return jsonify({'authorized': False})

        send_log(tenant, "router", f"Authorized, forwarding to tenant {payload['destination_tenant']} router")

        # send request to other pep
        host = router['tenants'][payload['destination_tenant']]["pep"]['host']
        port = router['tenants'][payload['destination_tenant']]["pep"]['port']
        response = requests.post(
            f"http://{host}:{port}/proxy",
            headers=headers,
            json=payload
        )

        return response.json()


if __name__ == '__main__':
    tenant = sys.argv[1]
    port = router["tenants"][tenant]["pep"]["port"]
    app.run(port=port)
