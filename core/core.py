from core.classification import classifier
from core.constants import \
    CLASSIFICATION, REGRESSION, ZERO_PADDING
from core.next_activity import next_activity
from core.regression import regression
from encoders.common import encode_label_logs, REMAINING_TIME, ATTRIBUTE_NUMBER, ATTRIBUTE_STRING, NEXT_ACTIVITY
from logs.splitting import prepare_logs


def calculate(job):
    """ Main entry method for calculations"""
    print("Start job {} with {}".format(job['type'], get_run(job)))

    training_df, test_df = get_encoded_logs(job)
    results, model_split = run_by_type(training_df, test_df, job)
    return results, model_split


def get_encoded_logs(job: dict):
    training_log, test_log = prepare_logs(job['split'])

    # Python dicts are bad
    if 'prefix_length' in job:
        prefix_length = job['prefix_length']
    else:
        prefix_length = 1
    zero_padding = True if job['padding'] is ZERO_PADDING else False

    training_df, test_df = encode_label_logs(training_log, test_log, job['encoding'], job['type'], job['label'],
                                             prefix_length=prefix_length, zero_padding=zero_padding)
    return training_df, test_df


def run_by_type(training_df, test_df, job):
    if job['type'] == CLASSIFICATION:
        label_type = job['label'].type
        # Binary classification
        if label_type == REMAINING_TIME or label_type == ATTRIBUTE_NUMBER:
            results, model_split = classifier(training_df, test_df, job)
        elif label_type == NEXT_ACTIVITY or label_type == ATTRIBUTE_STRING:
            results, model_split = next_activity(training_df, test_df, job)
        else:
            raise ValueError("Label type not supported", label_type)
    elif job['type'] == REGRESSION:
        results, model_split = regression(training_df, test_df, job)
    else:
        raise ValueError("Type not supported", job['type'])
    print("End job {}, {} . Results {}".format(job['type'], get_run(job), results))
    return results, model_split


def get_run(job):
    """Defines job identity"""
    return job['method'] + '_' + job['encoding'] + '_' + job['clustering'] + '_' + job['label'].type
