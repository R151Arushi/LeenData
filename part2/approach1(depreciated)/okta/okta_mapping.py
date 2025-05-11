import json
from datetime import datetime

# Load Okta policy data
with open('part2/approach1/okta_policy.json', 'r') as f:
    okta_data = json.load(f)


okta_policies = okta_data

leen_policies = []

def extract_password_policy(policy):

    settings = policy.get("settings", {}).get("password", {})
    
    # Extracting complexity settings
    complexity = settings.get("complexity", {})
    minLength = complexity.get("minLength", 8)
    minUpperCase = complexity.get("minUpperCase", 1)
    minLowerCase = complexity.get("minLowerCase", 1)
    minNumber = complexity.get("minNumber", 0)
    minSymbol = complexity.get("minSymbol", 0)
    
    # Ensure all values are integers, not None
    minLength = 0 if minLength is None else minLength
    minUpperCase = 0 if minUpperCase is None else minUpperCase
    minLowerCase = 0 if minLowerCase is None else minLowerCase
    minNumber = 0 if minNumber is None else minNumber
    minSymbol = 0 if minSymbol is None else minSymbol

    # Extracting age settings
    age = settings.get("age", {})
    maxAgeDays = age.get("maxAgeDays", 0)
    historyCount = age.get("historyCount", 4)

    # Extracting overrides for specific roles
    overrides = settings.get("overrides", {})

    # Constructing the final structure for the password policy
    leen_policy = {
        "policyName": "passwordPolicy",
        "status": policy.get("status", "ACTIVE"),
        "priority": policy.get("priority", 1),
        "createdAt": policy.get("created", ""),
        "lastUpdated": policy.get("lastUpdated", ""),
        "details": {
            "minLength": minLength,
            "complexity": {
                "requireUppercase": minUpperCase > 0,
                "requireLowercase": minLowerCase > 0,
                "requireNumber": minNumber > 0,
                "requireSymbol": minSymbol > 0
            },
            "expiryDays": maxAgeDays if maxAgeDays > 0 else 0,
            "historyCount": historyCount,
            "overrides": {}
        }
    }

    for role, override in overrides.items():
        role_details = {
            "minLength": override.get("minLength", 0),
            "complexity": {
                "requireUppercase": override.get("complexity", {}).get("minUpperCase", 0) > 0,
                "requireLowercase": override.get("complexity", {}).get("minLowerCase", 0) > 0,
                "requireNumber": override.get("complexity", {}).get("minNumber", 0) > 0,
                "requireSymbol": override.get("complexity", {}).get("minSymbol", 0) > 0
            },
            "expiryDays": override.get("expiryDays", 0),
            "historyCount": override.get("historyCount", 0)
        }
        leen_policy["details"]["overrides"][role] = role_details

    return leen_policy

def extract_signon_policy(policy):
    # Extracting conditions
    conditions = policy.get("conditions", {}).get("people", {}).get("groups", {}).get("include", [])

    # Default session settings
    session_settings = {
        "maxSessionLifetimeMinutes": 120,  # Default max session lifetime
        "usePersistentCookie": False,  # Okta doesn't explicitly provide persistent cookie option
        "requireFactorEverySignIn": True  # Assuming this is always true for sign-on policy
    }

    # Access control settings
    access_control = {
        "allowedRegions": [],
        "blockedCountries": []
    }

    # Check for specific rules in Okta for access control
    if "accessControl" in policy:
        allowed_regions = policy["accessControl"].get("allowedRegions", [])
        blocked_countries = policy["accessControl"].get("blockedCountries", [])
        
        access_control["allowedRegions"] = allowed_regions if allowed_regions else []
        access_control["blockedCountries"] = blocked_countries if blocked_countries else []

    # Constructing the final structure for the sign-on policy
    leen_policy = {
        "policyName": "signOnPolicy",
        "status": policy.get("status", "ACTIVE"),
        "priority": policy.get("priority", 1),
        "createdAt": policy.get("created", ""),
        "lastUpdated": policy.get("lastUpdated", ""),
        "details": {
            "allowedGroups": conditions,
            "sessionSettings": session_settings,
            "accessControl": access_control,
            "overrides": {}
        }
    }

    # Handle overrides (for roles such as admin, contractor)
    overrides = policy.get("overrides", {})
    for role, override in overrides.items():
        role_details = {
            "allowedGroups": override.get("allowedGroups", []),
            "sessionSettings": {
                "maxSessionLifetimeMinutes": override.get("sessionSettings", {}).get("maxSessionLifetimeMinutes", 120),
                "requireFactorEverySignIn": override.get("sessionSettings", {}).get("requireFactorEverySignIn", True)
            },
            "accessControl": {
                "allowedRegions": override.get("accessControl", {}).get("allowedRegions", []),
                "blockedCountries": override.get("accessControl", {}).get("blockedCountries", [])
            }
        }
        leen_policy["details"]["overrides"][role] = role_details

    return leen_policy

