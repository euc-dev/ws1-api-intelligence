---
layout: page
title: API sample responses
hide:
  - toc
---

# API sample responses

These examples are transcribed from **API Documentation for Omnissa Intelligence – V2**. Values illustrate shape only; substitute your tenant URLs, identifiers, and tokens in real calls.

For authentication and token responses, see **[Authentication](Authentication.md)**. For interactive exploration, see **[REST APIs](REST-APIs.md)**.

---

## Metrics metadata (SDK Apps)

### Entities API — sample response (`POST /v2/metadata/entities`)

```json
{
  "data": {
    "page_size": 5,
    "offset": 0,
    "total_count": 25,
    "results": [
      {
        "name": "airwatch.userriskscore",
        "label": "User Risk Score",
        "description": ""
      },
      {
        "name": "airwatch.userriskscore_timeseries",
        "label": "User Risk Score For Timeseries data",
        "description": ""
      }
    ]
  }
}
```

### Attributes API — sample response (`POST /v2/metadata/entity/{name}/attributes`)

```json
{
  "data": {
    "page_size": 2,
    "offset": 0,
    "total_count": 189,
    "entity": "airwatch.device",
    "results": [
      {
        "name": "airwatch.device._airwatch_device_guid",
        "label": "Workspace ONE UEM Device GUID",
        "description": "Workspace ONE UEM Device GUID",
        "data_type": "STRING",
        "bucketing_allowed": true
      },
      {
        "name": "airwatch.device._city",
        "label": "City",
        "description": "City",
        "data_type": "STRING",
        "bucketing_allowed": false
      }
    ]
  }
}
```

---

## Metrics (SDK Apps)

### Entity metrics API — sample response (`POST /v2/metrics/entity`)

```json
{
  "data": {
    "entity": "apteligent.net_event",
    "result_type": "SIMPLE_TIMERANGE",
    "metadata": {
      "date_attribute_name": "apteligent.net_event.adp_modified_at",
      "attributes": {
        "apteligent.net_event.http_status_code": {
          "label": "HTTP Status Code",
          "data_type": "INTEGER"
        },
        "apteligent.net_event._url_host": {
          "label": "URL",
          "data_type": "STRING"
        },
        "apteligent.net_event.bytes_sent": {
          "label": "Data Out",
          "data_type": "LONG"
        }
      }
    },
    "is_complete_dataset": false,
    "result": [
      {
        "start_time": "2020-08-23T00:00:00Z",
        "end_time": "2020-09-02T18:43:02.25Z",
        "bucketing_attributes": {
          "apteligent.net_event.http_status_code": 505,
          "apteligent.net_event._url_host": "api.event.gov"
        },
        "metrics_values": [
          {
            "name": "apteligent.net_event.bytes_sent",
            "function": "AVG",
            "value": 498.22222222222223
          }
        ]
      },
      {
        "start_time": "2020-08-23T00:00:00Z",
        "end_time": "2020-09-02T18:43:02.25Z",
        "bucketing_attributes": {
          "apteligent.net_event.http_status_code": 413,
          "apteligent.net_event._url_host": "api.event.gov"
        },
        "metrics_values": [
          {
            "name": "apteligent.net_event.bytes_sent",
            "function": "AVG",
            "value": 506.64814814814815
          }
        ]
      }
    ]
  }
}
```

### Simple time window — sample response (`POST /v2/metrics/entity/simple_timerange`)

Wrapped payload uses `data` in the request body; response shape matches the metrics envelope below.

```json
{
  "data": {
    "entity": "apteligent.net_event",
    "result_type": "SIMPLE_TIMERANGE",
    "metadata": {
      "date_attribute_name": "apteligent.net_event.event_timestamp",
      "attributes": {
        "apteligent.net_event.bytes_sent": {
          "label": "Data Out",
          "data_type": "LONG"
        }
      }
    },
    "result": [
      {
        "start_time": "2022-12-24T00:00:00Z",
        "end_time": "2023-02-21T23:57:29.568Z",
        "metrics_values": [
          {
            "name": "apteligent.net_event.bytes_sent",
            "function": "AVG",
            "value": 567.833333333334
          }
        ]
      }
    ]
  }
}
```

### Histogram — sample response (`POST /v2/metrics/entity/histogram`)

