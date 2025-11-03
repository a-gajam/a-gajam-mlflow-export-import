"""
Trace utilities.
"""

import json

from mlflow_export_import.common import utils

def trace_to_json(trace):
    """
    Converts a trace info and data to Json
    """

    result =  {
        "info": _trace_to_json(trace.info),
        "data": _trace_to_json(trace.data),
    }
    return result


def _trace_to_json(trace_object):
    result = {}
    for k, v in trace_object.__dict__.items():
        if k == 'spans':
            result[k] = _extract_span(v)
        elif hasattr(v, 'value'):
            # Handles enums like Status
            result[k] = v.value
        elif isinstance(v, dict):
            result[k] = v
        elif isinstance(v, str):
            try:
                result[k] = json.loads(v)
            except (json.JSONDecodeError, ValueError):
                result[k] = v
        elif isinstance(v, list):
            result[k] = [key for key in v]
        else:
            result[k] = v

    return result

def _extract_span(spans):
    """
    Converts a Spans object to a dictionary with only essential fields.
    """
    result = []
    for span in spans:
        result.append({
            'name': getattr(span, 'name', None),
            'trace_id': getattr(span, 'trace_id', None),
            'span_id': getattr(span, 'span_id', None),
            'parent_id': getattr(span, 'parent_id', None),
        })
    return result