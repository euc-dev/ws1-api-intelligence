---
layout: page
title: Authentication
hide:
  - toc
---

# Authentication

API calls to Omnissa Intelligence are always authenticated using a JSON Web Token (JWT). JWT tokens are submitted as Bearer tokens in an HTTP Authorization header.

| Header name | Header value |
| --- | --- |
| Authorization | Bearer `<token>` |

More information about JSON Web Tokens can be found in [RFC 7519](https://tools.ietf.org/html/rfc7519). [jwt.io](https://jwt.io/) is a helpful tool for parsing JSON Web Tokens.

If access tokens are expired or invalid, the API invoked returns an HTTP status **401 (Unauthorized)**.

Individual operations in **[REST APIs](REST-APIs.md)** may note additional requirements.

---

## Credentials for API access

### 1. Configure a service account

A service account provides you with a clientId and clientSecret that can be used to obtain a JSON Web Token for calling Intelligence APIs.

1. In the Omnissa Intelligence UI, go to **Settings → Service Accounts**.
2. Create a service account.
3. The browser downloads a JSON credentials file with the credential.

Example shape of the downloaded file (values are illustrative):

```json
{
  "name": "reportscript",
  "tokenEndpoint": "https://auth.{environment}/oauth/token",
  "clientId": "your-client-id@{tenant}.data.workspaceone.com",
  "clientSecret": "<secret>",
  "authorizedGrantType": ["CLIENT_CREDENTIALS"],
  "resourceIds": ["api.data.workspaceone.com"]
}
```

The clientSecret is a password and must be protected. After creating the service account, you cannot retrieve the clientSecret again. You may generate a new clientSecret, but this replaces (invalidates) the original clientSecret.

!!! warning "Protect client secrets"

    Treat `clientSecret` like a password. Store the downloaded JSON securely.

Use the `tokenEndpoint`, `clientId`, and `clientSecret` from **your** downloaded file — hostnames differ by region and environment.

### 2. Obtain an access token (client credentials)

The PDF documents obtaining a token with **OAuth 2.0 client credentials** using:

- **HTTP method:** `POST`
- **URL:** your token endpoint with `grant_type` in the **query string**, for example:

  `https://auth.sandbox.data.workspaceone.com/oauth/token?grant_type=client_credentials`

| Header | Value |
| --- | --- |
| Authorization | `Basic` + Base64(`clientId` + `:` + `clientSecret`) |

The username for Basic auth is the client Id; the password is the client Secret.

The documented flow does **not** require a request body when `grant_type` is supplied in the query string.

Notice the **auth** prefix on the URI. All other APIs are accessed with an **api** prefix. Only the token endpoint uses the **auth** prefix.

!!! tip "Alternate OAuth client implementations"

    Some OAuth2 clients send `grant_type=client_credentials` in an **HTML form body** and set `Content-Type: application/x-www-form-urlencoded`. That pattern is common in the ecosystem but is **not** what the Intelligence V2 PDF documents for the query-string flow above.

### Example request (cURL)

Replace placeholders with values from your service account JSON:

```bash
CLIENT_ID='your-client-id@{tenant}.data.workspaceone.com'
CLIENT_SECRET='your-client-secret'
AUTH_HOST='https://auth.sandbox.data.workspaceone.com'

BASIC=$(printf '%s:%s' "$CLIENT_ID" "$CLIENT_SECRET" | base64)

curl -s -X POST "$AUTH_HOST/oauth/token?grant_type=client_credentials" \
  -H "Authorization: Basic $BASIC" \
  -H "Accept: application/json"
```

### Example token response

Successful responses include an access token and related fields. Below is an illustrative shape aligned with the DHUB V2 documentation; the real `access_token` is a long JWT string.

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.<payload-and-signature-truncated>",
  "expires_in": 3599,
  "iss": "https://auth.{your-environment}",
  "jti": "a3a990fb-b5f8-4ed9-afc0-4a671dd5758b",
  "nbf": 1559613306,
  "scope": "dpa.example.scope.one dpa.example.scope.two",
  "token_type": "bearer",
  "dpa.org_id": "538f619e-2db4-4f07-974b-efb3e5326116"
}
```

The access_token in the response can be used to call Omnissa Intelligence APIs.

---

## Quick checklist

- [ ] Service account JSON downloaded and stored securely  
- [ ] Token retrieved from the `auth` endpoint  
- [ ] `Authorization: Bearer …` set on Intelligence `api` requests  

Continue to **[REST APIs](REST-APIs.md)** for endpoint details. Non-auth **API sample responses** from the same documentation set are collected on **[API sample responses](API-sample-responses.md)**.