```json
{
  "data": {
    "entity": "apteligent.crash_ios",
    "result_type": "HISTOGRAM",
    "metadata": {
      "date_attribute_name": "apteligent.crash_ios.adp_modified_at",
      "attributes": {
        "apteligent.crash_ios.device_model": {
          "label": "Device Model",
          "data_type": "STRING"
        }
      }
    },
    "result": [
      {
        "start_time": "2023-02-20T00:00:00Z",
        "end_time": "2023-02-21T00:00:00Z",
        "metrics_values": [
          {
            "name": "apteligent.crash_ios.device_model",
            "function": "COUNT",
            "value": 0
          }
        ]
      },
      {
        "start_time": "2023-02-21T00:00:00Z",
        "end_time": "2023-02-22T00:00:00Z",
        "metrics_values": [
          {
            "name": "apteligent.crash_ios.device_model",
            "function": "COUNT",
            "value": 256
          }
        ]
      }
    ]
  }
}
```

### Rolling window — sample response (`POST /v2/metrics/entity/rolling_window`)

```json
{
  "data": {
    "entity": "apteligent.net_error",
    "result_type": "ROLLING_WINDOW",
    "metadata": {
      "date_attribute_name": "apteligent.net_error.adp_modified_at",
      "attributes": {
        "apteligent.net_error.bytes_sent": {
          "label": "Data Out",
          "data_type": "LONG"
        }
      }
    },
    "result": [
      {
        "start_time": "2023-02-14T00:00:00Z",
        "end_time": "2023-02-21T00:00:00Z",
        "metrics_values": [
          {
            "name": "apteligent.net_error.bytes_sent",
            "function": "COUNT_DISTINCT",
            "value": 400
          }
        ]
      },
      {
        "start_time": "2023-02-15T00:00:00Z",
        "end_time": "2023-02-22T00:00:00Z",
        "metrics_values": [
          {
            "name": "apteligent.net_error.bytes_sent",
            "function": "COUNT_DISTINCT",
            "value": 0
          }
        ]
      }
    ]
  }
}
```

---

## Reports

### Report metadata API — sample response (`GET /v2/meta/integration/{integration}/entity/{entity}/attributes`)

```json
{
  "data": [
    {
      "classification": {
        "label": "User",
        "name": "USER"
      },
      "data_type": "DATETIME",
      "entity": "user",
      "integration": "airwatch",
      "attribute": "airwatch.user.user_last_message_sent_date",
      "source_attribute": "airwatch.user.user_last_message_sent_date",
      "path": "user_last_message_sent_date",
      "label": "Last Message Sent Date",
      "description": "Last Message Sent Date",
      "metadata": false,
      "hidden_in_uifilter": false,
      "hidden_in_uiselect": false,
      "sorting_supported": true,
      "suggestion_supported": false,
      "supported_operators": [
        {
          "name": "BEFORE",
          "label": "Before",
          "description": "Before",
          "value": "<",
          "single": true,
          "value_required": true,
          "min_length": -1
        },
        {
          "name": "AFTER",
          "label": "After",
          "description": "After",
          "value": ">",
          "single": true,
          "value_required": true,
          "min_length": -1
        },
        {
          "name": "BETWEEN",
          "label": "Between",
          "description": "Between",
          "value": "BETWEEN",
          "single": false,
          "value_required": true,
          "min_length": -1
        }
      ]
    }
  ]
}
```

### Create report — historical sample response (`POST /v2/reports`)

```json
{
  "data": {
    "id": "20602124-f68b-4dd5-949a-0e45b3d265b0",
    "name": "API Test Report - 5f5abb88-ea63-43bf-8738-ed0c6a7b345a",
    "description": "Sample report description",
    "integration": "airwatch",
    "entity": "application",
    "filter": "airwatch.application.app_dynamic_size_bytes > 5000000",
    "report_type": "HISTORICAL",
    "report_format": "CSV",
    "date_range": {
      "start_date_millis": 1627756241000,
      "end_date_millis": 1628274581000
    },
    "join_entities_by_integration": {
      "airwatch": ["application"]
    },
    "created_at": "2022-05-24T06:45:42.785Z",
    "created_by": "22345678-0000-0000-0000-100000000000",
    "modified_at": "2022-05-24T06:45:42.785Z",
    "entity_label": "Apps",
    "column_names": ["airwatch.application.app_name"],
    "total_schedules": 0,
    "total_downloads": 0,
    "total_recipients": 0,
    "created_by_details": {
      "id": "22345678-0000-0000-0000-100000000000",
      "display_name": "display-name-1-0",
      "UserName": "display-name-1-0"
    },
    "shared_report": false,
    "share_count": 0,
    "account_access_level": "FULL",
    "owner": true,
    "orphaned": false,
    "filter_condition": {
      "parenthesized": false,
      "nested_attribute": false,
      "custom_attribute": false,
      "attribute": "airwatch.application.app_dynamic_size_bytes",
      "operator": ">",
      "operands": [
        {
          "operand_type": "BasicOperand",
          "data_type": "LONG",
          "value": 5000000
        }
      ],
      "operand_collection_present": false
    }
  }
}
```

