import sys
import json
from flask import Flask, request, jsonify
from router import router
from logger import send_log
app = Flask(__name__)

tenant = None

def match(payload, rule):
    if (
        payload['source_tenant'] == rule['source_tenant']
        and payload['destination_tenant'] == rule['destination_tenant']
    ):
        return True
    return False

@app.route('/session-authorization', methods=['POST'])
def session_authorization():
    payload = request.json

    authorized = False

    # Read rule base
    with open('rulebase.json', 'r') as f:
        rulebase = json.load(f)

        # Loop over all rules
        for rule in rulebase:

            # check rule match
            if match(payload, rule):

                authorized = True

    send_log("global", "pep", f"Authorization request from tenant {payload['source_tenant']} to tenant {payload['destination_tenant']} - result {authorized}")

    # Default to unauthorized
    return jsonify({'authorized': authorized})


if __name__ == '__main__':
    port = router["global_pep"]["port"]
    app.run(port=port)
