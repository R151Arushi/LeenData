## Leen Candidate Exercise: IDP Model Extension

###Part 1: Enhancing the User Object

1. API Endpoints:
```
For Okta:
GET https://{yourOktaDomain}/api/v1/users
GET https://{yourOktaDomain}/api/v1/users/{userId}/factors
GET https://{yourOktaDomain}/api/v1/iam/assignees/users

For MS Entra:
GET https://graph.microsoft.com/v1.0/users
GET https://graph.microsoft.com/v1.0/reports/authenticationMethods/userRegistrationDetails/{userId}

```
2. Final Mapping:

| Leen Model Field           | Okta IDP | MS Entra IDP |
|----------------------------|:--------:|:------------:|
| `id`                       | ✅       | ✅           |
| `domain`                   | ✅       | ✅           |
| `email_addr`              | ✅       | ✅           |
| `full_name`                | ✅       | ✅           |
| `name`                     | ✅       | ✅           |
| `vendor_id`                | ✅       | ✅           |
| `vendor_status`            | ✅       | ❌           |
| `vendor_created_at`        | ✅       | ✅           |
| `activated_at`             | ✅       | ✅           |
| `last_status_changed_at`   | ✅       | ❌           |
| `last_login_at`            | ✅       | ✅           |
| `last_updated_at`          | ✅       | ❌           |
| `password_changed_days`    | ✅       | ✅           |
| `is_mfa_enrolled`          | ✅       | ✅           |
| `mfa_type`                 | ✅       | ❌           |
| `mfa_status`               | ✅       | ❌           |
| `mfa_provider`             | ✅       | ❌           |
| `is_admin`                 | ✅       | ✅           |
| `access_level`             | ✅       | ✅           |
| `assigned_role`            | ✅       | ✅           |
| `is_deleted`               | ✅       | ✅           |


For a detailed deep dive in to process, refer to this google doc: [Google Doc](https://docs.google.com/document/d/1msJhx4C_EoU7_iprS4mwE67q3YukB8T95tBfBf_dz9Q/edit?usp=sharing)

Part 2: Desiging a Policy Object
- Intsert Json
- Approach 1: 
- Approach 2:
- More infromation