The PDF may include additional fields such as `filter_condition_nested_rules` on create-report responses.

### Create report — snapshot sample response (`POST /v2/reports`)

```json
{
  "data": {
    "id": "124985bb-e0fa-40d1-b2fb-de2f8e915e38",
    "name": "Test Report - V2 Joins",
    "description": "All managed and un-managed apps on devices with good antivirus status and half battery level",
    "integration": "airwatch",
    "entity": "application",
    "filter": " airwatch.device.device_enrollment_status = 'Enrolled' AND airwatch.device._device_antivirus_status IN ( 'Pass' ) AND airwatch.device.device_battery_percent = 50 ",
    "report_type": "SNAPSHOT",
    "report_format": "CSV",
    "join_entities_by_integration": {
      "airwatch": ["application", "device"]
    },
    "created_at": "2022-06-28T19:48:04.590Z",
    "created_by": "26f5d3cb-7f76-4c5e-aa20-57264ac17280",
    "modified_at": "2022-06-28T19:48:04.590Z",
    "entity_label": "Apps",
    "column_names": [
      "airwatch.application.app_name",
      "airwatch.device.device_friendly_name",
      "airwatch.device.device_platform",
      "airwatch.device.device_os_version",
      "airwatch.application.app_version",
      "airwatch.application.app_package_id",
      "airwatch.application.app_install_status",
      "airwatch.application.app_install_status_reason",
      "airwatch.device.device_app_sample_last_seen",
      "airwatch.application.app_last_seen",
      "airwatch.device.device_last_seen",
      "airwatch.application.app_is_managed",
      "airwatch.device.device_location_group_name",
      "airwatch.application.app_type",
      "airwatch.device.device_enrollment_status",
      "airwatch.application.app_bundle_size_bytes",
      "airwatch.application.app_is_installed"
    ],
    "total_schedules": 0,
    "total_downloads": 0,
    "total_recipients": 0,
    "created_by_details": {
      "id": "26f5d3cb-7f76-4c5e-aa20-57264ac17280",
      "display_name": "test15@xxx.com",
      "UserName": "test15@xxx.com"
    },
    "shared_report": false,
    "share_count": 0,
    "account_access_level": "FULL",
    "owner": true,
    "orphaned": false
  }
}
```

The PDF continues with nested `filter_condition` / `filter_condition_nested_rules` trees for this snapshot; they are omitted here for readability.

### Run report — sample response (`POST /v2/reports/{id}/run`)

```json
{
  "data": {
    "active": true,
    "created_at": "2022-06-03T17:28:24.554Z",
    "created_by": "f65716f4-0d44-4c50-8cca-05d1306fbf77",
    "cron_expression_detail": {
      "frequency": "ONCE"
    },
    "id": "749b30e0-6e75-4d58-ba90-3e175e2b8b8e",
    "modified_at": "2022-06-03T17:28:24.554Z",
    "modified_by": "f65716f4-0d44-4c50-8cca-05d1306fbf77",
    "name": "Single run report request 5f5abb88-ea63-43bf-8738-ed0c6a7b345a",
    "report_id": "20602124-f68b-4dd5-949a-0e45b3d265b0",
    "schedule_type": "ADHOC",
    "start": "2022-06-03T17:28:24.553Z"
  }
}
```

### Schedule reports — sample response (`POST /v2/reports/schedules`)

