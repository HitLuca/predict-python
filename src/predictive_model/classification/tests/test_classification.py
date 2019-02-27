"""
classification tests
"""

import itertools
import unittest

from django.test import TestCase

from src.core.constants import KNN, NO_CLUSTER, CLASSIFICATION, HOEFFDING_TREE, CLASSIFICATION_METHODS, SGDCLASSIFIER, \
    ADAPTIVE_TREE, PERCEPTRON, NN, RANDOM_FOREST, DECISION_TREE
from src.core.core import calculate
from src.core.tests.common import split_double, add_default_config
from src.encoding.encoding_container import EncodingContainer, ZERO_PADDING, SIMPLE_INDEX, ENCODING_METHODS, PADDINGS, \
    NO_PADDING
from src.labelling.label_container import LabelContainer, NEXT_ACTIVITY, ATTRIBUTE_STRING, THRESHOLD_CUSTOM, DURATION, \
    CLASSIFICATION_LABELS, ATTRIBUTE_NUMBER, THRESHOLD_MEAN


class TestClassification(TestCase):
    @staticmethod
    def get_job(method=KNN, encoding_method=SIMPLE_INDEX, padding=ZERO_PADDING, label=DURATION,
                add_elapsed_time=False):
        json = dict()
        json['clustering'] = NO_CLUSTER
        json['split'] = split_double()
        json['method'] = method
        json['encoding'] = EncodingContainer(encoding_method, padding=padding)
        json['incremental_train'] = {'base_model': None}
        if label == ATTRIBUTE_STRING:
            json['label'] = LabelContainer(label, attribute_name='creator')
        elif label == THRESHOLD_CUSTOM:
            json['label'] = LabelContainer(threshold_type=label, threshold=50)
        elif label == THRESHOLD_MEAN:
            json['label'] = LabelContainer(threshold_type=label, threshold=50)
        else:
            json['label'] = LabelContainer(label)
        json['add_elapsed_time'] = add_elapsed_time
        json['type'] = CLASSIFICATION

        if method != KNN:
            add_default_config(json)
        else:
            json['classification.knn'] = {'n_neighbors': 3}
        return json

    def test_no_exceptions(self):
        filtered_labels = [x for x in CLASSIFICATION_LABELS if
                           x not in [ATTRIBUTE_NUMBER]]  # TODO: check how to add TRACE_NUMBER_ATTRIBUTE

        filtered_classification_methods = [x for x in CLASSIFICATION_METHODS if x not in
                                           [HOEFFDING_TREE, ADAPTIVE_TREE, SGDCLASSIFIER, PERCEPTRON,
                                            NN]]  # TODO: fix new models
        choices = [ENCODING_METHODS, PADDINGS, filtered_classification_methods, filtered_labels]

        job_combinations = list(itertools.product(*choices))

        for (encoding, padding, method, label) in job_combinations:
            print(encoding, padding, method, label)

            if method == 'nn' and (padding == NO_PADDING or label == ATTRIBUTE_STRING):
                pass
            job = self.get_job(method=method, encoding_method=encoding, padding=padding, label=label)
            # with HidePrints():
            calculate(job)

    @staticmethod
    def results():
        return {'f1score': 0.66666666666666663, 'acc': 0.5, 'auc': 0.16666666666666666, 'false_negative': 0,
                'false_positive': 1, 'true_positive': 1, 'true_negative': 0, 'precision': 1.0, 'recall': 0.5}

    @staticmethod
    def results2():
        return {'f1score': 0.3333333333333333, 'acc': 0.5, 'true_positive': 1, 'true_negative': 0, 'false_negative': 0,
                'false_positive': 1, 'precision': 0.25, 'recall': 0.5, 'auc': 0.5}

    @staticmethod
    def results3():
        return {'f1score': 0.3333333333333333, 'acc': 0.5, 'true_positive': 0, 'true_negative': 1, 'false_negative': 1,
                'false_positive': 0, 'precision': 0.25, 'recall': 0.5, 'auc': 0.5}

    @unittest.skip('needs refactoring')
    def test_class_randomForest(self):
        job = self.get_job()
        job['method'] = RANDOM_FOREST
        job['clustering'] = 'noCluster'
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, self.results2())

    @unittest.skip('needs refactoring')
    def test_next_activity_DecisionTree(self):
        job = self.get_job()
        job['method'] = DECISION_TREE
        job['label'] = LabelContainer(NEXT_ACTIVITY)
        job['clustering'] = 'noCluster'
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, self.results3())
