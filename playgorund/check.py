import json
import jsonschema


def validate_response(response_body: str, schema: dict):
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


# Example usage
response_body = """{
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
            "productId": "22111111-874611-1111-1111-111111111111"
        },
        {
            "latitude": 32.652417803520216,
            "longitude": 35.71351164961295,
            "height": 0,
            "productId": "11111111-1111-1111-1111-111111111111"
        }
    ],
    "products": {
        "22111111-1111-1111-1111-111111111111": {
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-05-08T17:44:01.000Z",
            "resolutionMeter": 30,
            "absoluteAccuracyLEP90": 9e-7
        },
        "11111111-1111-1111-1111-111111111111": {
            "productType": "QUANTIZED_MESH_DTM_BEST",
            "updateDate": "2023-04-21T23:44:41.000Z",
            "resolutionMeter": 100,
            "absoluteAccuracyLEP90": 9e-7
        }
    }
}"""
schema = {
    "type": "object",
    "required": ["data"],
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["longitude", "latitude", "height", "productId"],
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
        },
    },
    "dependencies": {
        "data": {
            "properties": {
                "products": {
                    "properties": {
                        "additionalProp1": {
                            "properties": {
                                "productId": { "type": "string" }
                            }
                        },
                        "additionalProp2": {
                            "properties": {
                                "productId": { "type": "string" }
                            }
                        },
                        "additionalProp3": {
                            "properties": {
                                "productId": { "type": "string" }
                            }
                        }
                    }
                }
            }
        }
    }
}


if validate_response(response_body, schema):
    print("Response is valid according to the schema.")
else:
    print("Response is not valid according to the schema.")

import json


def find_unfounded_product_ids(response_data):
    """
    this function will find the product ids that wasn't found at the response products property
    :param response_data: requests response data (str)
    :return:
    list of unfounded product ids if exist
    """
    try:
        # Parse the JSON response
        response_data = json.loads(response_data)

        # Extract data and products
        data = response_data.get("data", [])
        products = response_data.get("products", {})

        # Get a list of all product IDs from the data property
        data_product_ids = [item.get("productId") for item in data]

        # Get the set of keys from the products property
        products_keys = set(products.keys())

        # Find unfound product IDs
        unfound_product_ids = [product_id for product_id in data_product_ids if product_id not in products_keys]

        return unfound_product_ids

    except json.JSONDecodeError:
        print("Error parsing JSON response.")
    except Exception as e:
        print(f"Validation error: {str(e)}")

    return []


# Example usage
response_data = '''
{
    "data": [
        {
            "longitude": 0,
            "latitude": 0,
            "height": 0,
            "productId": "product1"
        },
        {
            "longitude": 0,
            "latitude": 0,
            "height": 0,
            "productId": "product2"
        },
               {
            "longitude": 1,
            "latitude": 2,
            "height": 3,
            "productId": "product3"
        }
    ],
    "products": {
        "product1": {
            "productType": "DSM",
            "resolutionMeter": 0,
            "absoluteAccuracyLEP90": 0,
            "updateDate": "2023-10-29T15:09:06.674Z"
        },
        "product2": {
            "productType": "DSM",
            "resolutionMeter": 0,
            "absoluteAccuracyLEP90": 0,
            "updateDate": "2023-10-29T15:09:06.674Z"
        }
    }
}
'''

unfound_ids = find_unfounded_product_ids(response_data)

if unfound_ids:
    print("Unfound product IDs:", unfound_ids)
else:
    print("All product IDs were found in the products.")
