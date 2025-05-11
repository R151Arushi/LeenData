import json
from datetime import datetime

# Load Okta policy data
with open('part2/approach2/okta/okta_policy.json', 'r') as f:
    okta_data = json.load(f)


okta_policies = okta_data

leen_policies = []

def extract_policy(policy):

    leen_policy = {
        "type": policy.get("type"),
        "description": policy.get("description"),
        "policyName": policy.get("name"),
        "id": policy.get("id"),
        "status": policy.get("status"),
        "priority": policy.get("priority"),
        "createdAt": policy.get("created"),
        "lastUpdated": policy.get("lastUpdated"),
        "details": {
            "conditions": policy.get("conditions"),
            "settings": policy.get("settings")
        }
    }

    return leen_policy


for policy in okta_policies:
    leen_policies.append(extract_policy(policy))


leen_payload = {
    "policies": leen_policies
}


with open('part2/approach2/okta/okta_leen_policy.json', 'w') as out:
    json.dump(leen_payload, out, indent=2)

print("Leen policy data saved as okta_leen_policy.json")
