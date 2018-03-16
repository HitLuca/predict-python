import pandas as pd
from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier

from encoders.log_util import HEADER_COLUMNS, HEADER_COLUMNS_RUN
from .log_util import remaining_time_id, elapsed_time_id

CLASSIFIER = XEventAttributeClassifier("Trace name", ["concept:name"])


def simple_index(log: list, event_names: list, prefix_length=1, next_activity=False, run=False):
    if prefix_length < 1:
        raise ValueError("Prefix length must be greater than 1")
    if next_activity:
        return encode_next_activity(log, event_names, prefix_length, run)
    return encode_simple_index(log, event_names, prefix_length, run)


def encode_simple_index(log: list, event_names: list, prefix_length: int, run):
    columns = __create_columns(prefix_length, run)
    encoded_data = []

    for trace in log:
        if len(trace) <= prefix_length - 1:
            continue
        trace_row = []
        trace_name = CLASSIFIER.get_class_identity(trace)
        trace_row.append(trace_name)
        if run == False:
            trace_row.append(remaining_time_id(trace, prefix_length - 1))
        trace_row.append(elapsed_time_id(trace, prefix_length - 1))
        trace_row += trace_prefixes(trace, event_names, prefix_length)
        #print(trace_row)
        encoded_data.append(trace_row)

    return pd.DataFrame(columns=columns, data=encoded_data)


def encode_next_activity(log: list, event_names: list, prefix_length: int, run):
    columns = __columns_next_activity(prefix_length, run)
    encoded_data = []

    for trace in log:
        trace_row = []
        trace_name = CLASSIFIER.get_class_identity(trace)
        trace_row.append(trace_name)

        trace_row += trace_prefixes(trace, event_names, prefix_length)

        for _ in range(len(trace), prefix_length):
            trace_row.append(0)
        if not run:
            trace_row.append(next_event_index(trace, event_names, prefix_length))
        encoded_data.append(trace_row)
    return pd.DataFrame(columns=columns, data=encoded_data)


def __create_columns(prefix_length: int, run):
    if run:
        columns = list(HEADER_COLUMNS_RUN)
    else:
        columns = list(HEADER_COLUMNS)
    for i in range(1, prefix_length + 1):
        columns.append("prefix_" + str(i))
    return columns


def __columns_next_activity(prefix_length, run):
    """Creates columns for next activity"""
    columns = ["trace_id"]
    for i in range(0, prefix_length):
        columns.append("prefix_" + str(i + 1))
    if not run:
        columns.append("label")
    return columns


def trace_prefixes(trace: list, event_names: list, prefix_length: int):
    """List of indexes of the position they are in event_names"""
    prefixes = list()
    for idx, event in enumerate(trace):
        if idx == prefix_length:
            break
        event_name = CLASSIFIER.get_class_identity(event)
        event_id = event_names.index(event_name)
        prefixes.append(event_id + 1)
    return prefixes


def next_event_index(trace: list, event_names: list, prefix_length: int):
    """Return the event_name index of the one after at prefix_length.
    Offset by +1.
    Or 0 if out of range.
    """
    if prefix_length < len(trace):
        next_event = trace[prefix_length]
        next_event_name = CLASSIFIER.get_class_identity(next_event)
        return event_names.index(next_event_name) + 1
    else:
        return 0
