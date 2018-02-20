from django.test import TestCase

from core.core import calculate
from core.tests.test_prepare import split_single, split_double


class TestClassification(TestCase):
    """Proof of concept tests"""

    def get_job(self):
        json = dict()
        json["clustering"] = "kmeans"
        json["split"] = split_double()
        json["method"] = "randomForest"
        json["encoding"] = "simpleIndex"
        json["rule"] = "remaining_time"
        json["prefix_length"] = 1
        json["threshold"] = "default"
        json["type"] = "classification"
        return json

    """def test_class_randomForest(self):
        job = self.get_job()
        job['clustering'] = 'noCluster'
        result = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.6666666666666666, 'acc': 0.5, 'auc': 0.5})

    # KNN Fails due to small dataset
    # Expected n_neighbors <= n_samples,  but n_samples = 4, n_neighbors = 5
    def class_KNN(self):
        job = self.get_job()
        job['method'] = 'KNN'
        calculate(job)

    def test_class_DecisionTree(self):
        job = self.get_job()
        job['method'] = 'decisionTree'
        result = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.6666666666666666, 'acc': 0.5, 'auc': 0})

    def test_next_activity_randomForest(self):
        job = self.get_job()
        job['type'] = 'nextActivity'
        result = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.6666666666666666, 'acc': 0.5, 'auc': 0})

    # KNN Fails due to small dataset
    # Expected n_neighbors <= n_samples,  but n_samples = 4, n_neighbors = 5
    def next_activity_KNN(self):
        job = self.get_job()
        job['method'] = 'KNN'
        job['type'] = 'nextActivity'
        calculate(job)

    def test_next_activity_DecisionTree(self):
        job = self.get_job()
        job['method'] = 'decisionTree'
        job['type'] = 'nextActivity'
        job['clustering'] = 'None'
        result = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.6666666666666666, 'acc': 0.5, 'auc': 0})"""

    def test_class_complex(self):
        job = self.get_job()
        job['clustering'] = 'noCluster'
        job["encoding"] = "complex"
        result = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.6666666666666666, 'acc': 0.5, 'auc': 0.5})

    def test_class_last_payload(self):
        job = self.get_job()
        job['clustering'] = 'noCluster'
        job["encoding"] = "lastPayload"
        result = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.6666666666666666, 'acc': 0.5, 'auc': 0.5})
