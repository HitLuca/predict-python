from django_rq.decorators import job

from core.core import calculate
from jobs.models import Job, CREATED, RUNNING, COMPLETED, ERROR
from predModels.models import ModelSplit, PredModels
from sklearn.externals import joblib
from core.constants import KMEANS


@job("default", timeout='1h')
def prediction_task(job_id):
    print("Start prediction task ID {}".format(job_id))
    job = Job.objects.get(id=job_id)
    try:
        if job.status == CREATED:
            job.status = RUNNING
            job.save()
            result,model_split = calculate(job.to_dict())
            if job.config['create_models']:
                save_models(model_split,job)
            job.result = result
            job.status = COMPLETED
    except Exception as e:
        print("error " + str(e.__repr__()))
        job.status = ERROR
        job.error = str(e.__repr__())
        raise e
    finally:
        job.save()

def save_models(to_model_split,job):
    print("Start saving models of JOB {}".format(job.id))
    jobsplit = job.split
    if jobsplit.type == 'single':
        log = jobsplit.original_log
    else:
        log = jobsplit.training_log
    filename_model = 'model_cache/split_{}-model-{}.sav'.format(job.split.id,job.type)
    joblib.dump(to_model_split['model'], filename_model)
    model_split, created = ModelSplit.objects.get_or_create(type=to_model_split['type'], model_path=filename_model, predtype=job.type)
    if to_model_split['type'] == KMEANS:
        filename_estimator = 'model_cache/split_{}-estimator-{}.sav'.format(job.split.id,job.type)
        joblib.dump(to_model_split['estimator'], filename_estimator)
        model_split.estimator_path=filename_estimator
        model_split.save()
    models = PredModels.objects.create(split=model_split, type=job.type, log = log, config = job.config)
    return 1