#!/usr/bin/env python3
"""Align components.schemas property descriptions with DHUB PDF extract text."""

import json
from pathlib import Path


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
                    param["description"] = (
                        '"name" is "entity_name" that can be learned from Entities API.'
                    )
                elif pname == "entity" and path_key.startswith("/v2/metrics/entity/"):
                    param["description"] = (
                        "Entity name and this is a required field. This can be known from Entities "
                        "API. Non empty String and a valid entity name."
                    )
                elif pname == "integration" and "/v2/meta/integration/" in path_key:
                    param["description"] = (
                        "Identifies the integration from which the data will be sourced."
                    )
                elif pname == "entity" and "/v2/meta/integration/" in path_key:
                    param["description"] = (
                        "Identifies the entity from which the data will be sourced."
                    )
                elif pname == "report_id":
                    param["description"] = (
                        "The report identifier obtained via the Create Report API."
                    )
                elif pname == "tracking_id":
                    param["description"] = (
                        'Report tracking identifier from the Available downloads API results ("id" '
                        "field)."
                    )
                elif pname == "id" and path_key.startswith("/v2/reports/"):
                    param["description"] = "Report identifier."

            for resp_key, resp in op.get("responses", {}).items():
                if not isinstance(resp, dict):
                    continue
                loc = (resp.get("headers") or {}).get("Location")
                if isinstance(loc, dict):
                    loc["description"] = (
                        "The response is an HTTP redirect to a secure URL where the report contents "
                        "can be downloaded (Location header)."
                    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    p = root / "docs" / "intelligence-rest-api-swagger.json"
    spec = json.loads(p.read_text())
    schemas = spec["components"]["schemas"]

    schemas["ErrorItem"]["properties"]["code"]["description"] = (
        "The error code indicating the type of error."
    )
    schemas["ErrorItem"]["properties"]["message"]["description"] = (
        "More information about the specific error."
    )
    schemas["ErrorItem"]["properties"]["violated_property"]["description"] = (
        "A specific property name (if applicable)."
    )

    schemas["ErrorResponse"]["properties"]["errors"]["description"] = (
        "Errors is an array with code, message, and violated_property fields."
    )

    schemas["SortOn"]["properties"]["field"]["description"] = "The field to sort on."
    schemas["SortOn"]["properties"]["order"]["description"] = (
        "The sort order (ASC or DESC)."
    )

    schemas["SearchTerm"]["properties"]["value"]["description"] = (
        "String value used for searching."
    )
    schemas["SearchTerm"]["properties"]["fields"]["description"] = (
        "Optional Array of fields to search the value."
    )
    schemas["SearchTerm"]["properties"]["operator"]["description"] = (
        'Optional Search operator specified as a String. This can accept one of the three '
        'values : "START_WITH", "CONTAINS", "ENDS_WITH". Default "CONTAINS".'
    )

    schemas["PagingOnlyBody"]["properties"]["offset"]["description"] = (
        "Offset across the entire data set at which the current page starts."
    )
    schemas["PagingOnlyBody"]["properties"]["page_size"]["description"] = (
        "The number of records to return. Min and max values are listed in the Paging section."
    )

    schemas["EntitiesQueryRequest"]["description"] = (
        "Request information requires following fields in a JSON body."
    )
    eq = schemas["EntitiesQueryRequest"]["properties"]
    eq["offset"]["description"] = (
        "Offset across the entire data set at which the current page starts."
    )
    eq["page_size"]["description"] = "Min and max values are listed in the Paging section."
    eq["sort_ons"]["description"] = (
        "Optional: An ordered array ascending order of fields to sort on. Valid sort field: "
        "entity is the only sortable field."
    )
    eq["search_terms"]["description"] = (
        'Optional: An array of search terms and the corresponding fields which should be inspected. '
        'Must be a searchable field; "name" is the only searchable field so only one search term '
        "is expected in the request."
    )

    schemas["AttributesQueryRequest"]["description"] = (
        'Request requires following information in a JSON request body. "name" is "entity_name" '
        "that can be learned from Entities API which is a required field and if not provided will "
        "result in validation error response."
    )
    aq = schemas["AttributesQueryRequest"]["properties"]
    aq["offset"]["description"] = (
        "Offset across the entire data set at which the current page starts."
    )
    aq["page_size"]["description"] = "Min and max values are listed in the Paging section."
    aq["sort_ons"]["description"] = (
        'Optional: An ordered array ascending order of fields to sort on. Valid sort field: "name" '
        "is the only allowed sort field."
    )
    aq["search_terms"]["description"] = (
        'Optional: An array of search terms and the corresponding fields which should be inspected. '
        'Only searchable field, so only one search term is expected in the request. "name" is the '
        "searchable field."
    )

    schemas["EntitySummary"]["properties"]["name"]["description"] = "Name of entity."
    schemas["EntitySummary"]["properties"]["label"]["description"] = (
        "User friendly/well known name of entity."
    )
    schemas["EntitySummary"]["properties"]["description"]["description"] = (
        "Description of that entity."
    )

    pe = schemas["PagedEntityResultsWrapper"]["properties"]["data"]["properties"]
    pe["offset"]["description"] = (
        "Offset across the entire data set at which the current page starts."
    )
    pe["page_size"]["description"] = "Min and max values are listed in the section."
    pe["total_count"]["description"] = "Total count of result set."
    pe["results"]["description"] = (
        "An array of entities. Details are provided in the following table."
    )

    schemas["AttributeSummary"]["properties"]["name"]["description"] = "Name of the attribute."
    schemas["AttributeSummary"]["properties"]["label"]["description"] = (
        "Label gives better understanding of attribute name."
    )
    schemas["AttributeSummary"]["properties"]["description"]["description"] = (
        "Description of the attribute."
    )
    schemas["AttributeSummary"]["properties"]["data_type"]["description"] = (
        "Attribute data type."
    )
    schemas["AttributeSummary"]["properties"]["bucketing_allowed"]["description"] = (
        "Bucketing / Filtering for Metrics API will be allowed only when the value is true "
        "for the attribute."
    )

    pa = schemas["PagedAttributeResultsWrapper"]["properties"]["data"]["properties"]
    pa["entity"]["description"] = "Entity from request."
    pa["offset"]["description"] = (
        "Offset across the entire data set at which the current page starts."
    )
    pa["page_size"]["description"] = "Min and max values are listed in the section."
    pa["total_count"]["description"] = "Total count of result set."
    pa["results"]["description"] = (
        "Array of attributes for the requested entity. The description and fields for each "
        "attribute in the list is mentioned in the following table."
    )

    schemas["Timespan"]["description"] = (
        'timespan { "duration" : duration of the request, "unit" : time unit }. Mentions the span '
        "of time to calculate metrics. Accepted time units and sample are provided in the "
        "following table. Valid Time Units : Seconds, Minutes, Hours, Days, Weeks, Months, Years."
    )
    schemas["Timespan"]["properties"]["duration"]["description"] = "duration of the request."
    schemas["Timespan"]["properties"]["unit"]["description"] = (
        "time unit. Valid Time Units : Seconds, Minutes, Hours, Days, Weeks, Months, Years."
    )

    tw = schemas["TimeWindow"]["properties"]
    tw["type"]["description"] = (
        'Optional; used for rolling window requests (for example type "rolling_window").'
    )
    tw["timespan"]["description"] = (
        "Mentions the span of time to calculate metrics. Accepted time units and sample are "
        "provided in the following table. Optional, either this or start_time are mandatory in "
        "the request."
    )
    tw["start_time"]["description"] = (
        'Date in the format "yyyy-mm ddTHH:MM:SSz". Optional. Either this or timespan should be '
        "present. Otherwise results in validation error."
    )
    tw["end_time"]["description"] = (
        'Date in the format "yyyy-mm ddTHH:MM:SSz". Optional, if not provided considered as '
        "current time."
    )

    schemas["MetricDefinition"]["properties"]["name"]["description"] = (
        'Fully qualified attribute name known from the Attributes Metadata API. Required with '
        '"function".'
    )
    schemas["MetricDefinition"]["properties"]["function"]["description"] = (
        "Aggregation function per Supported Metrics (AVG, SUM, MIN, MAX, COUNT, COUNT_DISTINCT). "
        "Should be one of the aggregation listed functions."
    )
    schemas["MetricDefinition"]["description"] = (
        "Specifies metric name and aggregation function. If metrics are requested with unsupported "
        "metric type or on attributes with datatypes that are not supported, HTTP 400 error response "
        "will be returned with appropriate error message."
    )

    schemas["EntityMetricsRequest"]["description"] = (
        "Payload for any entity metrics end point have the following common parameters."
    )
    em = schemas["EntityMetricsRequest"]["properties"]
    em["entity"]["description"] = (
        "Entity name and this is a required field. This can be known from Entities API. "
        "Non empty String and a valid entity name."
    )
    em["time_window"]["description"] = (
        "This object takes time range in one of the time span or date range with start and end "
        "time or just start time. This is required and if none are provided in the request it "
        "results in validation error. Validation of date values or time span: 1) The timewindow "
        "cannot exceed 90 days. 2) Either start_time or Timespan should be present in the request "
        "but not both. 3) Only end_time is not valid."
    )
    em["date_attribute_name"]["description"] = (
        "Optional date field to be used for computing metrics and the data type of the attribute "
        "should be date."
    )
    em["metrics"]["description"] = (
        'Specifies an array of the metric function to be applied on the attribute. The attributes '
        "can be known from the Attributes Metadata API. This is a required object and takes "
        '"name" and "function" required fields. Upto 5 metrics are allowed in each request. At this '
        "point only one Metric is supported."
    )
    em["filter"]["description"] = (
        "String of filter attributes that follows ANTLR grammar. Optional. Only attributes that "
        "have set bucketing/filtering to true from Attributes API are allowed."
    )
    em["bucketing_attributes"]["description"] = (
        "Array of grouping attributes known from Attributes Metadata API. Metrics will be returned "
        "within the time range for each bucket. Optional. Maximum of 10 bucketing attributes per "
        "request are allowed but the more the number of bucketing attributes, number of buckets per "
        "data point will be less. Currently this field is not supported for Rolling window type "
        "requests. If provided in the request, it will be ignored."
    )
    em["num_results_per_bucketing_attribute"]["description"] = (
        'An optional field that defines number of buckets per data point. A data point corresponds '
        'to sampling interval size. "simple_timerange" will have one data point and "histogram" or '
        '"rolling window" number of data points is based on number of sampling intervals. Default '
        "value is set to 20 and maximum value is set 500."
    )

    schemas["SamplingInterval"]["description"] = (
        'Similar to timespan. Accepted time units are "HOURS" and "DAYS". The interval size should '
        "be within the requested time range otherwise results in validation error."
    )
    schemas["SamplingInterval"]["properties"]["duration"]["description"] = (
        "Duration for the sampling interval."
    )
    schemas["SamplingInterval"]["properties"]["unit"]["description"] = (
        'Accepted time units are "HOURS" and "DAYS".'
    )

    for item in schemas["HistogramMetricsPayload"]["allOf"]:
        if item.get("type") == "object" and "sampling_interval" in item.get("properties", {}):
            item["properties"]["sampling_interval"]["description"] = schemas["SamplingInterval"][
                "description"
            ]
            break

    schemas["HistogramMetricsRequestWrapper"]["description"] = (
        "JSON body uses a data object wrapping the histogram metrics payload (Histogram Requests)."
    )
    schemas["HistogramMetricsRequestWrapper"]["properties"]["data"]["description"] = (
        "Histogram metrics request fields including sampling_interval."
    )

    schemas["RollingWindowMetricsRequestWrapper"]["description"] = (
        'Note : "bucketing_attributes" is currently not supported for rolling window requests and '
        "will be ignored if present in the request."
    )
    for item in schemas["RollingWindowMetricsRequestWrapper"]["allOf"]:
        if item.get("type") == "object" and "window_size" in item.get("properties", {}):
            item["properties"]["window_size"]["description"] = (
                'Required. This also takes duration for window size and time unit similar to '
                'sampling interval. Accepted time units are "HOURS" and "DAYS".'
            )
            break

    schemas["SimpleTimerangeMetricsRequestWrapper"]["properties"]["data"]["description"] = (
        "Entity metrics fields as defined for Entity Metrics API (wrapped in data)."
    )

    schemas["MetricsResultEnvelope"]["description"] = "Response has the following fields."
    data_props = schemas["MetricsResultEnvelope"]["properties"]["data"]["properties"]
    data_props["entity"]["description"] = "entity received in request."
    data_props["result_type"]["description"] = (
        "Result type is the request end point type sent back in response."
    )
    data_props["is_complete_dataset"]["description"] = (
        "If this field is present it indicates that entire dataset is not returned in response and "
        "to retrieve additional data, request should be adjusted (time window or sampling interval "
        "size or cardinality) and re tried."
    )
    data_props["metadata"]["description"] = (
        'This contains metadata for all the aggregation and bucketing attributes and '
        'date_attribute_name. Includes "date_attribute_name" and attributes map with label and '
        "data_type."
    )
    data_props["result"]["description"] = (
        "Array of response objects as shown in the API documentation. Each object includes "
        "start_time, end_time, bucketing_attributes (if applicable), and metrics_values."
    )
    data_props["result"]["items"] = {
        "type": "object",
        "description": (
            "Each object in result array: start_time — Start time for the metric will be returned "
            'in the format "yyyy-mm-ddTHH:MM:ssZ" if milliseconds equals 0. If milliseconds has '
            'value then format will be "yyyy-mm ddTHH:MM:ss.SSSZ". Start time and end time will be '
            "set to current time for non-time series/snapshot requests. "
            "end_time — End time for that metric will be returned in the format "
            '"yyyy mm-ddTHH:MM:ssZ" or if milliseconds has value then "yyyy-mm ddTHH:MM:ss.SSSZ". '
            "bucketing_attributes — This is returned only if request has bucketing attributes. "
            "This has key, value pairs for each bucketing attribute in the request. "
            "metrics_values — Array of objects that contain metric details from request and value "
            "whose type varies based on the aggregation functions listed in Supported Metrics."
        ),
        "additionalProperties": True,
    }

    schemas["ReportAttributeMetadataResponse"]["description"] = (
        "A meta-data API response listing attributes available for a particular integration and "
        "entity."
    )
    schemas["ReportAttributeMetadataResponse"]["properties"]["data"]["description"] = (
        "Array of attribute metadata entries as described in Report Metadata API sample responses."
    )

    cr = schemas["CreateReportRequest"]
    cr["description"] = (
        "Report creation requires the following information get encoded in a JSON request body."
    )
    cp = cr["properties"]
    cp["name"]["description"] = (
        "Free-form text string naming the report. It must be unique within the context of a "
        "customer."
    )
    cp["description"]["description"] = "Free-form text string describing the report."
    cp["integration"]["description"] = (
        "Identifies the integration from which the data will be sourced."
    )
    cp["entity"]["description"] = "Identifies the entity from which the data will be sourced."
    cp["column_names"]["description"] = (
        "An array of column names. Indicates the attributes of corresponding integration and entity "
        "that will appear in the report. Note: Column names are expected to be fully qualified."
    )
    cp["filter"]["description"] = (
        "A filter expression. Filters the data based on the expression, so the data matching the "
        "criteria appears in the report. Note: column names in the filter conditions should also "
        "match the format."
    )
    cp["report_type"]["description"] = (
        "Report type. Possible values are HISTORICAL and SNAPSHOT. Indicates the type of the "
        "report being created."
    )
    cp["report_format"]["description"] = (
        "Report format. Supported formats are CSV and JSONL. Indicates the output format of the "
        "report being created."
    )
    cp["date_range"]["description"] = (
        "Date range for HISTORICAL report type. Indicates the date range for time-series data. "
        "Required for HISTORICAL report type. Request body can have date range in formats "
        "documented for Last 12 hours, Last 7 days, or Custom (custom time period can be maximum "
        "28 days)."
    )
    cp["join_entities_by_integration"]["description"] = (
        "Mapping of integration to corresponding entity list. Enables creating reports requiring "
        "multi entity joins. Optional, computed based on entities involved."
    )
    cp["recipients"]["description"] = (
        "An array of email address objects. Indicates who should receive the output of the report."
    )
    rc_items = cp["recipients"].setdefault("items", {"type": "object", "properties": {}})
    rc_items.setdefault("properties", {})
    rc_items["properties"]["email"] = rc_items["properties"].get("email", {"type": "string"})
    if rc_items["properties"]["email"].get("format") != "email":
        rc_items["properties"]["email"]["format"] = "email"
    rc_items["properties"]["email"]["description"] = "Recipient email address."

    rd = schemas["ReportDetail"]
    rdp = rd["properties"]
    rdp["id"]["description"] = (
        "Report identifier used with Run Reports API, schedules, downloads, and related calls."
    )
    rdp["name"]["description"] = "Free-form text string naming the report."
    rdp["description"]["description"] = "Free-form text string describing the report."
    rdp["integration"]["description"] = (
        "Identifies the integration from which the data will be sourced."
    )
    rdp["entity"]["description"] = "Identifies the entity from which the data will be sourced."
    rdp["filter"]["description"] = "Filter expression applied to the report."
    rdp["report_type"]["description"] = "Report type (HISTORICAL or SNAPSHOT)."
    rdp["report_format"]["description"] = "Report format (CSV or JSONL)."
    rdp["column_names"]["description"] = (
        "Attributes (fully qualified) included in the report."
    )
    rdp["created_at"]["description"] = "Created timestamp."
    rdp["modified_at"]["description"] = "Modified timestamp."
    rdp["total_schedules"]["description"] = "Total schedules associated with the report."
    rdp["total_downloads"]["description"] = "Total downloads associated with the report."
    rdp["total_recipients"]["description"] = "Total recipients associated with the report."

    schemas["ReportDetailWrapper"]["description"] = (
        "Standard wrapper with data containing report details."
    )

    schemas["ReportRunResponseWrapper"]["description"] = (
        "Run report API response body including schedule-related fields for an ADHOC or scheduled "
        "run."
    )

    csr = schemas["CreateReportScheduleRequest"]
    csr["description"] = (
        "Report Schedule creation requires the following information get encoded in a JSON request "
        "body."
    )
    csp = csr["properties"]
    csp["name"]["description"] = "The schedule name."
    csp["report_id"]["description"] = "The report ID returned by the Create Report API."
    csp["schedule_type"]["description"] = (
        "Schedule type: CRON (meaning scheduled) or ADHOC per API Documentation."
    )
    csp["start"]["description"] = (
        "The time at which the schedule takes effect (maybe be in the future)."
    )
    csp["cron_expression_detail"]["description"] = (
        "Cron expression detail specifying frequency (ONCE, HOURLY, DAILY, WEEKLY, MONTHLY, "
        "YEARLY) per Additional Scheduling Options in the API documentation."
    )

    schemas["ReportScheduleWrapper"]["description"] = (
        "Response includes schedule fields such as id (internal report schedule ID), active, "
        "created_at, cron_expression_detail, report_id, schedule_type, start."
    )

    rdr = schemas["ReportDownloadRecord"]
    rdrp = rdr["properties"]
    rdrp["id"]["description"] = (
        "Report tracking identifier used with GET /v2/reports/tracking/{tracking_id}/download."
    )
    rdrp["report_id"]["description"] = "Associated report id."
    rdrp["status"]["description"] = 'Processing status (for example "COMPLETED").'
    rdrp["location"]["description"] = "Storage location path for the report output."
    rdrp["start_time"]["description"] = "Start time for the report processing run."
    rdrp["processing_time_millis"]["description"] = "Processing duration in milliseconds."

    schemas["ReportDownloadsSearchWrapper"]["description"] = (
        'Lists downloads with paging; JSON body provides "report tracking" identifiers for '
        "completed runs available for download."
    )
    rds = schemas["ReportDownloadsSearchWrapper"]["properties"]["data"]["properties"]
    rds["offset"]["description"] = "Offset reflected from request paging parameters."
    rds["page_size"]["description"] = "Page size reflected from request paging parameters."
    rds["total_count"]["description"] = "Total count of download records."
    rds["results"]["description"] = (
        "Download records whose identifiers can be used to download report contents now or at any "
        "other point in the future."
    )

    schemas["ReportPreviewWrapper"]["description"] = (
        "Paged preview rows for a report (Report preview API)."
    )
    rpw = schemas["ReportPreviewWrapper"]["properties"]["data"]["properties"]
    rpw["page_size"]["description"] = "Page size for preview results."
    rpw["offset"]["description"] = "Offset for preview results."
    rpw["total_count"]["description"] = "Total rows available for preview."
    rpw["results"]["description"] = (
        "Array of row objects with fully qualified column keys."
    )

    schemas["ReportsSearchBody"]["description"] = (
        "Report search API JSON request body with paging and optional sort_ons."
    )
    rsb = schemas["ReportsSearchBody"]["properties"]
    rsb["offset"]["description"] = (
        "Offset across the entire data set at which the current page starts."
    )
    rsb["page_size"]["description"] = "The number of records to return per Paging rules."
    rsb["sort_ons"]["description"] = "Optional sort specifications (field and ASC/DESC order)."

    schemas["ReportsSearchWrapper"]["description"] = (
        "Paged list of reports matching the search request."
    )
    rsw = schemas["ReportsSearchWrapper"]["properties"]["data"]["properties"]
    rsw["page_size"]["description"] = "Page size in the response."
    rsw["offset"]["description"] = "Offset in the response."
    rsw["total_count"]["description"] = "Total reports matching the query."
    rsw["results"]["description"] = "Array of report detail objects."

    schemas["ReportRecipientsBody"]["description"] = (
        "Set Report recipients API — specify recipients for a report."
    )
    schemas["ReportRecipientsBody"]["properties"]["recipients"]["description"] = (
        "Recipients who should receive report output (email objects)."
    )
    rem = schemas["ReportRecipientsBody"]["properties"]["recipients"].setdefault(
        "items",
        {"type": "object", "properties": {}, "additionalProperties": True},
    )
    rem.setdefault("properties", {})
    rem["properties"]["email"] = rem["properties"].get("email", {"type": "string", "format": "email"})
    rem["properties"]["email"]["description"] = "Recipient email address."

    schemas["ReportRecipientsWrapper"]["description"] = (
        "Get Report recipients API response listing recipients for a report."
    )
    rrw = schemas["ReportRecipientsWrapper"]["properties"]["data"]["properties"]
    rrw["report_id"]["description"] = "Report identifier."
    rrw["recipients"]["description"] = "Recipients associated with the report."
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

    spec["components"]["responses"]["NotFound"]["description"] = (
        "The resource you attempted to access does not exist."
    )

    _patch_path_parameters(spec)

    spec["servers"][0]["variables"]["region"]["description"] = (
        "As a customer you will need to substitute the host name specific to the region in which "
        "your data resides."
    )

    p.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {p}")


if __name__ == "__main__":
    main()
