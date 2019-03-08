"""
refactoring tests
"""

from django.test import TestCase

from src.clustering.models import ClusteringMethods
from src.core.core import calculate
from src.core.tests.common import repair_example
from src.labelling.models import LabelTypes
from src.predictive_model.classification.models import ClassificationMethods
from src.predictive_model.models import PredictiveModels
from src.predictive_model.regression.models import RegressionMethods
from src.utils.tests_utils import create_test_clustering, create_test_job, create_test_encoding, \
    create_test_predictive_model, create_test_labelling


class RefactorProof(TestCase):

    def test_class_kmeans(self):
        self.max_diff = None
        job = create_test_job(
            clustering=create_test_clustering(clustering_type=ClusteringMethods.KMEANS.value),
            split=repair_example(),
            encoding=create_test_encoding(prefix_length=5, padding=True, add_elapsed_time=True),
            predictive_model=create_test_predictive_model(predictive_model=PredictiveModels.CLASSIFICATION.value,
                                                          prediction_method=ClassificationMethods.RANDOM_FOREST.value)
        )
        result, _ = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.67690058479532156, 'acc': 0.68325791855203621, 'true_positive': 91,
                                      'true_negative': 60, 'false_negative': 36, 'false_positive': 34,
                                      'precision': 0.67649999999999999, 'recall': 0.67741665270564577,
                                      'auc': 0.5913497814050234})

    def test_class_no_cluster(self):
        self.max_diff = None
        job = create_test_job(
            clustering=create_test_clustering(clustering_type=ClusteringMethods.NO_CLUSTER.value),
            split=repair_example(),
            encoding=create_test_encoding(prefix_length=5, padding=True, add_elapsed_time=True),
            predictive_model=create_test_predictive_model(predictive_model=PredictiveModels.CLASSIFICATION.value,
                                                          prediction_method=ClassificationMethods.RANDOM_FOREST.value)
        )
        result, _ = calculate(job)
        self.assertDictEqual(result, {'f1score': 0.67690058479532156, 'acc': 0.6832579185520362, 'true_positive': 91,
                                      'true_negative': 60, 'false_negative': 36, 'false_positive': 34,
                                      'precision': 0.67649999999999999, 'recall': 0.67741665270564577,
                                      'auc': 0.71720556207069863})

    def test_next_activity_kmeans(self):
        self.max_diff = None
        job = create_test_job(
            clustering=create_test_clustering(clustering_type=ClusteringMethods.KMEANS.value),
            split=repair_example(),
            encoding=create_test_encoding(prefix_length=8, padding=True),
            labelling=create_test_labelling(label_type=LabelTypes.NEXT_ACTIVITY.value),
            predictive_model=create_test_predictive_model(predictive_model=PredictiveModels.CLASSIFICATION.value,
                                                          prediction_method=ClassificationMethods.RANDOM_FOREST.value)
        )
        result, _ = calculate(job)

        self.assertDictEqual(result, {'f1score': 0.54239884582595577, 'acc': 0.80995475113122173, 'true_positive': '--',
                                      'true_negative': '--', 'false_negative': '--', 'false_positive': '--',
                                      'precision': 0.62344720496894401, 'recall': 0.5224945442336747,
                                      'auc': 0.19638554216867468})

    def test_next_activity_no_cluster(self):
        self.max_diff = None
        job = create_test_job(
            clustering=create_test_clustering(clustering_type=ClusteringMethods.NO_CLUSTER.value),
            split=repair_example(),
            encoding=create_test_encoding(prefix_length=8, padding=True),
            labelling=create_test_labelling(label_type=LabelTypes.NEXT_ACTIVITY.value),
            predictive_model=create_test_predictive_model(predictive_model=PredictiveModels.CLASSIFICATION.value,
                                                          prediction_method=ClassificationMethods.RANDOM_FOREST.value)
        )
        result, _ = calculate(job)

        self.assertAlmostEqual(result['f1score'], 0.5423988458)
        self.assertAlmostEqual(result['acc'], 0.809954751)
        self.assertAlmostEqual(result['precision'], 0.623447204)
        self.assertAlmostEqual(result['recall'], 0.52249454423)
        self.assertAlmostEqual(result['auc'], 0)

    def test_regression_kmeans(self):
        self.max_diff = None
        job = create_test_job(
            clustering=create_test_clustering(clustering_type=ClusteringMethods.KMEANS.value),
            split=repair_example(),
            encoding=create_test_encoding(prefix_length=5, padding=True),
            predictive_model=create_test_predictive_model(predictive_model=PredictiveModels.REGRESSION.value,
                                                          prediction_method=RegressionMethods.RANDOM_FOREST.value)
        )
        result, _ = calculate(job)
        self.assertAlmostEqual(result['rmse'], 0.62164488)
        self.assertAlmostEqual(result['mae'], 0.00014269)
        self.assertAlmostEqual(result['rscore'], -0.11336870)
        self.assertAlmostEqual(result['mape'], float('inf'))

    def test_regression_no_cluster(self):
        self.max_diff = None
        job = create_test_job(
            clustering=create_test_clustering(clustering_type=ClusteringMethods.NO_CLUSTER.value),
            split=repair_example(),
            encoding=create_test_encoding(prefix_length=5, padding=True),
            predictive_model=create_test_predictive_model(predictive_model=PredictiveModels.REGRESSION.value,
                                                          prediction_method=RegressionMethods.RANDOM_FOREST.value)
        )
        result, _ = calculate(job)
        self.assertAlmostEqual(result['rmse'], 0.03057088)
        self.assertAlmostEqual(result['mae'], 0.00011685)
        self.assertAlmostEqual(result['rscore'], 0.13776124)
        self.assertAlmostEqual(result['mape'], float('inf'))
