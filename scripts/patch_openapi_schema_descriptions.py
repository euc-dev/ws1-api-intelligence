#!/usr/bin/env python3
"""Align components.schemas property descriptions with DHUB PDF extract text."""

import json
from pathlib import Path


def _set_description(obj: dict | None, description: str) -> None:
    """Set description only when missing (idempotent re-runs)."""
    if obj is not None and not obj.get("description"):
        obj["description"] = description


def _patch_allof_property(schema: dict, property_name: str, description: str) -> bool:
    """Patch a property nested in an allOf composition, if present."""
    for item in schema.get("allOf") or []:
        props = item.get("properties") or {}
        if property_name in props:
            _set_description(props[property_name], description)
            return True
    return False


def _patch_path_parameters(spec: dict) -> None:
    """Add PDF-aligned descriptions for operation parameters (mostly path params)."""
    paths = spec.get("paths") or {}
    for path_key, path_item in paths.items():
        for method, op in path_item.items():
            if method.startswith("x-") or not isinstance(op, dict):
                continue
            for param in op.get("parameters") or []:
                if param.get("description"):
                    continue
                pname = param.get("name")
                pin = param.get("in")
                if pin != "path" or not pname:
                    continue

                if pname == "name" and "/v2/metadata/entity/" in path_key:
                    _set_description(param, (
                        '"name" is "entity_name" that can be learned from Entities API.'
                    ))
                elif pname == "entity" and path_key.startswith("/v2/metrics/entity/"):
                    _set_description(param, (
                        "Entity name and this is a required field. This can be known from Entities "
                        "API. Non empty String and a valid entity name."
                    ))
                elif pname == "integration" and "/v2/meta/integration/" in path_key:
                    _set_description(param, (
                        "Identifies the integration from which the data will be sourced."
                    ))
                elif pname == "entity" and "/v2/meta/integration/" in path_key:
                    _set_description(param, (
                        "Identifies the entity from which the data will be sourced."
                    ))
                elif pname == "report_id":
                    _set_description(param, (
                        "The report identifier obtained via the Create Report API."
                    ))
                elif pname == "tracking_id":
                    _set_description(param, (
                        'Report tracking identifier from the Available downloads API results ("id" '
                        "field)."
                    ))
                elif pname == "id" and path_key.startswith("/v2/reports/"):
                    _set_description(param, "Report identifier.")

            for resp_key, resp in op.get("responses", {}).items():
                if not isinstance(resp, dict):
                    continue
                loc = (resp.get("headers") or {}).get("Location")
                if isinstance(loc, dict):
                    _set_description(loc, (
                        "The response is an HTTP redirect to a secure URL where the report contents "
                        "can be downloaded (Location header)."
                    ))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    p = root / "docs" / "intelligence-rest-api-swagger.json"
    spec = json.loads(p.read_text())
    schemas = spec["components"]["schemas"]

    _set_description(schemas["ErrorItem"]["properties"]["code"], (
        "The error code indicating the type of error."
    ))
    _set_description(schemas["ErrorItem"]["properties"]["message"], (
        "More information about the specific error."
    ))
    _set_description(schemas["ErrorItem"]["properties"]["violated_property"], (
        "A specific property name (if applicable)."
    ))

    _set_description(schemas["ErrorResponse"]["properties"]["errors"], (
        "Errors is an array with code, message, and violated_property fields."
    ))

    _set_description(schemas["SortOn"]["properties"]["field"], "The field to sort on.")
    _set_description(schemas["SortOn"]["properties"]["order"], (
        "The sort order (ASC or DESC)."
    ))

    _set_description(schemas["SearchTerm"]["properties"]["value"], (
        "String value used for searching."
    ))
    _set_description(schemas["SearchTerm"]["properties"]["fields"], (
        "Optional Array of fields to search the value."
    ))
    _set_description(schemas["SearchTerm"]["properties"]["operator"], (
        'Optional Search operator specified as a String. This can accept one of the three '
        'values : "START_WITH", "CONTAINS", "ENDS_WITH". Default "CONTAINS".'
    ))

    _set_description(schemas["PagingOnlyBody"]["properties"]["offset"], (
        "Offset across the entire data set at which the current page starts."
    ))
    _set_description(schemas["PagingOnlyBody"]["properties"]["page_size"], (
        "The number of records to return. Min and max values are listed in the Paging section."
    ))

    _set_description(schemas["EntitiesQueryRequest"], (
        "Request information requires following fields in a JSON body."
    ))
    eq = schemas["EntitiesQueryRequest"]["properties"]
    _set_description(eq["offset"], (
        "Offset across the entire data set at which the current page starts."
    ))
    _set_description(eq["page_size"], "Min and max values are listed in the Paging section.")
    _set_description(eq["sort_ons"], (
        "Optional: An ordered array ascending order of fields to sort on. Valid sort field: "
        "entity is the only sortable field."
    ))
    _set_description(eq["search_terms"], (
        'Optional: An array of search terms and the corresponding fields which should be inspected. '
        'Must be a searchable field; "name" is the only searchable field so only one search term '
        "is expected in the request."
    ))

    _set_description(schemas["AttributesQueryRequest"], (
        'Request requires following information in a JSON request body. "name" is "entity_name" '
        "that can be learned from Entities API which is a required field and if not provided will "
        "result in validation error response."
    ))
    aq = schemas["AttributesQueryRequest"]["properties"]
    _set_description(aq["offset"], (
        "Offset across the entire data set at which the current page starts."
    ))
    _set_description(aq["page_size"], "Min and max values are listed in the Paging section.")
    _set_description(aq["sort_ons"], (
        'Optional: An ordered array ascending order of fields to sort on. Valid sort field: "name" '
        "is the only allowed sort field."
    ))
    _set_description(aq["search_terms"], (
        'Optional: An array of search terms and the corresponding fields which should be inspected. '
        'Only searchable field, so only one search term is expected in the request. "name" is the '
        "searchable field."
    ))

    _set_description(schemas["EntitySummary"]["properties"]["name"], "Name of entity.")
    _set_description(schemas["EntitySummary"]["properties"]["label"], (
        "User friendly/well known name of entity."
    ))
    _set_description(schemas["EntitySummary"]["properties"]["description"], (
        "Description of that entity."
    ))

    pe = schemas["PagedEntityResultsWrapper"]["properties"]["data"]["properties"]
    _set_description(pe["offset"], (
        "Offset across the entire data set at which the current page starts."
    ))
    _set_description(pe["page_size"], "Min and max values are listed in the section.")
    _set_description(pe["total_count"], "Total count of result set.")
    _set_description(pe["results"], (
        "An array of entities. Details are provided in the following table."
    ))

    _set_description(schemas["AttributeSummary"]["properties"]["name"], "Name of the attribute.")
    _set_description(schemas["AttributeSummary"]["properties"]["label"], (
        "Label gives better understanding of attribute name."
    ))
    _set_description(schemas["AttributeSummary"]["properties"]["description"], (
        "Description of the attribute."
    ))
    _set_description(schemas["AttributeSummary"]["properties"]["data_type"], (
        "Attribute data type."
    ))
    _set_description(schemas["AttributeSummary"]["properties"]["bucketing_allowed"], (
        "Bucketing / Filtering for Metrics API will be allowed only when the value is true "
        "for the attribute."
    ))

    pa = schemas["PagedAttributeResultsWrapper"]["properties"]["data"]["properties"]
    _set_description(pa["entity"], "Entity from request.")
    _set_description(pa["offset"], (
        "Offset across the entire data set at which the current page starts."
    ))
    _set_description(pa["page_size"], "Min and max values are listed in the section.")
    _set_description(pa["total_count"], "Total count of result set.")
    _set_description(pa["results"], (
        "Array of attributes for the requested entity. The description and fields for each "
        "attribute in the list is mentioned in the following table."
    ))

    _set_description(schemas["Timespan"], (
        'timespan { "duration" : duration of the request, "unit" : time unit }. Mentions the span '
        "of time to calculate metrics. Accepted time units and sample are provided in the "
        "following table. Valid Time Units : Seconds, Minutes, Hours, Days, Weeks, Months, Years."
    ))
    _set_description(schemas["Timespan"]["properties"]["duration"], "duration of the request.")
    _set_description(schemas["Timespan"]["properties"]["unit"], (
        "time unit. Valid Time Units : Seconds, Minutes, Hours, Days, Weeks, Months, Years."
    ))

    tw = schemas["TimeWindow"]["properties"]
    _set_description(tw["type"], (
        'Optional; used for rolling window requests (for example type "rolling_window").'
    ))
    _set_description(tw["timespan"], (
        "Mentions the span of time to calculate metrics. Accepted time units and sample are "
        "provided in the following table. Optional, either this or start_time are mandatory in "
        "the request."
    ))
    _set_description(tw["start_time"], (
        'Date in the format "yyyy-mm ddTHH:MM:SSz". Optional. Either this or timespan should be '
        "present. Otherwise results in validation error."
    ))
    _set_description(tw["end_time"], (
        'Date in the format "yyyy-mm ddTHH:MM:SSz". Optional, if not provided considered as '
        "current time."
    ))

    _set_description(schemas["MetricDefinition"]["properties"]["name"], (
        'Fully qualified attribute name known from the Attributes Metadata API. Required with '
        '"function".'
    ))
    _set_description(schemas["MetricDefinition"]["properties"]["function"], (
        "Aggregation function per Supported Metrics (AVG, SUM, MIN, MAX, COUNT, COUNT_DISTINCT). "
        "Should be one of the aggregation listed functions."
    ))
    _set_description(schemas["MetricDefinition"], (
        "Specifies metric name and aggregation function. If metrics are requested with unsupported "
        "metric type or on attributes with datatypes that are not supported, HTTP 400 error response "
        "will be returned with appropriate error message."
    ))

    _set_description(schemas["EntityMetricsRequest"], (
        "Payload for any entity metrics end point have the following common parameters."
    ))
    em = schemas["EntityMetricsRequest"]["properties"]
    _set_description(em["entity"], (
        "Entity name and this is a required field. This can be known from Entities API. "
        "Non empty String and a valid entity name."
    ))
    _set_description(em["time_window"], (
        "This object takes time range in one of the time span or date range with start and end "
        "time or just start time. This is required and if none are provided in the request it "
        "results in validation error. Validation of date values or time span: 1) The timewindow "
        "cannot exceed 90 days. 2) Either start_time or Timespan should be present in the request "
        "but not both. 3) Only end_time is not valid."
    ))
    _set_description(em["date_attribute_name"], (
        "Optional date field to be used for computing metrics and the data type of the attribute "
        "should be date."
    ))
    _set_description(em["metrics"], (
        'Specifies an array of the metric function to be applied on the attribute. The attributes '
        "can be known from the Attributes Metadata API. This is a required object and takes "
        '"name" and "function" required fields. Upto 5 metrics are allowed in each request. At this '
        "point only one Metric is supported."
    ))
    _set_description(em["filter"], (
        "String of filter attributes that follows ANTLR grammar. Optional. Only attributes that "
        "have set bucketing/filtering to true from Attributes API are allowed."
    ))
    _set_description(em["bucketing_attributes"], (
        "Array of grouping attributes known from Attributes Metadata API. Metrics will be returned "
        "within the time range for each bucket. Optional. Maximum of 10 bucketing attributes per "
        "request are allowed but the more the number of bucketing attributes, number of buckets per "
        "data point will be less. Currently this field is not supported for Rolling window type "
        "requests. If provided in the request, it will be ignored."
    ))
    _set_description(em["num_results_per_bucketing_attribute"], (
        'An optional field that defines number of buckets per data point. A data point corresponds '
        'to sampling interval size. "simple_timerange" will have one data point and "histogram" or '
        '"rolling window" number of data points is based on number of sampling intervals. Default '
        "value is set to 20 and maximum value is set 500."
    ))

    _set_description(schemas["SamplingInterval"], (
        'Similar to timespan. Accepted time units are "HOURS" and "DAYS". The interval size should '
        "be within the requested time range otherwise results in validation error."
    ))
    _set_description(schemas["SamplingInterval"]["properties"]["duration"], (
        "Duration for the sampling interval."
    ))
    _set_description(schemas["SamplingInterval"]["properties"]["unit"], (
        'Accepted time units are "HOURS" and "DAYS".'
    ))

    sampling_interval_desc = schemas["SamplingInterval"]["description"]
    if not _patch_allof_property(
        schemas["HistogramMetricsPayload"], "sampling_interval", sampling_interval_desc
    ):
        _set_description(
            schemas["HistogramMetricsPayload"].get("properties", {}).get("sampling_interval"),
            sampling_interval_desc,
        )

    _set_description(
        schemas["HistogramMetricsRequestWrapper"],
        "JSON body uses a data object wrapping the histogram metrics payload (Histogram Requests).",
    )
    _set_description(
        schemas["HistogramMetricsRequestWrapper"]["properties"]["data"],
        "Histogram metrics request fields including sampling_interval.",
    )

    rw = schemas["RollingWindowMetricsRequestWrapper"]
    _set_description(
        rw,
        'Note : "bucketing_attributes" is currently not supported for rolling window requests and '
        "will be ignored if present in the request.",
    )
    window_size_desc = (
        'Required. This also takes duration for window size and time unit similar to '
        'sampling interval. Accepted time units are "HOURS" and "DAYS".'
    )
    if not _patch_allof_property(rw, "window_size", window_size_desc):
        _set_description(rw.get("properties", {}).get("window_size"), window_size_desc)

    _set_description(
        schemas["SimpleTimerangeMetricsRequestWrapper"]["properties"]["data"],
        "Entity metrics fields as defined for Entity Metrics API (wrapped in data).",
    )

    _set_description(schemas["MetricsResultEnvelope"], "Response has the following fields.")
    for result_schema_name in ("MetricsResultData", "RollingWindowMetricsResultData"):
        data_props = schemas[result_schema_name]["properties"]
        _set_description(data_props["entity"], "entity received in request.")
        _set_description(
            data_props["result_type"],
            "Result type is the request end point type sent back in response.",
        )
        _set_description(
            data_props["is_complete_dataset"],
            "If this field is present it indicates that entire dataset is not returned in response "
            "and to retrieve additional data, request should be adjusted (time window or sampling "
            "interval size or cardinality) and re tried.",
        )
        _set_description(
            data_props["result"],
            "Array of response objects as shown in the API documentation. Each object includes "
            "start_time, end_time, bucketing_attributes (if applicable), and metrics_values.",
        )

    _set_description(schemas["ReportAttributeMetadataResponse"], (
        "A meta-data API response listing attributes available for a particular integration and "
        "entity."
    ))
    _set_description(schemas["ReportAttributeMetadataResponse"]["properties"]["data"], (
        "Array of attribute metadata entries as described in Report Metadata API sample responses."
    ))

    cr = schemas["CreateReportRequest"]
    _set_description(cr, (
        "Report creation requires the following information get encoded in a JSON request body."
    ))
    cp = cr["properties"]
    _set_description(cp["name"], (
        "Free-form text string naming the report. It must be unique within the context of a "
        "customer."
    ))
    _set_description(cp["description"], "Free-form text string describing the report.")
    _set_description(cp["integration"], (
        "Identifies the integration from which the data will be sourced."
    ))
    _set_description(cp["entity"], "Identifies the entity from which the data will be sourced.")
    _set_description(cp["column_names"], (
        "An array of column names. Indicates the attributes of corresponding integration and entity "
        "that will appear in the report. Note: Column names are expected to be fully qualified."
    ))
    _set_description(cp["filter"], (
        "A filter expression. Filters the data based on the expression, so the data matching the "
        "criteria appears in the report. Note: column names in the filter conditions should also "
        "match the format."
    ))
    _set_description(cp["report_type"], (
        "Report type. Possible values are HISTORICAL and SNAPSHOT. Indicates the type of the "
        "report being created."
    ))
    _set_description(cp["report_format"], (
        "Report format. Supported formats are CSV and JSONL. Indicates the output format of the "
        "report being created."
    ))
    _set_description(cp["date_range"], (
        "Date range for HISTORICAL report type. Indicates the date range for time-series data. "
        "Required for HISTORICAL report type. Request body can have date range in formats "
        "documented for Last 12 hours, Last 7 days, or Custom (custom time period can be maximum "
        "28 days)."
    ))
    _set_description(cp["join_entities_by_integration"], (
        "Mapping of integration to corresponding entity list. Enables creating reports requiring "
        "multi entity joins. Optional, computed based on entities involved."
    ))
    _set_description(cp["recipients"], (
        "An array of email address objects. Indicates who should receive the output of the report."
    ))
    _set_description(
        schemas.get("ReportRecipient", {}).get("properties", {}).get("email"),
        "Recipient email address.",
    )

    rd = schemas["ReportDetail"]
    rdp = rd["properties"]
    _set_description(rdp["id"], (
        "Report identifier used with Run Reports API, schedules, downloads, and related calls."
    ))
    _set_description(rdp["name"], "Free-form text string naming the report.")
    _set_description(rdp["description"], "Free-form text string describing the report.")
    _set_description(rdp["integration"], (
        "Identifies the integration from which the data will be sourced."
    ))
    _set_description(rdp["entity"], "Identifies the entity from which the data will be sourced.")
    _set_description(rdp["filter"], "Filter expression applied to the report.")
    _set_description(rdp["report_type"], "Report type (HISTORICAL or SNAPSHOT).")
    _set_description(rdp["report_format"], "Report format (CSV or JSONL).")
    _set_description(rdp["column_names"], (
        "Attributes (fully qualified) included in the report."
    ))
    _set_description(rdp["created_at"], "Created timestamp.")
    _set_description(rdp["modified_at"], "Modified timestamp.")
    _set_description(rdp["total_schedules"], "Total schedules associated with the report.")
    _set_description(rdp["total_downloads"], "Total downloads associated with the report.")
    _set_description(rdp["total_recipients"], "Total recipients associated with the report.")

    _set_description(schemas["ReportDetailWrapper"], (
        "Standard wrapper with data containing report details."
    ))

    _set_description(schemas["ReportRunResponseWrapper"], (
        "Run report API response body including schedule-related fields for an ADHOC or scheduled "
        "run."
    ))

    csr = schemas["CreateReportScheduleRequest"]
    _set_description(csr, (
        "Report Schedule creation requires the following information get encoded in a JSON request "
        "body."
    ))
    csp = csr["properties"]
    _set_description(csp["name"], "The schedule name.")
    _set_description(csp["report_id"], "The report ID returned by the Create Report API.")
    _set_description(csp["schedule_type"], (
        "Schedule type: CRON (meaning scheduled) or ADHOC per API Documentation."
    ))
    _set_description(csp["start"], (
        "The time at which the schedule takes effect (maybe be in the future)."
    ))
    _set_description(csp["cron_expression_detail"], (
        "Cron expression detail specifying frequency (ONCE, HOURLY, DAILY, WEEKLY, MONTHLY, "
        "YEARLY) per Additional Scheduling Options in the API documentation."
    ))

    _set_description(schemas["ReportScheduleWrapper"], (
        "Response includes schedule fields such as id (internal report schedule ID), active, "
        "created_at, cron_expression_detail, report_id, schedule_type, start."
    ))

    rdr = schemas["ReportDownloadRecord"]
    rdrp = rdr["properties"]
    _set_description(rdrp["id"], (
        "Report tracking identifier used with GET /v2/reports/tracking/{tracking_id}/download."
    ))
    _set_description(rdrp["report_id"], "Associated report id.")
    _set_description(rdrp["status"], 'Processing status (for example "COMPLETED").')
    _set_description(rdrp["location"], "Storage location path for the report output.")
    _set_description(rdrp["start_time"], "Start time for the report processing run.")
    _set_description(rdrp["processing_time_millis"], "Processing duration in milliseconds.")

    _set_description(schemas["ReportDownloadsSearchWrapper"], (
        'Lists downloads with paging; JSON body provides "report tracking" identifiers for '
        "completed runs available for download."
    ))
    rds = schemas["ReportDownloadsSearchWrapper"]["properties"]["data"]["properties"]
    _set_description(rds["offset"], "Offset reflected from request paging parameters.")
    _set_description(rds["page_size"], "Page size reflected from request paging parameters.")
    _set_description(rds["total_count"], "Total count of download records.")
    _set_description(rds["results"], (
        "Download records whose identifiers can be used to download report contents now or at any "
        "other point in the future."
    ))

    _set_description(schemas["ReportPreviewWrapper"], (
        "Paged preview rows for a report (Report preview API)."
    ))
    rpw = schemas["ReportPreviewWrapper"]["properties"]["data"]["properties"]
    _set_description(rpw["page_size"], "Page size for preview results.")
    _set_description(rpw["offset"], "Offset for preview results.")
    _set_description(rpw["total_count"], "Total rows available for preview.")
    _set_description(rpw["results"], (
        "Array of row objects with fully qualified column keys."
    ))

    _set_description(schemas["ReportsSearchBody"], (
        "Report search API JSON request body with paging and optional sort_ons."
    ))
    rsb = schemas["ReportsSearchBody"]["properties"]
    _set_description(rsb["offset"], (
        "Offset across the entire data set at which the current page starts."
    ))
    _set_description(rsb["page_size"], "The number of records to return per Paging rules.")
    _set_description(rsb["sort_ons"], "Optional sort specifications (field and ASC/DESC order).")

    _set_description(schemas["ReportsSearchWrapper"], (
        "Paged list of reports matching the search request."
    ))
    rsw = schemas["ReportsSearchWrapper"]["properties"]["data"]["properties"]
    _set_description(rsw["page_size"], "Page size in the response.")
    _set_description(rsw["offset"], "Offset in the response.")
    _set_description(rsw["total_count"], "Total reports matching the query.")
    _set_description(rsw["results"], "Array of report detail objects.")

    _set_description(schemas["ReportRecipientsBody"], (
        "Set Report recipients API — specify recipients for a report."
    ))
    _set_description(schemas["ReportRecipientsBody"]["properties"]["recipients"], (
        "Recipients who should receive report output (email objects)."
    ))

    _set_description(schemas["ReportRecipientsWrapper"], (
        "Get Report recipients API response listing recipients for a report."
    ))
    rrw = schemas["ReportRecipientsWrapper"]["properties"]["data"]["properties"]
    _set_description(rrw["report_id"], "Report identifier.")
    _set_description(rrw["recipients"], "Recipients associated with the report.")
    rrw_rec_items = rrw["recipients"].setdefault(
        "items",
        {"type": "object", "additionalProperties": True},
    )
    rrw_rec_items.setdefault("properties", {})
    ep = rrw_rec_items["properties"]
    ep.setdefault(
        "email",
        {"type": "string", "description": "Recipient email address."},
    )
    ep.setdefault(
        "created_at",
        {"type": "string", "description": "Created timestamp."},
    )
    ep.setdefault(
        "created_by",
        {"type": "string", "description": "Created by user identifier."},
    )

    _set_description(spec["components"]["responses"]["NotFound"], (
        "The resource you attempted to access does not exist."
    ))

    _patch_path_parameters(spec)

    _set_description(spec["servers"][0]["variables"]["region"], (
        "As a customer you will need to substitute the host name specific to the region in which "
        "your data resides."
    ))

    p.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {p}")


if __name__ == "__main__":
    main()
