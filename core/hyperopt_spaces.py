import numpy as np
from hyperopt import hp
from hyperopt.pyll.base import scope

from core.constants import *


def get_space(job: dict):
    method_conf_name = "{}.{}".format(job['type'], job['method'])
    return HYPEROPT_SPACE_MAP[method_conf_name]()


def _classification_random_forest():
    return {
        'n_estimators': hp.choice('n_estimators', np.arange(150, 1000, dtype=int)),
        'max_depth': scope.int(hp.quniform('max_depth', 4, 30, 1)),
        'max_features': hp.uniform('max_features', 0.0, 1.0)
    }


# test case dynamic max feature
def _classification_knn():
    return {
        'n_neighbors': hp.choice('n_neighbors', np.arange(1, 20, dtype=int)),
        'weights': hp.choice('weights', ['uniform', 'distance']),
    }


def _classification_decision_tree():
    return {
        'max_depth': scope.int(hp.quniform('max_depth', 4, 30, 1)),
        'min_samples_split': hp.choice('min_samples_split', np.arange(2, 10, dtype=int)),
        'min_samples_leaf': hp.choice('min_samples_leaf', np.arange(1, 10, dtype=int)),
    }


def _classification_xgboost():
    return {
        'n_estimators': hp.choice('n_estimators', np.arange(150, 1000, dtype=int)),
        'max_depth': scope.int(hp.quniform('max_depth', 3, 30, 1)),
    }


def _classification_incremental_naive_bayes():
    return {
        'alpha': hp.uniform('alpha', 0.001, 10.0),
        'fit_prior': hp.choice('fit_prior', [ True, False ])
    }


def _classification_incremental_adaptive_tree():
    return {
        'grace_period': hp.uniform('grace_period', 1, 200),
        'split_criterion': hp.choice('split_criterion', [ 'gini', 'info_gain' ]),
        'split_confidence': hp.uniform('split_confidence', .0000001, .0000009),
        'tie_threshold': hp.uniform('tie_threshold', 0.01, .09),
        'binary_split': hp.choice('binary_split', [ True, False ]),
        'stop_mem_management': hp.choice('stop_mem_management', [ True, False ]),
        'remove_poor_atts': hp.choice('remove_poor_atts', [ True, False ]),
        'no_preprune': hp.choice('no_preprune', [ True, False ]),
        'leaf_prediction': hp.choice('leaf_prediction', [ 'mc', 'nb', 'nba']),
        'nb_threshold': hp.uniform('nb_threshold', 0.0, 1.0)
    }


def _classification_incremental_hoeffding_tree():
    return {
        'grace_period': hp.uniform('grace_period', 1, 200),
        'split_criterion': hp.choice('split_criterion', [ 'gini', 'info_gain' ]),
        'split_confidence': hp.uniform('split_confidence', .0000001, .0000009),
        'tie_threshold': hp.uniform('tie_threshold', 0.01, .09),
        'binary_split': hp.choice('binary_split', [ True, False ]),
        'stop_mem_management': hp.choice('stop_mem_management', [ True, False ]),
        'remove_poor_atts': hp.choice('remove_poor_atts', [ True, False ]),
        'no_preprune': hp.choice('no_preprune', [ True, False ]),
        'leaf_prediction': hp.choice('leaf_prediction', [ 'mc', 'nb', 'nba']),
        'nb_threshold': hp.uniform('nb_threshold', 0.0, 1.0)
    }


def _regression_random_forest():
    return {
        'n_estimators': hp.choice('n_estimators', np.arange(150, 1000, dtype=int)),
        'max_features': hp.uniform('max_features', 0.0, 1.0),
        'max_depth': scope.int(hp.quniform('max_depth', 4, 30, 1)),
    }


def _regression_lasso():
    return {
        'alpha': hp.uniform('alpha', 0.01, 2.0),
        'fit_intercept': hp.choice('fit_intercept', [True, False]),
        'normalize': hp.choice('normalize', [True, False])
    }


def _regression_linear():
    return {
        'fit_intercept': hp.choice('fit_intercept', [True, False]),
        'normalize': hp.choice('normalize', [True, False])
    }


def _regression_xgboost():
    return {
        'max_depth': scope.int(hp.quniform('max_depth', 3, 100, 1)),
        'n_estimators': hp.choice('n_estimators', np.arange(150, 1000, dtype=int)),
    }


HYPEROPT_SPACE_MAP = {
    CLASSIFICATION_RANDOM_FOREST: _classification_random_forest,
    CLASSIFICATION_KNN: _classification_knn,
    CLASSIFICATION_XGBOOST: _classification_xgboost,
    CLASSIFICATION_DECISION_TREE: _classification_decision_tree,
    CLASSIFICATION_INCREMENTAL_NAIVE_BAYES: _classification_incremental_naive_bayes,
    CLASSIFICATION_INCREMENTAL_ADAPTIVE_TREE: _classification_incremental_adaptive_tree,
    CLASSIFICATION_INCREMENTAL_HOEFFDING_TREE: _classification_incremental_hoeffding_tree,
    REGRESSION_RANDOM_FOREST: _regression_random_forest,
    REGRESSION_XGBOOST: _regression_xgboost,
    REGRESSION_LASSO: _regression_lasso,
    REGRESSION_LINEAR: _regression_linear
}
