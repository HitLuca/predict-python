from django.test import TestCase

from core.core import calculate
from core.job import Job


class TestClassification(TestCase):
    """Proof of concept tests"""

    def get_job(self):
        json = dict()
        json['uuid'] = "ads69"
        json["clustering"] = "kmeans"
        json["status"] = "completed"
        json["log"] = "log_cache/general_example.xes"
        json["classification"] = "randomForest"
        json["encoding"] = "simpleIndex"
        json["timestamp"] = "Oct 03 2017 13:26:53"
        json["rule"] = "remaining_time"
        json["prefix"] = 0
        json["threshold"] = "default"
        json["type"] = "classification"
        return Job(json)

    def test_class_randomForest(self):
        job = self.get_job()
        job.clustering = 'None'
        result = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.6666666666666666, 'acc': 0.5, 'auc': 0.5})

    # KNN Fails due to small dataset
    # Expected n_neighbors <= n_samples,  but n_samples = 4, n_neighbors = 5
    def class_KNN(self):
        job = self.get_job()
        job.classification = 'KNN'
        calculate(job)

    def test_class_DecisionTree(self):
        job = self.get_job()
        job.classification = 'decisionTree'
        result = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.6666666666666666, 'acc': 0.5, 'auc': 0})

    def test_next_activity_randomForest(self):
        job = self.get_job()
        job.type = 'nextActivity'
        calculate(job)

    # KNN Fails due to small dataset
    # Expected n_neighbors <= n_samples,  but n_samples = 4, n_neighbors = 5
    def next_activity_KNN(self):
        job = self.get_job()
        job.classification = 'KNN'
        job.type = 'nextActivity'
        calculate(job)

    def test_next_activity_DecisionTree(self):
        job = self.get_job()
        job.classification = 'decisionTree'
        job.type = 'nextActivity'
        job.clustering = 'None'
        calculate(job)
