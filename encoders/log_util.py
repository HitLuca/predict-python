from datetime import datetime as dt
import math
from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier
from opyenxes.model.XLog import XLog

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DEFAULT_COLUMNS = ["trace_id", "event_nr", "remaining_time", "elapsed_time"]
TIMESTAMP_CLASSIFIER = XEventAttributeClassifier("Timestamp", ["time:timestamp"])
HEADER_COLUMNS = ['trace_id', 'remaining_time', 'elapsed_time']
HEADER_COLUMNS_RUN = ['trace_id',  'elapsed_time']


def unique_events(log: list):
    """List of unique events using event concept:name

    Adds all events into a list and removes duplicates while keeping order.
    """
    
    classifier = XEventAttributeClassifier("Resource", ["concept:name"])
    event_list = []
    length=[]
    for trace in log:
        count=0
        for event in trace:
            count += 1
            event_name = classifier.get_class_identity(event)
            event_list.append(event_name)
        length.append(count)
    p_length=0
    for i in range(len(length)):
        p_length+=length[i]
    divisor=math.ceil(len(length)*3/4)
    p_length=math.ceil(p_length/divisor)
    return sorted(set(event_list), key=lambda x: event_list.index(x)),p_length


def unique_events2(training_log: list, test_log: list):
    """ Combines unique events from two logs into one list.

    Renamed to 2 because Python doesn't allow functions with same names.
    Python is objectively the worst language.
    """
    tr_event_list, _ = unique_events(training_log) 
    ts_event_list, _ = unique_events(test_log)
    event_list=tr_event_list + ts_event_list
    return sorted(set(event_list), key=lambda x: event_list.index(x))


def elapsed_time_id(trace, event_index: int):
    """Calculate elapsed time by event index in trace"""
    return elapsed_time(trace, trace[event_index])


def elapsed_time(trace, event):
    """Calculate elapsed time by event in trace"""
    # FIXME using no timezone info for calculation
    event_time = TIMESTAMP_CLASSIFIER.get_class_identity(event)[:19]
    first_time = TIMESTAMP_CLASSIFIER.get_class_identity(trace[0])[:19]
    try:
        delta = dt.strptime(event_time, TIME_FORMAT) - dt.strptime(first_time, TIME_FORMAT)
    except ValueError:
        # Log has no timestamps
        return 0
    return delta.total_seconds()


def remaining_time_id(trace, event_index: int):
    """Calculate remaining time by event index in trace"""
    return remaining_time(trace, trace[event_index])


def remaining_time(trace, event):
    """Calculate remaining time by event in trace"""
    # FIXME using no timezone info for calculation
    event_time = TIMESTAMP_CLASSIFIER.get_class_identity(event)[:19]
    last_time = TIMESTAMP_CLASSIFIER.get_class_identity(trace[-1])[:19]
    try:
        delta = dt.strptime(last_time, TIME_FORMAT) - dt.strptime(event_time, TIME_FORMAT)
    except ValueError:
        # Log has no timestamps
        return 0
    return delta.total_seconds()


def get_event_attributes(log):
    """Get log event attributes that are not name or time

    Log can be XLog or list of events (meaning it was split). Cast to XLog.
    """
    if type(log) is list:
        log = XLog(log)
    event_attributes = []
    for attribute in log.get_global_event_attributes():
        if attribute.get_key() not in ["concept:name", "time:timestamp"]:
            event_attributes.append(attribute.get_key())
    return sorted(event_attributes)
