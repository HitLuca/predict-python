"""
hyperopt methods and functionalities
"""
import hyperopt
from hyperopt import Trials, STATUS_OK, fmin, STATUS_FAIL

from src.core.core import get_encoded_logs, get_run, run_by_type
from src.hyperparameter_optimization.hyperopt_spaces import _get_space
from src.hyperparameter_optimization.models import HyperOptAlgorithms, HyperOptLosses
from src.jobs.models import Job

trial_number = 0


def calculate_hyperopt(job: Job) -> (dict, dict, dict):
    """main entry method for hyperopt calculations
    returns the predictive_model for the best trial

    :param job: job configuration
    :return: tuple containing the results, config and predictive_model split from the search
    """

    print("Start hyperopt job {} with {}, performance_metric {}".format(job.type, get_run(job),
                                                                        job.hyperparameter_optimizer.performance_metric))

    global training_df, test_df, global_job
    global_job = job
    training_df, test_df = get_encoded_logs(job, use_cache=False)  # TODO:restore to true

    space = _get_space(job)

    max_evaluations = job.hyperparameter_optimizer.max_evaluations
    trials = Trials()

    algorithm = _choose_algorithm(job)

    try:
        fmin(_calculate_and_evaluate, space, algo=algorithm.suggest, max_evals=max_evaluations, trials=trials)
    except ValueError:
        raise ValueError("All jobs failed, cannot find best configuration")
    current_best = {'loss': 100, 'results': {}, 'config': {}}
    for trial in trials:
        a = trial['result']
        if current_best['loss'] > a['loss']:
            current_best = a

    print("End hyperopt job {}, {} . Results {}".format(job.type, get_run(job), current_best['results']))
    return current_best['results'], current_best['config'], current_best['model_split']


def _get_metric_multiplier(performance_metric: int) -> int:
    """returns the multiplier to be used for each metric

    :param performance_metric: metric used
    :return: metric multiplier associated
    """
    metric_map = {HyperOptLosses.RMSE.value: -1,
                  HyperOptLosses.MAE.value: -1,
                  HyperOptLosses.RSCORE.value: 1,
                  HyperOptLosses.ACC.value: 1,
                  HyperOptLosses.F1SCORE.value: 1,
                  HyperOptLosses.AUC.value: 1,
                  HyperOptLosses.PRECISION.value: 1,
                  HyperOptLosses.RECALL.value: 1,
                  HyperOptLosses.TRUE_POSITIVE.value: 1,
                  HyperOptLosses.TRUE_NEGATIVE.value: 1,
                  HyperOptLosses.FALSE_POSITIVE.value: 1,
                  HyperOptLosses.FALSE_NEGATIVE.value: 1,
                  HyperOptLosses.MAPE.value: -1}
    return metric_map[performance_metric]


def _choose_algorithm(job: Job):
    job_algorithm = job.hyperparameter_optimizer.algorithm_type

    if job_algorithm == HyperOptAlgorithms.RANDOM_SEARCH.value:
        return hyperopt.rand
    elif job_algorithm == HyperOptAlgorithms.TPE.value:
        return hyperopt.tpe


def _calculate_and_evaluate(args) -> dict:
    global trial_number
    if trial_number % 20 == 0:
        print("Trial {}".format(trial_number))
    trial_number += 1
    local_job = global_job

    predictive_model = local_job.predictive_model.predictive_model
    prediction_method = local_job.predictive_model.prediction_method

    model_config = {'predictive_model': predictive_model, 'prediction_method': prediction_method, **args}

    print(model_config)

    performance_metric = local_job.hyperparameter_optimizer.performance_metric

    method_conf_name = "{}.{}".format(local_job.type, local_job.predictive_model.__class__.__name__)
    local_job[method_conf_name] = {**local_job[method_conf_name], **args}
    multiplier = _get_metric_multiplier(performance_metric)
    try:
        results, model_split = run_by_type(training_df.copy(), test_df.copy(), local_job)
        return {'loss': -results[performance_metric] * multiplier, 'status': STATUS_OK, 'results': results}
    except:
        return {'loss': 100, 'status': STATUS_FAIL, 'results': {}}
