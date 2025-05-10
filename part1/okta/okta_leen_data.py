import json
from datetime import datetime
from collections import defaultdict

def safe_date_diff_days(from_date_str):
    try:
        from_date = datetime.strptime(from_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return (datetime.utcnow() - from_date).days
    except Exception:
        return None

# Load the actual JSON file
with open('okta/okta.json') as f:
    okta_data = json.load(f)

users = okta_data.get('user', [])
factors_raw = okta_data.get('factor', [])
roles_raw = okta_data.get('role', [])

# Group factors and roles by user ID
user_factors = defaultdict(list)
user_roles = defaultdict(list)

for factor in factors_raw:
    user_id = factor.get('id')
    if user_id:
        user_factors[user_id].append(factor)

for role in roles_raw:
    user_id = role.get('id')
    if user_id:
        user_roles[user_id].append(role)

leen_items = []

for user in users:
    uid = user.get('id')
    profile = user.get('profile', {})
    email = profile.get('email', '')
    domain = email.split('@')[-1] if email else ''
    factors = user_factors.get(uid, [])
    roles = user_roles.get(uid, [])
    status = user.get('status', '')

    # Use first factor if any
    factor = factors[0] if factors else {}
    is_mfa_enrolled = bool(factor)
    mfa_type = factor.get('factorType', '') if factor else ''
    mfa_provider = factor.get('provider', '') if factor else ''
    mfa_status = factor.get('status', 'NOT_SETUP') if factor else 'NOT_SETUP'

    # Role logic
    access_level = roles[0]['type'] if roles else 'APP_USER'
    assigned_role = roles[0].get('assignmentType', 'USER') if roles else 'USER'
    is_admin = any(role.get('type') == 'APP_ADMIN' for role in roles)

    password_changed_days = safe_date_diff_days(user.get('passwordChanged'))

    item = {
        "id": uid,
        "domain": domain,
        "email_addr": email,
        "full_name": f"{profile.get('firstName', '')} {profile.get('lastName', '')}".strip(),
        "name": profile.get('firstName', ''),
        "vendor_id": uid,
        "vendor_status": status,
        "vendor_created_at": user.get('created'),
        "activated_at": user.get('activated'),
        "last_status_changed_at": user.get('statusChanged'),
        "last_login_at": user.get('lastLogin'),
        "last_updated_at": user.get('lastUpdated'),
        "password_changed_days": password_changed_days,
        "is_mfa_enrolled": is_mfa_enrolled,
        "mfa_type": mfa_type,
        "mfa_status": mfa_status,
        "mfa_provider": mfa_provider,
        "is_admin": is_admin,
        "access_level": access_level,
        "assigned_role": assigned_role,
        "is_deleted": status == 'DEPROVISIONED'
    }

    leen_items.append(item)

leen_payload = {
    "count": len(leen_items),
    "total": len(leen_items),
    "items": leen_items
}

with open('okta/leen_users_from_okta.json', 'w') as out:
    json.dump(leen_payload, out, indent=2)
