---
sidebar_position: 4
---

# Get access token

### Request URL

:::info POST
```
https://api.aviauth.com/latest/auth/token/
```
:::

### Request body

```json
{
  "grant_type": "password",
  "email": "johndoe@example.com",
  "password": "tss!its-a-secret",
  "scope": "user:full",
  "client_id": "super-secret-client-id",
  "client_secret": "and-even-more-secret-secret",
}
```

### Curl

```bash
curl -X 'POST' \
  'https://api.aviauth.com/latest/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=johndoe@example.com&password=tss!its-a-secret&scope=user%3Afull&client_id=super-secret-client-id&client_secret=and-even-more-secret-secret'
```

### Response

:::success status_code: 201
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
  "expires_in": 1800
}
```
:::

### Common errors

:::warning status_code: 401
```json
{
  "detail": "Invalid client credentials"
}
```
:::

Will be raised in case `client_id` and `client_secret` are not valid.


:::warning status_code: 401
```json
{
  "detail": "Invalid user credentials"
}
```
:::
