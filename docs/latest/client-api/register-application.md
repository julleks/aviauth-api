---
sidebar_position: 1
---

# Register application

### Request URL

:::info POST
```
https://api.aviauth.com/latest/applications/register/
```
:::

### Request body

```json
{
  "client_id": "switter",
  "client_secret": "5USE.6]f38n1Bb|i9?sAvQEFU+Y~t"
}
```

### Curl

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/latest/applications/register' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' \
  -H 'Content-Type: application/json' \
  -d '{
  "client_id": "switter",
  "client_secret": "5USE.6]f38n1Bb|i9?sAvQEFU+Y~t"
}'
```

### Response

:::success 201
```json
{
  "client_id": "switter"
}
```
:::


### Common errors

:::warning 400
```json
{
  "detail": "Application with this client_id already registered"
}
```
:::

:::warning 401
```json
{
  "detail": "Not authenticated"
}
```
:::
