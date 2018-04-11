"""This module contains set of json schemas for json response validation."""


verify_search_requestid_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "request_id": {
            "type": "string",
            "maxLength": 32
        },
        "account_id": {
            "type": "string"
        },
        "number": {
            "type": "string"
        },
        "sender_id": {
            "type": "string"
        },
        "date_submitted": {
            "format": "date-time",
            "type": "string"
        },
        "date_finalized": {
            "format": "date-time",
            "type": "string"
        },
        "checks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date_received": {
                        "format": "date-time",
                        "type": "string"
                    },
                    "code": {
                        "format": "date-time",
                        "type": "string"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["VALID", "INVALID"]
                    },
                    "ip_address": {
                        "format": "date-time",
                        "type": "string"
                    }
                },
                'additionalProperties': False,
            }
        },
        "first_event_date": {
            "type": "string"
        },
        "last_event_date": {
            "type": "string"
        },
        "price": {
            "type": "string"
        },
        "currency": {
            "type": "string"
        },
        "status": {
            "type": "string",
            "enum": ["IN PROGRESS", "SUCCESS", "FAILED", "EXPIRED", "CANCELLED"]
        }
    },
    "required": [
        "request_id",
        "account_id",
        "number",
        "sender_id",
        "date_submitted",
        "date_finalized",
        "checks",
        "first_event_date",
        "last_event_date",
        "price",
        "currency",
        "status"
    ],
    "additionalProperties": False,
}
verify_search_requestids_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "verification_requests": {
            "type": "array",
            "items": verify_search_requestid_schema
        }
    },
    "required": ["verification_requests"],
    "additionalProperties": False,
}
