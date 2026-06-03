"""Site hooks for toggling Swagger/OpenAPI documentation."""

SWAGGER_OPENAPI_PAGES = (
    "Authentication.md",
    "REST-APIs.md",
    "API-sample-responses.md",
)

SWAGGER_OPENAPI_NAV = (
    {"Overview": "index.md"},
    {"Authentication": "Authentication.md"},
    {"REST APIs": "REST-APIs.md"},
    {"Sample responses": "API-sample-responses.md"},
)


def _is_swagger_openapi_enabled(config):
    return bool(config.get("extra", {}).get("enable_swagger_openapi", False))


def on_config(config):
    if _is_swagger_openapi_enabled(config):
        config["nav"] = list(SWAGGER_OPENAPI_NAV)
        return config

    config["nav"] = ["index.md"]
    config["extra_javascript"] = [
        script
        for script in config.get("extra_javascript", [])
        if "swagger-token-bridge" not in script
    ]
    return config


def on_files(files, config):
    if _is_swagger_openapi_enabled(config):
        return files

    for page in SWAGGER_OPENAPI_PAGES:
        file = files.get_file_from_path(page)
        if file is not None:
            files.remove(file)

    return files
