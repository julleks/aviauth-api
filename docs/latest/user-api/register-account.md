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
  "client_id": "super-secret-client-id",
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


### What do we keep underneath

:::info access_token
```json
{
  "sub": "dda1757c-1947-490b-8cb3-b3295ae5366e",
  "scope": "user:read user:update user:full applications:read applications:create applications:update applications:full",
  "exp": 1640939869
}
```
:::

:::info refresh_token
```json
{
  "exp": 1640975054,
  "iat": 1640939054,
  "scope": "user:read user:update user:full applications:read applications:create applications:update applications:full",
  "sub": "54648e29-5e6c-4fc8-b4a6-d514acb98c59",
  "aud": ["https://api.aviauth.com/latest/auth/token"],
  "iss": "https://api.aviauth.com",
  "azp": "super-secret-client-id"
}
```
:::
