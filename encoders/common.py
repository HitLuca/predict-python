import hashlib

from pandas import DataFrame

from core.constants import LABELLING, REGRESSION
from encoders.boolean_frequency import frequency, boolean
from encoders.complex_last_payload import complex, last_payload
from encoders.encoding_container import EncodingContainer, SIMPLE_INDEX, BOOLEAN, FREQUENCY, COMPLEX, LAST_PAYLOAD
from encoders.label_container import *
from utils.event_attributes import unique_events
from .simple_index import simple_index


def encode_label_logs(training_log: list, test_log: list, encoding: EncodingContainer, job_type: str,
                      label: LabelContainer, additional_columns=None):
    """Encodes and labels test set and training set as data frames

    :param additional_columns: Global trace attributes for complex and last payload encoding
    :returns training_df, test_df
    """  # TODO: complete documentation
    training_log, cols = _encode_log(training_log, encoding, label, additional_columns=additional_columns,
                                     cols=None)
    # TODO pass the columns of the training log
    test_log, _ = _encode_log(test_log, encoding, label, additional_columns=additional_columns, cols=cols)

    if (label.threshold_type in [THRESHOLD_MEAN, THRESHOLD_CUSTOM]) and (
        label.type in [REMAINING_TIME, ATTRIBUTE_NUMBER, DURATION]):
        if label.threshold_type == THRESHOLD_MEAN:
            threshold = training_log['label'].mean()
        elif label.threshold_type == THRESHOLD_CUSTOM:
            threshold = label.threshold
        training_log['label'] = training_log['label'] < threshold
        test_log['label'] = test_log['label'] < threshold

    if job_type != LABELLING and encoding.method != BOOLEAN:
        # init nominal encode
        encoding.init_label_encoder(training_log)
        # encode data
        encoding.encode(training_log)
        encoding.encode(test_log)

    return training_log, test_log


def encode_label_log(run_log: list, encoding: EncodingContainer, job_type: str, label: LabelContainer, event_names=None,
                     additional_columns=None, fit_encoder=False):
    encoded_log, _ = _encode_log(run_log, encoding, label, additional_columns)

    # Convert strings to number
    if label.type == ATTRIBUTE_NUMBER:
        try:
            encoded_log['label'] = encoded_log['label'].apply(lambda x: float(x))
        except:
            encoded_log['label'] = encoded_log['label'].apply(lambda x: x == 'true')

    # converts string values to in
    if job_type != LABELLING:
        # Labelling has no need for this encoding
        _categorical_encode(encoded_log)
    # Regression only has remaining_time or number atr as label
    if job_type == REGRESSION:
        # Remove last events as worse for prediction
        # TODO filter out 0 labels. Doing it here means runtime errors for regression
        # if label.type == REMAINING_TIME:
        #     encoded_log = encoded_log.loc[encoded_log['label'] != 0.0]
        return encoded_log
    # Post processing
    if label.type == REMAINING_TIME or label.type == ATTRIBUTE_NUMBER or label.type == DURATION:
        return _label_boolean(encoded_log, label)
    return encoded_log


def _encode_log(log: list, encoding: EncodingContainer, label: LabelContainer, additional_columns=None, cols=None):
    if encoding.prefix_length < 1:
        raise ValueError("Prefix length must be greater than 1")
    if encoding.method == SIMPLE_INDEX:
        run_df = simple_index(log, label, encoding)
    elif encoding.method == BOOLEAN:
        if cols is None:
            cols = unique_events(log)
        run_df = boolean(log, cols, label, encoding)
    elif encoding.method == FREQUENCY:
        if cols is None:
            cols = unique_events(log)
        run_df = frequency(log, cols, label, encoding)
    elif encoding.method == COMPLEX:
        run_df = complex(log, label, encoding, additional_columns)
    elif encoding.method == LAST_PAYLOAD:
        run_df = last_payload(log, label, encoding, additional_columns)
    else:
        raise ValueError("Unknown encoding method {}".format(encoding.method))
    return run_df, cols


def _label_boolean(df: DataFrame, label: LabelContainer):
    """Label a numeric attribute as True or False based on threshold
    This is essentially a Fast/Slow classification without string labels
    By default use mean of label value
    True if under threshold value
    """
    if df['label'].dtype == bool:
        return df
    if label.threshold_type == THRESHOLD_MEAN:
        threshold = df['label'].mean()
    else:
        threshold = float(label.threshold)
    df['label'] = df['label'] < threshold
    return df


def _categorical_encode(df):
    """Encodes every column except trace_id and label as int

    Encoders module puts event name in cell, which can't be used by machine learning methods directly.
    """
    for column in df.columns:
        if column == 'trace_id':
            continue
        elif df[column].dtype == type(str):
            df[column] = df[column].map(lambda s: _convert(s))
    return df


def _convert(s):
    if isinstance(s, float) or isinstance(s, int):
        return s
    if s is None:
        # Next activity resources
        s = '0'
    # TODO this potentially generates collisions and in general is a clever solution for another problem
    # see https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
    return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10 ** 8
