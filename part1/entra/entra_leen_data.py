import json
from datetime import datetime

def safe_date_diff_days(from_date_str):
    try:
        from_date = datetime.strptime(from_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return (datetime.utcnow() - from_date).days
    except Exception:
        return None

# Load Microsoft Entra (Azure AD) export
with open('entra/ms_entra.json') as f:
    entra_data = json.load(f)

users = entra_data.get('Users', [])
factor = entra_data.get('factor', {})

leen_items = []

for user in users:
    uid = user.get('id')
    email = user.get('mail') or user.get('userPrincipalName', '')
    domain = email.split('@')[-1] if email else ''
    full_name = user.get('displayName', '')
    name = user.get('givenName') or full_name.split()[0] if full_name else ''
    is_admin = factor.get('isAdmin', False)
    is_mfa_enrolled = factor.get('isMfaRegistered', False)
    mfa_type = factor.get('defaultMfaMethod', '')
    mfa_status = "ACTIVE" if is_mfa_enrolled else "NOT_SETUP"
    mfa_provider = "MICROSOFT"
    access_level = "ORG_ADMIN" if is_admin else "ORG_USER"
    assigned_role = "USER"
    last_updated = factor.get("lastUpdatedDateTime")

    item = {
        "id": uid,
        "domain": domain,
        "email_addr": email,
        "full_name": full_name,
        "name": name,
        "vendor_id": uid,
        "vendor_status": "ACTIVE",
        "vendor_created_at": None,
        "activated_at": None,
        "last_status_changed_at": None,
        "last_login_at": None,
        "last_updated_at": last_updated,
        "password_changed_days": None,
        "is_mfa_enrolled": is_mfa_enrolled,
        "mfa_type": mfa_type,
        "mfa_status": mfa_status,
        "mfa_provider": mfa_provider,
        "is_admin": is_admin,
        "access_level": access_level,
        "assigned_role": assigned_role,
        "is_deleted": False
    }

    leen_items.append(item)

leen_payload = {
    "count": len(leen_items),
    "total": len(leen_items),
    "items": leen_items
}

# Save result
with open('entra/leen_users_from_entra.json', 'w') as out:
    json.dump(leen_payload, out, indent=2)