def extract_mfa_policy(policy):
    # Extract factors from Okta policy
    factors = policy.get("settings", {}).get("factors", {})

    # Mapping Okta factors to Leen's format
    leen_factors = []
    if factors.get("okta_otp", {}).get("enroll", {}).get("self") == "OPTIONAL":
        leen_factors.append("one_time_passcode")
    if factors.get("okta_push", {}).get("enroll", {}).get("self") == "OPTIONAL":
        leen_factors.append("push_notification")
    if factors.get("okta_password", {}).get("enroll", {}).get("self") == "OPTIONAL":
        leen_factors.append("password")
    
    # You can add more factors as necessary, defaulting to `sms` and `email` as placeholders for disabled factors
    if factors.get("okta_otp", {}).get("enroll", {}).get("self") != "OPTIONAL":
        leen_factors.append("sms")
    if factors.get("okta_push", {}).get("enroll", {}).get("self") != "OPTIONAL":
        leen_factors.append("email")

    # Construct Leen MFA policy JSON structure
    leen_policy = {
        "policyName": policy.get("name", "mfaPolicy"),
        "status": policy.get("status", "ACTIVE"),
        "priority": policy.get("priority", 1),
        "createdAt": policy.get("created", ""),
        "lastUpdated": policy.get("lastUpdated", ""),
        "details": {
            "enforced": True,  # Default to True, you can adjust this based on Okta's settings
            "factors": leen_factors  # Factors extracted from Okta policy
        }
    }

    return leen_policy

def extract_entity_risk_policy(policy):
    
    leen_policy = {
        "policyName": policy.get("name", "entityRiskPolicy"),
        "status": policy.get("status", "ACTIVE"),
        "priority": policy.get("priority", 1),
        "createdAt": policy.get("created", ""),
        "lastUpdated": policy.get("lastUpdated", ""),
        "details": policy.get("rules", {})
    }
    
    return leen_policy
    

# Map Okta policies into Leen format
for policy in okta_policies:
    policy_type = policy.get("type")

    if policy_type == "PASSWORD":
        leen_policies.append(extract_password_policy(policy))
    elif policy_type == "OKTA_SIGN_ON":
        leen_policies.append(extract_signon_policy(policy))
    elif policy_type == "MFA_ENROLL":
        leen_policies.append(extract_mfa_policy(policy))
    elif policy_type == "ENTITY_RISK":
        leen_policies.append(extract_entity_risk_policy(policy))

# Prepare the final Leen payload
leen_payload = {
    "count": len(leen_policies),
    "total": len(leen_policies),
    "items": leen_policies
}

# Write the output to a new JSON file
with open('part2/approach1/okta_leen_policy.json', 'w') as out:
    json.dump(leen_payload, out, indent=2)

print("Leen policy data saved as okta_leen_policy.json")
