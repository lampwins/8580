#!/usr/bin/env python
import requests
import sys
from router import router
from logger import send_log


def main(source_tenant, source, destination_tenant, destination, message):
    send_log(source_tenant, source, "-"*75)
    send_log(source_tenant, source, f"Starting transmission to tenant {destination_tenant} host {destination} with message {message}")
    headers = {
        "content-type": "application/json",
        "accept": "application/json"
    }

    host = router['tenants'][source_tenant]["pep"]['host']
    port = router['tenants'][source_tenant]["pep"]['port']

    payload = {
        "source_tenant": source_tenant,
        "source": source,
        "destination_tenant": destination_tenant,
        "destination": destination,
        "message": message
    }

    send_log(source_tenant, source, "Making session authorization request to PEP")

    response = requests.post(
        f"http://{host}:{port}/session-authorization",
        headers=headers,
        json=payload
    )

    data = response.json()

    if not data['authorized']:
        send_log(source_tenant, source, f"Not authorized to connect to tenant {destination_tenant} host {destination}")

    elif data['method'] == 'direct':
        send_log(source_tenant, source, "Authorized via direct connection")
        send_log(source_tenant, source, f"Opening session to host {destination}")

        host = router['tenants'][destination_tenant]["hosts"][destination]['host']
        port = router['tenants'][destination_tenant]["hosts"][destination]['port']

        # make direct request
        response = requests.post(
            f"http://{host}:{port}/payload",
            headers=headers,
            json=payload
        )

        if response.json().get('your_message'):
            send_log(source_tenant, source, f"Received successful response from host {destination}")
        else:
            send_log(source_tenant, source, f"Transmission failed!")

    elif data['method'] == 'route':
        send_log(source_tenant, source, "Authorized via external route")
        send_log(source_tenant, source, "Opening session to router")

        # make proxied request through the pep
        response = requests.post(
            f"http://{host}:{port}/proxy",
            headers=headers,
            json=payload
        )

        if response.json().get('your_message'):
            send_log(source_tenant, source, f"Received successful response from tenant {destination_tenant} host {destination}")
        else:
            send_log(source_tenant, source, f"Transmission failed!")
    
    send_log(source_tenant, source, "Transmission complete")
    send_log(source_tenant, source, "-"*75)

if __name__ == "__main__":

    source_tenant = sys.argv[1]
    source = sys.argv[2]
    destination_tenant = sys.argv[3]
    destination = sys.argv[4]
    message = sys.argv[5]

    main(source_tenant, source, destination_tenant, destination, message)
