from scripts.mock_api import transform_spec


def test_transform_spec_prefixes_paths_and_applies_examples():
    raw_spec = {
        "openapi": "3.0.1",
        "info": {"title": "BMC Discovery API", "version": "1.14"},
        "servers": [{"url": "/api/v1.14"}],
        "paths": {
            "/admin/about": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "OK",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            },
                        }
                    }
                }
            }
        },
        "components": {},
    }
    about = {
        "product": "BMC Discovery",
        "component": "REST API",
        "version": "15.0",
        "api_versions": ["1.14"],
        "product_version": "25.2.00",
    }
    overlay = {
        "examples": [
            {
                "path": "/admin/about",
                "method": "get",
                "status": 200,
                "example": {"versions": {"product": "15.0"}},
            }
        ]
    }

    spec = transform_spec(raw_spec, about, overlay, "1.14")

    assert spec["servers"] == [{"url": "/"}]
    assert "/admin/about" not in spec["paths"]
    assert "/api/v1.14/admin/about" in spec["paths"]
    assert "/api/about" in spec["paths"]
    example = spec["paths"]["/api/v1.14/admin/about"]["get"]["responses"]["200"]["content"]["application/json"]["example"]
    assert example == {"versions": {"product": "15.0"}}
    about_example = spec["paths"]["/api/about"]["get"]["responses"]["200"]["content"]["application/json"]["example"]
    assert about_example["product_version"] == "25.2.00"
