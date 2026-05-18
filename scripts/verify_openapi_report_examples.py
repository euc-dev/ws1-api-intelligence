#!/usr/bin/env python3
"""
Regression check: POST /v2/reports example bodies match the DHUB PDF
(API Documentation for Omnissa Intelligence V2) §9.2.1 and §9.2.3 sample requests.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs" / "intelligence-rest-api-swagger.json"


def main() -> None:
    spec = json.loads(SPEC.read_text())
    examples = spec["paths"]["/v2/reports"]["post"]["requestBody"]["content"]["application/json"][
        "examples"
    ]

    historical = examples["historical"]["value"]
    assert historical["name"] == "API Test Report - 5f5abb88-ea63-43bf-8738-ed0c6a7b345a"
    assert historical["description"] == "Sample report description"
    assert historical["integration"] == "airwatch"
    assert historical["entity"] == "application"
    assert historical["column_names"] == ["airwatch.application.app_name"]
    assert (
        historical["filter"] == "airwatch.application.app_dynamic_size_bytes > 5000000"
    )
    assert historical["report_type"] == "HISTORICAL"
    assert historical["report_format"] == "CSV"
    assert historical["date_range"] == {
        "start_date_millis": 1627756241000,
        "end_date_millis": 1628274581000,
    }
    assert historical["join_entities_by_integration"] == {"airwatch": ["application"]}

    snapshot = examples["snapshot"]["value"]
    assert snapshot["name"] == "Test Report - V2 Joins"
    assert (
        snapshot["description"]
        == "All managed and un-managed apps on devices with good antivirus status and half battery level"
    )
    assert (
        snapshot["filter"]
        == " airwatch.device.device_enrollment_status = 'Enrolled' AND airwatch.device._device_antivirus_status IN ( 'Pass' ) AND airwatch.device.device_battery_percent = 50 "
    )
    assert snapshot["report_type"] == "SNAPSHOT"
    assert snapshot["report_format"] == "CSV"
    assert snapshot["integration"] == "airwatch"
    assert snapshot["entity"] == "application"
    assert snapshot["join_entities_by_integration"] == {
        "airwatch": ["application", "device"]
    }
    assert snapshot["column_names"] == [
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
        "airwatch.application.app_is_installed",
    ]

    print("verify_openapi_report_examples: OK")


if __name__ == "__main__":
    main()
