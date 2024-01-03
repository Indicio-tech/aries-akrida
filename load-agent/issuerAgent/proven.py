from .base import BaseIssuer
import json
import os
import requests
import time

class ProvenIssuer(BaseIssuer):
        def get_invite(self, out_of_band=False, verify=False): 
                # TO DO: how to handle verify param
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                # TO DO: out_of_band?
                r = requests.post(
                    os.getenv("ISSUER_URL") + "/api/v1/invitations?auto_accept=true",
                    json={"metadata": {}, "multi_use": "true"},
                    headers=headers,
                    verify=False)
                try:
                    invitation_url = r.json()["invitation_url"]
                except Exception:
                    raise Exception("Failed to get invitation url. Request: ", r.json())
                if r.status_code != 200:
                    raise Exception(r.content)

                r = r.json()

                return r

        def issue_credential(self, invitation_id):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                issuer_did = os.getenv("CRED_DEF").split(":")[0]
                schema_parts = os.getenv("SCHEMA").split(":")

                r = requests.post(
                    os.getenv('ISSUER_URL') + '/api/v1/credentials', 
                    json={
                        "invitation_id": invitation_id,
                        "attributes": json.loads(os.getenv('CRED_ATTR')),
                        "schema_id":  os.getenv('SCHEMA'),
                    },
                    headers=headers,
                    verify=False
                    )
                if r.status_code != 200:
                    raise Exception(r.content)

                r = r.json()

                line = self.readjsonline()

                # TO DO: return minimal amount of things
                return r, line

        def revoke_credential(self, connection_id, credential_exchange_id):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                issuer_did = os.getenv("CRED_DEF").split(":")[0]
                schema_parts = os.getenv("SCHEMA").split(":")

                time.sleep(1)

                r = requests.post(
                        os.getenv("ISSUER_URL") + "/revocation/revoke",
                        json={
                                "comment": "load test",
                                "connection_id": connection_id,
                                "cred_ex_id": credential_exchange_id,
                                "notify": True,
                                "notify_version": "v1_0",
                                "publish": True,
                        },
                        headers=headers,
                )
                if r.status_code != 200:
                        raise Exception(r.content)

        def send_message(self, connection_id, msg):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                r = requests.post(
                        os.getenv("ISSUER_URL") + "/connections/" + connection_id + "/send-message",
                        json={"content": msg},
                        headers=headers,
                )
                r = r.json()
