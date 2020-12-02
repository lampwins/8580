import sys
import json
from flask import Flask, request, jsonify
from router import router
from logger import send_log
app = Flask(__name__)

tenant = None
host = None

@app.route('/payload', methods=['POST'])
def pyload():
    payload = request.json

    send_log(tenant, host, f"Received messge from tenant {payload['source_tenant']} host {payload['source']}")
    return jsonify({'host': host, 'your_message': payload['message']})


if __name__ == '__main__':
    tenant = sys.argv[1]
    host = sys.argv[2]
    port = router["tenants"][tenant]["hosts"][host]["port"]
    app.run(port=port)
