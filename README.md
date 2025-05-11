## Leen Candidate Exercise: IDP Model Extension

### Part 1: Enhancing the User Object

1. API Endpoints:
```
For Okta:
GET https://{yourOktaDomain}/api/v1/users
GET https://{yourOktaDomain}/api/v1/users/{userId}/factors
GET https://{yourOktaDomain}/api/v1/iam/assignees/users

For MS Entra:
GET https://graph.microsoft.com/v1.0/users
GET https://graph.microsoft.com/v1.0/reports/authenticationMethods/userRegistrationDetails/{userId}
GET https://graph.microsoft.com/v1.0/users/{userId}?$select=accountEnabled,createdDateTime

```
2. Final Mapping:

| Leen Model Field           | Okta IDP | MS Entra IDP |
|----------------------------|:--------:|:------------:|
| `id`                       | ✅       | ✅           |
| `domain`                   | ✅       | ✅           |
| `email_addr`               | ✅       | ✅           |
| `full_name`                | ✅       | ✅           |
| `name`                     | ✅       | ✅           |
| `vendor_id`                | ✅       | ✅           |
| `vendor_status`            | ✅       | ✅           |
| `vendor_created_at`        | ✅       | ❌           |
| `activated_at`             | ✅       | ❌           |
| `last_status_changed_at`   | ✅       | ❌           |
| `last_login_at`            | ✅       | ✅           |
| `last_updated_at`          | ✅       | ❌           |
| `password_changed_days`    | ✅       | ❌           |
| `is_mfa_enrolled`          | ✅       | ✅           |
| `mfa_type`                 | ✅       | ✅           |
| `mfa_status`               | ✅       | ✅           |
| `mfa_provider`             | ✅       | ✅           |
| `is_admin`                 | ✅       | ✅           |
| `access_level`             | ✅       | ✅           |
| `assigned_role`            | ✅       | ✅           |


For a detailed deep dive in to process, refer to this google doc: [Google Doc](https://docs.google.com/document/d/1msJhx4C_EoU7_iprS4mwE67q3YukB8T95tBfBf_dz9Q/edit?usp=sharing)

### Part 2: Desiging a Policy Object

1. API Endpoints:

```
For Okta:
1. GET https://{yourOktaDomain}/api/v1/policies

For MS Entra:
1. GET https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies

```

2. Final JSON Schema:

```
{
  "policies": [
    { 
      "type": "policyType",
      "policyName": "policy1",
      "description": "policyDescription",
      "id": "policyId",
      "status": "ACTIVE",
      "priority": 1,
      "createdAt": "2024-10-01T12:00:00Z",
      "lastUpdated": "2025-01-10T10:45:00Z",
      "details": {
        "overrides": {
          "users": {}
        }
      }
    }
  ]
}

```

For a detailed deep dive in to process, refer to this google doc: [Google Doc](https://docs.google.com/document/d/1msJhx4C_EoU7_iprS4mwE67q3YukB8T95tBfBf_dz9Q/edit?usp=sharing)

