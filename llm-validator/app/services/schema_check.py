from typing import Any
import json
from jsonschema import validate, ValidationError

def check_schema(response: Any, expected_schema: dict) -> float:
    try:
        # If already a dict, no need to parse JSON
        if isinstance(response, str):
            response_data = json.loads(response)
        else:
            response_data = response

        # Validate against the schema
        validate(instance=response_data, schema=expected_schema)
        return 1.0  # Perfect match
    except json.JSONDecodeError:
        return 0.0  # Not valid JSON
    except ValidationError:
        return 0.0  # Schema validation failed
    except Exception:
        return 0.0  # Any other error

def validate_json_schema(schema: dict) -> bool:
    try:
        # Basic schema validation
        validate(instance={}, schema=schema)
        return True
    except ValidationError:
        return False
    except Exception:
        return False

def validate_json_data(json_data: dict, schema: dict) -> bool:
    try:
        validate(instance=json_data, schema=schema)
        return True
    except ValidationError:
        return False
    except Exception:
        return False