```json
{
  "data": {
    "active": true,
    "created_at": "2022-06-03T18:24:56.199Z",
    "created_by": "f65716f4-0d44-4c50-8cca-05d1306fbf77",
    "cron_expression_detail": {
      "frequency": "HOURLY",
      "hourly": {
        "interval": 4
      }
    },
    "id": "5a384bd7-9ac4-46bb-a810-59e0b498d99f",
    "modified_at": "2022-06-03T18:24:56.199Z",
    "modified_by": "f65716f4-0d44-4c50-8cca-05d1306fbf77",
    "name": "Schedule Test Hourly",
    "report_id": "20602124-f68b-4dd5-949a-0e45b3d265b0",
    "schedule_type": "CRON",
    "start": "2022-06-03T19:00:00.000Z"
  }
}
```

### Available downloads — sample response (`POST /v2/reports/{id}/downloads/search`)

```json
{
  "data": {
    "offset": 0,
    "page_size": 100,
    "total_count": 2,
    "results": [
      {
        "created_at": "2022-06-03T17:28:47.146Z",
        "created_by": "f65716f4-0d44-4c50-8cca-05d1306fbf77",
        "id": "416c1890-70d5-4261-a440-d2dc402e52cf",
        "location": "reports/538f619e-2db4-4f07-974b-efb3e5326116/5f2c2fa1-e9ec-4c55-9649-b3fbabf4d116/BK---API-Test1---Enrolled-Devices-2019-06-03-17-28-UTC.csv",
        "modified_at": "2022-06-03T17:29:01.873Z",
        "modified_by": "11223344-5500-0000-0000-000000000000",
        "processing_time_millis": 12660,
        "report_id": "5f2c2fa1-e9ec-4c55-9649-b3fbabf4d116",
        "report_schedule_id": "749b30e0-6e75-4d58-ba90-3e175e2b8b8e",
        "start_time": "2022-06-03T17:28:47.740Z",
        "status": "COMPLETED"
      },
      {
        "created_at": "2022-06-03T17:13:15.545Z",
        "created_by": "f65716f4-0d44-4c50-8cca-05d1306fbf77",
        "id": "397e00fb-5c32-439d-b4fc-a657458c9f6d",
        "location": "reports/538f619e-2db4-4f07-974b-efb3e5326116/5f2c2fa1-e9ec-4c55-9649-b3fbabf4d116/BK---API-Test1---Enrolled-Devices-2019-06-03-17-13-UTC.csv",
        "modified_at": "2022-06-03T17:13:33.616Z",
        "modified_by": "11223344-5500-0000-0000-000000000000",
        "processing_time_millis": 13967,
        "report_id": "20602124-f68b-4dd5-949a-0e45b3d265b0",
        "report_schedule_id": "600300be-7958-4158-a550-dcca31186fd4",
        "start_time": "2022-06-03T17:13:17.546Z",
        "status": "COMPLETED"
      }
    ]
  }
}
```

### Download report — sample responses

**Step 1 — get signed URL (`GET /v2/reports/tracking/{tracking_id}/download`)**

HTTP **302 Found** with an empty body and a `Location` header pointing at time-limited storage (example host/path from the PDF: `https://storage.{environment}/reports/...csv?...`).

**Step 2 — follow redirect**

HTTP **200 OK** with `Content-Type: application/octet-stream` and the report bytes (PDF shows `content-length` and ellipses for the payload).

### Report preview — sample response (`POST /v2/reports/{id}/preview`)

```json
{
  "data": {
    "page_size": 25,
    "offset": 0,
    "total_count": 6385,
    "results": [
      {
        "airwatch.device.device_enrollment_user_name": "ws1intel.bda44ae7-66eb-42c2-899a-d2af3685d8e2",
        "airwatch.device.device_friendly_name": "KENYATTA's HP Elite x3",
        "airwatch.windowspatch.winpatch_revision_id": 228923,
        "airwatch.windowspatch.winpatch_update_id": "8c196037-dbb0-4eaa-9e0f-254bf83bebe2",
        "airwatch.windowspatch.winpatch_kb_number": 2124261,
        "airwatch.windowspatch.winpatch_update_status": "Unknown",
        "airwatch.windowspatch.winpatch_approval_status": "approved",
        "airwatch.windowspatch.winpatch_assignment_status": "assigned",
        "airwatch.windowspatch.winpatch_update_classification": "CriticalUpdates",
        "airwatch.windowspatch.winpatch_approved_date": 1606984113000,
        "airwatch.windowspatch.winpatch_publish_date": 1623955447000,
        "airwatch.device.device_enrollment_date": 1472357078000,
        "airwatch.device.device_enrollment_status": "EnrollmentInProgress",
        "airwatch.device.device_last_seen": 1651512997000,
        "airwatch.device.device_enrollment_user_email": "9ddfe9b1-b623-46b1-9bfc-a0081d1e4311@ws1.intelligent.staging.dpa0.org",
        "airwatch.device.device_os_version": "9.0.4",
        "airwatch.device.device_model": "HP Elite x3"
      }
    ]
  }
}
```

