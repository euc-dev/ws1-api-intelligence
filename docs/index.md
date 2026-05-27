---
layout: page
title: Omnissa Intelligence APIs
hide:
  - toc
---

![Omnissa Intelligence](assets/logos/favicon-dark.svg){ align=right }

The Omnissa Intelligence (formerly Workspace ONE Intelligence) V2 API documentation describes how to query and extract data for use in other business intelligence tools. It also helps with building General Data Protection Regulation (GDPR) compliant tools and applications with REST APIs.

A limitation of V1 APIs was they didn't support joining multiple entities. V2 APIs for reports now support JOINS. Attribute names in V2 endpoint requests and responses are fully qualified and are in the format `<integration>.<entity>.<attribute_name>` (for example, `airwatch.application.app_name`).

## Documentation and reference

| Resource | Link |
| --- | --- |
| API Documentation for Omnissa Intelligence V2 (PDF) | [Download PDF](https://developer.omnissa.com/omnissa-intelligence-apis/guides/DHUB-APIDocumentationforOmnissaIntelligence-V2-130326-183145.pdf){ .md-button } |
| Authentication | [Authentication](Authentication.md) |
| REST APIs (OpenAPI / Swagger UI) | [REST APIs](REST-APIs.md) |
| API sample responses | [Sample responses](API-sample-responses.md) |

Web-native companion pages:

- **[Authentication](Authentication.md)** — JWT bearer tokens and service account credentials as described in the PDF.
- **[REST APIs](REST-APIs.md)** — interactive OpenAPI reference for Intelligence V2 endpoints.
- **[API sample responses](API-sample-responses.md)** — JSON examples aligned with **API Documentation for Omnissa Intelligence – V2**.

## Intended audience

This content is intended for experienced developers who are familiar with Omnissa Intelligence data and controls.

## Terms

**Omnissa Workspace ONE UEM:** The name of the product formerly known as AirWatch.

**Omnissa Intelligence for Consumer Apps (Omnissa Intelligence SDK):** The name of the product formerly known as Apteligent or Workspace ONE Intelligence for Consumer Apps.

## API concepts

### Host names

Examples in this document refer to the host. As a customer you will need to substitute the host name specific to the region in which your data resides. For a list of the regions and endpoints, refer to Omnissa’s regional endpoint documentation for your environment.

### Data formats

Any HTTP request body must be submitted as JSON. Include the following header with such requests:

| Header name | Header value |
| --- | --- |
| Content-Type | application/json |

Data returned from the Omnissa Intelligence APIs is likewise returned as JSON. A client should always indicate its ability to process JSON in any request:

| Header name | Header value |
| --- | --- |
| Accept | `application/json` or `*/*` |

### HTTP methods

**GET:** Used to request a single, specific entity/object.

**POST:** Used to submit a request that requires a JSON body. The JSON body can provide information used to create a new object (for example, Create Report API) or it can provide information used to control the result set of a query (for example, pagination, search).

### Path parameters

When a URL requires path parameters, those parameters are denoted with curly braces. For example:

`https://api.sandbox.data.workspaceone.com/v2/reports/{a}`

When making this API call, the value `{a}` must be substituted with an appropriate value.

### Paging

API requests that return more than a single object are always paged. Paging is controlled with two parameters:

| Parameter name | Parameter description | Min | Max | Default |
| --- | --- | --- | --- | --- |
| page_size | The number of records to return. | 1 | 1000 | 100 |
| offset | Offset across the entire data set at which the current page starts. | — | — | (see request examples) |

Paging requires the data set to be sorted. Each dataset has a default sort order, but that can be controlled by specifying `sort_ons`, which consist of two parameters: **field** (the field to sort on; for example `name`) and **order** (`ASC` or `DESC`).

### Search terms

Search terms are provided in the request as an array. This takes three parameters:

| Parameter name | Parameter description | Default value |
| --- | --- | --- |
| value | String value used for searching | — |
| fields | Optional array of fields to search the value | — |
| operator | Optional search operator: `START_WITH`, `CONTAINS`, or `ENDS_WITH` | `CONTAINS` |

These search terms only apply to Omnissa SDK Apps APIs.

### Authentication

API calls to Omnissa Intelligence are always authenticated using a JSON Web Token (JWT). JWT tokens are submitted as Bearer tokens in an HTTP Authorization header (`Authorization: Bearer <token>`).

If access tokens are expired or invalid, the API invoked returns an HTTP status **401 (Unauthorized)**.

Step-by-step credential setup is on **[Authentication](Authentication.md)**.

### API error handling

Input errors always generate an HTTP BAD Request (status **400**) along with a JSON body that provides further details about the error.

`errors` is an array with the following fields:

| Field | Description |
| --- | --- |
| code | The error code indicating the type of error. |
| message | More information about the specific error. |
| violated_property | A specific property name (if applicable). |

Other standard errors include:

| HTTP status code | Description |
| --- | --- |
| 401 | Authentication failed. Likely your access-token needs to be renewed. |
| 403 | Authorization failed. You attempted to access a resource or perform an operation that you are not permitted to do. |
| 404 | The resource you attempted to access does not exist. |
| 429 | Rate limit exceeded. |

### Structure of data

Data is organized in a 3-level hierarchy: **Integration / Entity or Event Type / Attribute**.

An **Entity** would be an object for which the system tracks attributes over time. For example, device and users would be entities. An **Event Type** is an event that occurs at a point in time. For example, an app launch or a notification from a security vendor would both be events.

An **Attribute** is a key-value pair associated with an entity or an event type. For example, a “Device Friendly Name” could be an attribute of a device.

For API responses, the following integration/entity combinations are available (category as seen in the Omnissa Intelligence UI):

| Category | Integration | Entity | Category (UI) |
| --- | --- | --- | --- |
| Apps | airwatch | application | Apps |
| Devices | airwatch | device | Devices |
| OS Updates | airwatch | windowspatch | OS Updates |
| Device Sensors | airwatch | devicesensors | Device Sensors |
| Intelligence SDK | Not Applicable | e.g. Android Crashes | Intelligence SDK |

Note: This field is not applicable for Omnissa Intelligence for Consumer Apps APIs)

## API call limits

The calculations of API request amounts allow sufficient capacity for your organization's number of admin users and user licenses. Omnissa Workspace ONE license levels categorize rate limits by calls per second, calls per hour, and calls per 24 hours.

Refer to **Table 1. API Call Limits Per Organization** in the PDF for Standard, Advanced, Enterprise, and Intelligence Add-On tiers.

## Next steps

1. Follow **[Authentication](Authentication.md)** to configure a service account and retrieve tokens.
2. Explore endpoints in **[REST APIs](REST-APIs.md)**.
3. Compare payloads using **[Sample responses](API-sample-responses.md)**.
