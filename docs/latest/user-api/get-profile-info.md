---
sidebar_position: 3
---

# Get profile info

### Request URL

:::info GET
```
https://api.aviauth.com/latest/users/profile/
```
:::

### Curl

```bash
curl -X 'GET' \
  'https://api.aviauth.com/latest/users/profile' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
```

### Response

:::success 200
```json
{
  "email": "johndoe@example.com",
  "id": "dda1757c-1947-490b-8cb3-b3295ae5366e",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe"
}
```
:::


### Common errors

:::warning 401
```json
{
  "detail": "Not authenticated"
}
```
:::

Will be raised in case `access_token` was not provided or is outdated.