### Report search — sample response (`POST /v2/reports/search`)

```json
{
  "data": {
    "page_size": 10,
    "offset": 0,
    "total_count": 130,
    "results": [
      {
        "id": "31118250-7d6a-4bb2-befb-72f50e47d3b9",
        "name": "Windows Antivirus Updates",
        "description": "Devices with good antivirus status",
        "integration": "airwatch",
        "entity": "windowspatch",
        "filter": " airwatch.device._device_antivirus_status IN ( 'Pass' ) AND airwatch.windowspatch._device_os_version = '10.0.1' ",
        "report_type": "SNAPSHOT",
        "report_format": "CSV",
        "created_at": "2022-06-09T07:14:29.441Z",
        "created_by": "26f5d3cb-7f76-4c5e-aa20-57264ac17280",
        "modified_at": "2022-06-09T07:14:29.441Z",
        "entity_label": "Windows OS Updates",
        "column_names": [
          "airwatch.device.device_enrollment_user_name",
          "airwatch.device.device_friendly_name",
          "airwatch.windowspatch.winpatch_revision_id",
          "airwatch.windowspatch.winpatch_update_id",
          "airwatch.windowspatch.winpatch_update_status",
          "airwatch.windowspatch.winpatch_approval_status",
          "airwatch.windowspatch.winpatch_assignment_status",
          "airwatch.device.device_enrollment_date",
          "airwatch.device.device_enrollment_status",
          "airwatch.device.device_last_seen",
          "airwatch.device.device_enrollment_user_email",
          "airwatch.device.device_model",
          "airwatch.windowspatch.winpatch_kb_subject",
          "airwatch.windowspatch.winpatch_update_type"
        ],
        "total_schedules": 1,
        "total_downloads": 1,
        "total_recipients": 1,
        "shared_report": false,
        "share_count": 0,
        "account_access_level": "FULL",
        "owner": true,
        "orphaned": false,
        "filter_condition": {
          "parenthesized": false,
          "nested_attribute": false,
          "custom_attribute": false,
          "operand_collection_present": false,
          "logical_operator": "AND",
          "lhs": {
            "parenthesized": false,
            "nested_attribute": false,
            "custom_attribute": false,
            "attribute": "airwatch.device._device_antivirus_status",
            "operator": "IN",
            "operands": [
              {
                "operand_type": "BasicOperand",
                "data_type": "STRING",
                "value": "Pass"
              }
            ],
            "operand_collection_present": true
          },
          "rhs": {
            "parenthesized": false,
            "nested_attribute": false,
            "custom_attribute": false,
            "attribute": "airwatch.windowspatch._device_os_version",
            "operator": "=",
            "operands": [
              {
                "operand_type": "BasicOperand",
                "data_type": "STRING",
                "value": "10.0.1"
              }
            ],
            "operand_collection_present": false
          }
        }
      }
    ]
  }
}
```

### Set report recipients — sample response (`POST /v2/reports/{id}/recipients`)

```json
{
  "data": {
    "report_id": "5f2c2fa1-e9ec-4c55-9649-b3fbabf4d116",
    "recipients": [
      {
        "created_at": "2022-06-03T18:10:51.752Z",
        "created_by": "f65716f4-0d44-4c50-8cca-05d1306fbf77",
        "email": "margaret.thatcher@omnissa.com"
      },
      {
        "created_at": "2022-06-03T18:10:51.752Z",
        "created_by": "f65716f4-0d44-4c50-8cca-05d1306fbf77",
        "email": "paul.revere@omnissa.com"
      }
    ]
  }
}
```

### Get report recipients — sample response (`GET /v2/reports/{id}/recipients`)

Same JSON shape as **Set report recipients** above (the PDF illustrates `GET` returning the stored recipients list).
