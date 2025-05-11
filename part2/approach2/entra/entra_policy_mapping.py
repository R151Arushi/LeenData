import json
from datetime import datetime

# Load Okta policy data
with open('part2/approach2/entra/ms_entra_policy.json', 'r') as f:
    entra_data = json.load(f)


entra_policies = entra_data.get("value", [])

leen_policies = []

def extract_policy(policy):

    leen_policy = {
        "type": None,
        "description": policy.get("displayName"),
        "policyName": policy.get("displayName"),
        "id": policy.get("id"),
        "status": policy.get("state"),
        "priority": None,
        "createdAt": policy.get("createdDateTime"),
        "lastUpdated": policy.get("modifiedDateTime"),
        "details": {
            "conditions": policy.get("conditions"),
            "grantControls": policy.get("grantControls")
        }
    }

    return leen_policy


for policy in entra_policies:
    leen_policies.append(extract_policy(policy))


leen_payload = {
    "policies": leen_policies
}


with open('part2/approach2/entra/entra_leen_policy.json', 'w') as out:
    json.dump(leen_payload, out, indent=2)

print("Leen policy data saved as entra_leen_policy.json")
