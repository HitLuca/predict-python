from django.test import TestCase

from core.core import calculate
from core.tests.test_prepare import repair_example, add_default_config


class RefactorProof(TestCase):
    def results(self):
        return {'f1score': 0.6757679180887372, 'acc': 0.5701357466063348, 'true_positive': 99, 'true_negative': 27,
                'false_negative': 28, 'false_positive': 67, 'precision': 0.5963855421686747,
                'recall': 0.7795275590551181, 'auc': 0.6113391741461917}

    def results2(self):
        return {'f1score': 0.7200000000000001, 'acc': 0.6515837104072398, 'true_positive': 99, 'true_negative': 45,
                'false_negative': 28, 'false_positive': 49, 'precision': 0.668918918918919,
                'recall': 0.7795275590551181, 'auc': 0.69484000670128987}

    def get_job(self):
        json = dict()
        json["clustering"] = "kmeans"
        json["split"] = repair_example()
        json["method"] = "randomForest"
        json["encoding"] = "simpleIndex"
        json["rule"] = "remaining_time"
        json["prefix_length"] = 5
        json["threshold"] = "default"
        json["type"] = "classification"
        json["padding"] = 'zero_padding'
        return json

    def test_class_kmeans(self):
        self.maxDiff = None
        job = self.get_job()
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.6757679180887372, 'acc': 0.5701357466063348, 'true_positive': 99,
                                      'true_negative': 27,
                                      'false_negative': 28, 'false_positive': 67, 'precision': 0.5963855421686747,
                                      'recall': 0.7795275590551181, 'auc': 0.6113391741461917})

    def test_class_no_cluster(self):
        self.maxDiff = None
        job = self.get_job()
        job['clustering'] = 'noCluster'
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.7200000000000001, 'acc': 0.6515837104072398, 'true_positive': 99,
                                      'true_negative': 45,
                                      'false_negative': 28, 'false_positive': 49, 'precision': 0.668918918918919,
                                      'recall': 0.7795275590551181, 'auc': 0.69484000670128987})

    def test_next_activity_kmeans(self):
        self.maxDiff = None
        job = self.get_job()
        job["type"] = "nextActivity"
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.4914675767918089, 'acc': 0.3257918552036199, 'true_positive': 72,
                                      'true_negative': 0, 'false_negative': 0, 'false_positive': 149,
                                      'precision': 0.3257918552036199, 'recall': 1.0, 'auc': 0})

    def test_next_activity_no_cluster(self):
        self.maxDiff = None
        job = self.get_job()
        job["type"] = "nextActivity"
        job['clustering'] = 'noCluster'
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result,
                             {'f1score': 1.0, 'acc': 1.0, 'true_positive': 221, 'true_negative': 0, 'false_negative': 0,
                              'false_positive': 0, 'precision': 1.0, 'recall': 1.0, 'auc': 0})

    def test_regression_kmeans(self):
        self.maxDiff = None
        job = self.get_job()
        job["type"] = "regression"
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result,{'rmse': 0.3443653235293935, 'mae': 0.30008995917834302, 'rscore': -0.28701218314969568})

    def test_regression_no_cluster(self):
        self.maxDiff = None
        job = self.get_job()
        job["type"] = "regression"
        job['clustering'] = 'noCluster'
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, {'rmse': 0.29123518093268796, 'mae': 0.22594042332624051, 'rscore': 0.079483654726128616})
