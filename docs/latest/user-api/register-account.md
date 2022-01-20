---
sidebar_position: 1
---

# Register account

### Request URL

:::info POST
```
https://api.aviauth.com/latest/users/register/
```
:::

### Request body

```json
{
  "grant_type": "password",
  "email": "johndoe@example.com",
  "password": "tss!its-a-secret",
  "scope": "",
  "client_id": "super-secret-id",
  "client_secret": "and-even-more-secret-secret",
}
```

### Curl

```
curl -X 'POST' \
  'https://api.aviauth.com/latest/users/register/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&email=user@example.com&password=password&scope=&client_id=client_id&client_secret=client_secret'
```

### Response

:::success 201
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

:::warning 400
```json
{
  "detail": "User with this email already registered."
}
```
:::

:::warning 401
```json
{
  "detail": "Invalid client credentials"
}
```
:::

Will be raised in case `client_id` and `client_secret` are not valid.
