from collections import namedtuple

NEXT_ACTIVITY = 'next_activity'
REMAINING_TIME = 'remaining_time'
ATTRIBUTE_NUMBER = 'attribute_number'
ATTRIBUTE_STRING = 'attribute_string'
NO_LABEL = 'no_label'
DURATION = 'duration'

THRESHOLD_MEAN = 'threshold_mean'
THRESHOLD_CUSTOM = 'threshold_custom'


class LabelContainer(namedtuple('LabelContainer', ["type", "attribute_name", "threshold_type", "threshold",
                                                   "add_remaining_time", "add_elapsed_time", "add_events_executed",
                                                   "add_resources_used", "add_new_traces"])):
    """Inner object describing labelling state.
    For no labelling use NO_LABEL

    This is a horrible hack and should be split into a label container and a container for encoding options, like
    what to add to the encoded log.
    """

    def __new__(cls, type=REMAINING_TIME, attribute_name=None, threshold_type=THRESHOLD_MEAN, threshold=0,
                add_remaining_time=False, add_elapsed_time=False, add_events_executed=False, add_resources_used=False,
                add_new_traces=False):
        return super(LabelContainer, cls).__new__(cls, type, attribute_name, threshold_type, threshold,
                                                  add_remaining_time, add_elapsed_time, add_events_executed,
                                                  add_resources_used, add_new_traces)
