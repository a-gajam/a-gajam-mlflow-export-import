"""
Export a trace to a directory
"""

import click
import traceback
from mlflow.exceptions import RestException

from mlflow_export_import.client.client_utils import create_mlflow_client
from mlflow_export_import.common import utils, io_utils
from mlflow_export_import.common.click_options import (
    opt_trace_request_id,
    opt_output_dir
)
from mlflow_export_import.trace.trace_utils import trace_to_json

_logger = utils.getLogger(__name__)

def export_trace(
        trace_request_id,
        output_dir,
        mlflow_client = None,
    ):
    """
    :param trace_request_id: The trace request id
    :param output_dir: Output directory
    :param mlflow_client: Mlflow client
    """
    mlflow_client = mlflow_client or create_mlflow_client()

    try:
        trace = mlflow_client.get_trace(trace_request_id)
        mlflow_attr = trace_to_json(trace)
        io_utils.write_export_file(output_dir, "trace.json", __file__, mlflow_attr)
        return trace
    except RestException as e:
        err_msg = {"trace_request_id": trace_request_id, "experiment_id": trace.info.experiment_id, "RestException": e.json}
        _logger.error(f"Trace export failed (1): {err_msg}")
        return None
    except Exception as e:
        err_msg = {"trace_request_id": trace_request_id, "experiment_id": trace.info.experiment_id, "Exception": e}
        _logger.error(f"Trace export failed (2): {err_msg}")
        traceback.print_exc()
        return None


@click.command()
@opt_trace_request_id
@opt_output_dir
def main(trace_request_id, output_dir):
    _logger.info("Options:")
    export_trace(
        trace_request_id=trace_request_id,
        output_dir=output_dir,
    )


if __name__ == "__main__":
    main()