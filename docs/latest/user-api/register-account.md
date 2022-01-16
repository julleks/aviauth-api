---
sidebar_position: 1
---

# Register account

Everything starts from a user.

So, this endpoint is intended for user registration.

:::caution
Endpoint is available for **internal usage** only.
:::

If you are not an Aviauth developer, you may be interested in going further: [Get access token](./get-access-token.md).

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
  "client_id": "public-client-id",
  "client_secret": "super-secret-secret",
}
```

### Curl

```bash
curl -X 'POST' \
  'https://api.aviauth.com/latest/users/register/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&email=johndoe@example.com&password=tss!its-a-secret&scope=&client_id=public-client-id&client_secret=super-secret-secret'
```

### Response

:::success 201
```json
{
  "access_token": "eyJhbGciOiJIUzI1N...iIsInR5cCI6IkpXVCJ9",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJIUzI1...NiIsInR5cCI6IkpXVCJ9",
  "expires_in": 1800
}
```
:::


In case of successful user registration, an introduction email with confirmation link will be sent
to the provided email address.


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

:::warning 422
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "email"
      ],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```
:::

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
