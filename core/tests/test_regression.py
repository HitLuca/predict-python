from django.test import TestCase

from core.core import calculate


class TestRegression(TestCase):
    """Proof of concept tests"""

    def get_job(self):
        json = dict()
        json["clustering"] = "kmeans"
        json["log"] = "log_cache/general_example.xes"
        json["regression"] = "linear"
        json["encoding"] = "simpleIndex"
        json["rule"] = "remaining_time"
        json["type"] = "regression"
        return json

    def test_reg_linear(self):
        job = self.get_job()
        job['clustering'] = 'None'
        calculate(job)

    def test_reg_linear_boolean(self):
        job = self.get_job()
        job['clustering'] = 'None'
        job['encoding'] = 'boolean'
        calculate(job)

    def test_reg_randomforest(self):
        job = self.get_job()
        job['regression'] = 'randomForest'
        calculate(job)

    def test_reg_lasso(self):
        job = self.get_job()
        job['regression'] = 'lasso'
        calculate(job)

    def test_reg_lasso_complex(self):
        job = self.get_job()
        job['regression'] = 'lasso'
        job['encoding'] = 'complex'
        calculate(job)

    def test_reg_lasso_last_payload(self):
        job = self.get_job()
        job['regression'] = 'lasso'
        job['encoding'] = 'lastPayload'
        calculate(job)
