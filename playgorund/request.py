import jsonschema
import json
from common.config import *
from common.config.config import ElevationConfig


def validate_response_body_schema(response_body: str, schema: dict):
    """
    This function will validate the response body schema
    :param response_body: response body string
    :param schema: python schema
    :return:
    dict of is valida flag and reason
    """
    is_response_valid = {"is_valid": True, "reason": ""}
    try:
        response_data = json.loads(response_body)
        jsonschema.validate(response_data, schema)
        return is_response_valid
    except json.JSONDecodeError:
        is_response_valid["is_valid"] = False
        is_response_valid["reason"] = "Error parsing response JSON."
        return is_response_valid
    except jsonschema.exceptions.ValidationError as e:
        is_response_valid["is_valid"] = False
        is_response_valid["reason"] = f"Response validation error: {e.message}"
        return is_response_valid


response_schema = {
    "type": "object",
    "required": ["data", "products"],
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["longitude", "latitude", "height"],
                "properties": {
                    "longitude": {
                        "type": "number",
                        "format": "double"
                    },
                    "latitude": {
                        "type": "number",
                        "format": "double"
                    },
                    "height": {
                        "type": "number",
                        "nullable": True,
                        "format": "double"
                    },
                    "productId": {
                        "type": "string"
                    }
                }
            }
        },
        "products": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "productType": {
                        "oneOf": [
                            {"$ref": "#/definitions/productTypeEnum"}
                        ]
                    },
                    "resolutionMeter": {
                        "type": "number",
                        "format": "double"
                    },
                    "absoluteAccuracyLEP90": {
                        "type": "number",
                        "format": "double"
                    },
                    "updateDate": {
                        "type": "string",
                        "format": "date-time"
                    }
                }
            }
        }
    },
    "definitions": {
        "productTypeEnum": {
            "type": "string",
            "enum": ["DSM", "DTM", "MIXED"]
        }
    }
}



response_content = """ {
    "data": [
        {
            "latitude": 32.77799447531367,
            "longitude": 35.3515237021664,
            "height": 341.1314283899249,
            "productId": "22111111-1111-1111-1111-111111111111"
        },
        {
            "latitude": 32.63471527948201,
            "longitude": 35.43627669431557,
            "height": 194.52289124972788,
            "productId": "22111111-1111-1111-1111-111111111111"
        },
        {
            "latitude": 32.71178885617321,
            "longitude": 35.67004062476305,
            "height": 285.475907245389,
            "productId": "22111111-1111-1111-1111-111111111111"
        },
        {
            "latitude": 32.938864930225805,
            "longitude": 35.2513946971832,
            "height": 479.0000915555284,
            "productId": "22111111-1111-1111-1111-111111111111"
        },
        {
            "latitude": 32.61686551394591,
            "longitude": 35.592909262484916,
            "height": -217.7191314869324,
            "productId": "22111111-1111-1111-1111-111111111111"
        },
        {
            "latitude": 32.6274275271839,
            "longitude": 35.25963413542271,
            "height": 56.74249097000812,
            "productId": "22111111-1111-1111-1111-111111111111"
        },
        {
            "latitude": 32.91873888948771,
            "longitude": 35.377996112852536,
            "height": 248.27864581561394,
            "productId": "22111111-1111-1111-1111-111111111111"
        },
        {
            "latitude": 32.61143389324824,
            "longitude": 35.63459003056397,
            "height": -19.097115486640114,
            "productId": "22111111-1111-1111-1111-111111111111"
        },
        {
            "latitude": 32.84209176987322,
            "longitude": 35.4737307506895,
            "height": 49.81626034447447,
            "productId": "22111111-1111-1111-1111-111111111111"
        },
        {
            "latitude": 32.652417803520216,
            "longitude": 35.71351164961295,
            "height": 0,
            "productId": "11111111-1111-1111-1111-111111111111"
        }
    ]
    }
"""

print(validate_response_body_schema(response_body=response_content, schema=response_schema))
