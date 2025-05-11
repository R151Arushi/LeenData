import json
from datetime import datetime
import uuid
def generate_uid(user_id):
    return str(uuid.uuid4())

def safe_date_diff_days(from_date_str):
    try:
        from_date = datetime.strptime(from_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return (datetime.utcnow() - from_date).days
    except Exception:
        return None

# Load Microsoft Entra (Azure AD) export
with open('part1/entra/ms_entra.json') as f:
    entra_data = json.load(f)

users = entra_data.get('Users', [])
factor = entra_data.get('factor', {})
details = entra_data.get('details', {})
leen_items = []

for user in users:
    
    item = {
        "id": generate_uid(user.get('id')),
        "domain": user.get('mail').split('@')[-1] if user.get('mail') else '',
        "email_addr": user.get('mail') or user.get('userPrincipalName', ''),
        "full_name": user.get('displayName', ''),
        "name": user.get('displayName', ''),
        "vendor_id": user.get('id'),
        "vendor_status": "ACTIVE" if details.get('accountEnabled') else "INACTIVE",
        "vendor_created_at": None,
        "activated_at": None,
        "last_status_changed_at": None,
        "last_login_at": details.get('lastSignInDateTime'),
        "last_updated_at": None,
        "password_changed_days": None,
        "mfa_type": factor.get('methodsRegistered'),
        "mfa_status": "ACTIVE" if factor.get('isMfaRegistered') else "NOT_SETUP",
        "mfa_provider": "MS Entra",
        "is_admin": factor.get('isAdmin'),
        "access_level": "",
        "assigned_role": factor.get('userType'),
        "is_deleted": False
    }

    leen_items.append(item)

leen_payload = {
    "count": len(leen_items),
    "total": len(leen_items),
    "items": leen_items
}

# Save result
with open('part1/entra/entra_leen_data.json', 'w') as out:
    json.dump(leen_payload, out, indent=2)

