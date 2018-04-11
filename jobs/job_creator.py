from core.constants import CLASSIFICATION, all_configs, CLASSIFICATION_RANDOM_FOREST, CLASSIFICATION_KNN, \
    CLASSIFICATION_DECISION_TREE, REGRESSION_RANDOM_FOREST, REGRESSION_LASSO, REGRESSION_LINEAR, \
    NEXT_ACTIVITY_RANDOM_FOREST, NEXT_ACTIVITY_KNN, NEXT_ACTIVITY_DECISION_TREE
from jobs.models import Job, CREATED


def generate(split, payload, type=CLASSIFICATION):
    jobs = []

    for encoding in payload['config']['encodings']:
        for clustering in payload['config']['clusterings']:
            for method in payload['config']['methods']:
                item = Job.objects.create(
                    split=split,
                    status=CREATED,
                    type=type,
                    config=create_config(payload, encoding, clustering, method))
                jobs.append(item)
    return jobs


def create_config(payload, encoding, clustering, method):
    """Turn lists to single values"""
    config = dict(payload['config'])
    del config['encodings']
    del config['clusterings']
    del config['methods']

    # Extract and merge configurations
    method_conf_name = "{}.{}".format(payload['type'], method)
    method_conf = {**CONF_MAP[method_conf_name](), **payload['config'].get(method_conf_name, dict())}
    # Remove configs that are not needed for this method
    for any_conf_name in all_configs:
        try:
            del config[any_conf_name]
        except KeyError:
            pass
    config[method_conf_name] = method_conf
    config['encoding'] = encoding
    config['clustering'] = clustering
    config['method'] = method
    return config


# Default configurations
def _classification_random_forest():
    return {
        'n_estimators': 10,
        'criterion': 'gini',
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1
    }


def _classification_knn():
    return {
        'n_neighbors': 5,
        'weights': 'uniform'
    }


def _classification_decision_tree():
    return {
        'criterion': 'gini',
        'splitter': 'best',
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1
    }


def _regression_random_forest():
    return {
        'n_estimators': 10,
        'criterion': 'mse',
        'max_depth': None,
        'min_samples_split': 2
    }


def _regression_lasso():
    return {
        'alpha': 1.0,
        'fit_intercept': True,
        'normalize': False,
        'copy_X': True
    }


def _regression_linear():
    return {
        'fit_intercept': True,
        'normalize': False,
        'copy_X': True
    }


# Map method config to a dict
CONF_MAP = {CLASSIFICATION_RANDOM_FOREST: _classification_random_forest, CLASSIFICATION_KNN: _classification_knn,
            CLASSIFICATION_DECISION_TREE: _classification_decision_tree,
            REGRESSION_RANDOM_FOREST: _regression_random_forest,
            REGRESSION_LASSO: _regression_lasso, REGRESSION_LINEAR: _regression_linear,
            NEXT_ACTIVITY_RANDOM_FOREST: _classification_random_forest, NEXT_ACTIVITY_KNN: _classification_knn,
            NEXT_ACTIVITY_DECISION_TREE: _classification_decision_tree}
