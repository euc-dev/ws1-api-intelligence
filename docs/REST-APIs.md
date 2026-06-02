---
layout: page
title: REST APIs
hide:
  - toc
---

# REST APIs

The Omnissa Intelligence (formerly Workspace ONE Intelligence) V2 API documentation describes REST endpoints for querying and extracting data (metadata, metrics, and reports) across supported integrations. Calls are authenticated with a JWT bearer token as described in **[Authentication](Authentication.md)**.

Substitute your tenant’s regional **`api`** host name for examples that use hosts such as `api.sandbox.data.workspaceone.com`.

<section id="swagger-token-bridge" class="swagger-token-bridge" aria-labelledby="swagger-token-bridge-title">
  <h2 id="swagger-token-bridge-title">Get Access Token For Swagger</h2>
  <p>Enter the service account credentials from your downloaded JSON file to fetch an access token and automatically populate Swagger's Bearer authorization for the Intelligence APIs.</p>
  <form id="swagger-token-bridge-form" class="swagger-token-bridge__form">
    <label class="swagger-token-bridge__field">
      <span>Auth host</span>
      <input id="swagger-auth-host" name="authHost" type="url" placeholder="https://auth.sandbox.data.workspaceone.com" autocomplete="url" required />
    </label>
    <label class="swagger-token-bridge__field">
      <span>clientId</span>
      <input id="swagger-client-id" name="clientId" type="text" placeholder="your-client-id@{tenant}.data.workspaceone.com" autocomplete="username" required />
    </label>
    <label class="swagger-token-bridge__field">
      <span>clientSecret</span>
      <input id="swagger-client-secret" name="clientSecret" type="password" autocomplete="current-password" required />
    </label>
    <div class="swagger-token-bridge__actions">
      <button id="swagger-token-submit" type="submit">Get access token</button>
      <p class="swagger-token-bridge__hint">If you already have a JWT, you can still use Swagger's <strong>Authorize</strong> button to paste it directly into Bearer auth.</p>
    </div>
  </form>
  <p id="swagger-token-bridge-status" class="swagger-token-bridge__status" role="status" aria-live="polite"></p>
</section>

<swagger-ui src="intelligence-rest-api-swagger.json" />
