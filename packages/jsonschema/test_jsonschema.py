import pytest
from pytest_pyodide import run_in_pyodide


@run_in_pyodide(packages=["jsonschema"])
def test_jsonschema_import_draft202012(selenium):
    from jsonschema import Draft202012Validator

    assert Draft202012Validator is not None


@run_in_pyodide(packages=["jsonschema"])
def test_jsonschema_validate_ok(selenium):
    import jsonschema

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0},
        },
        "required": ["name"],
    }
    jsonschema.validate({"name": "Alice", "age": 30}, schema)


@run_in_pyodide(packages=["jsonschema"])
def test_jsonschema_validate_raises(selenium):
    import jsonschema
    import pytest

    schema = {"type": "integer", "minimum": 0}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(-1, schema)


@run_in_pyodide(packages=["jsonschema"])
def test_jsonschema_format_checker(selenium):
    import jsonschema
    from jsonschema import FormatChecker

    jsonschema.validate(
        "2026-05-12",
        {"type": "string", "format": "date"},
        format_checker=FormatChecker(),
    )


@run_in_pyodide(packages=["jsonschema"])
def test_jsonschema_draft202012_iter_errors(selenium):
    from jsonschema import Draft202012Validator

    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors({"name": 1}))
    assert len(errors) == 1
    assert errors[0].validator == "type"
