import lightgbm as lgb
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (RandomForestClassifier, ExtraTreesClassifier, RandomForestRegressor)
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.dummy import DummyClassifier, DummyRegressor

from tabular.ml.constants import BINARY, MULTICLASS, REGRESSION, LANGUAGE_MODEL
from tabular.ml.models.nn_nlp_classification_model import NNNLPClassificationModel
from tabular.ml.models.nn_nlp_lm_model import NNNLPLanguageModel
from tabular.ml.models.nn_tab_model import NNTabularModel
from tabular.ml.models.sklearn_model import SKLearnModel
from tabular.ml.models.lgb_model import LGBModel
from tabular.ml.models.rf_model import RFModel
from tabular.sandbox.models.lgb.parameters import get_param_baseline as lgb_get_param_baseline
from tabular.sandbox.models.nn.parameters import get_param_baseline as nn_get_param_baseline, get_nlp_param_baseline

from tabular.ml.mxnet.tabular_nn_model import TabularNeuralNetModel

def get_preset_models(path, problem_type, objective_func, num_boost_round=None, num_classes=None):
    if problem_type == BINARY:
        return get_preset_models_binary(path=path, problem_type=problem_type, objective_func=objective_func, num_boost_round=num_boost_round)
    elif problem_type == MULTICLASS:
        return get_preset_models_binary(path=path, problem_type=problem_type, objective_func=objective_func, num_boost_round=num_boost_round, num_classes=num_classes)
    elif problem_type == REGRESSION:
        return get_preset_models_regression(path=path, problem_type=problem_type, objective_func=objective_func, num_boost_round=num_boost_round)
    elif problem_type == LANGUAGE_MODEL:
        return get_preset_models_language(path=path)
    else:
        raise NotImplementedError


def get_preset_models_binary(path, problem_type, objective_func, num_boost_round=None, num_classes=None):
    models = [
        # SKLearnModel(path=path, name='DummyClassifier', model=DummyClassifier(), problem_type=problem_type, objective_func=objective_func),
        # SKLearnModel(path=path, name='GaussianNB', model=GaussianNB(), problem_type=problem_type, objective_func=objective_func),
        # SKLearnModel(path=path, name='DecisionTreeClassifier', model=DecisionTreeClassifier(), problem_type=problem_type, objective_func=objective_func),
        # RFModel(path=path, name='RandomForestClassifier', model=RandomForestClassifier(n_jobs=-1), problem_type=problem_type, objective_func=objective_func),
        # RFModel(path=path, name='RandomForestClassifierLarge', model=RandomForestClassifier(n_estimators=300, n_jobs=-1), problem_type=problem_type, objective_func=objective_func),
        # RFModel(path=path, name='RandomForestClassifierLargest', model=RandomForestClassifier(n_estimators=3000, n_jobs=-1), problem_type=problem_type, objective_func=objective_func),
        # RFModel(path=path, name='ExtraTreesClassifier', model=ExtraTreesClassifier(n_jobs=-1), problem_type=problem_type, objective_func=objective_func),
        # SKLearnModel(path=path, name='LogisticRegression', model=LogisticRegression(n_jobs=-1), problem_type=problem_type, objective_func=objective_func),
        # RFModel(path=path, name='LGBMClassifier', model=lgb.LGBMClassifier(n_jobs=-1), problem_type=problem_type, objective_func=objective_func),
        # LGBModel(path=path, name='LGBMClassifierCustom', params=lgb_get_param_baseline(problem_type, num_classes=num_classes), num_boost_round=num_boost_round, problem_type=problem_type, objective_func=objective_func),
        TabularNeuralNetModel(path=path, name='TabularNeuralNetModel', problem_type=problem_type, objective_func=objective_func),
        # NNTabularModel(path=path, name='NNTabularModel', params=nn_get_param_baseline(problem_type), problem_type=problem_type, objective_func=objective_func) # OG fast.ai model. TODO: remove!
        # NNNLPClassificationModel(path=path, name='NNNLPClassificationModel-FWD', params=get_nlp_param_baseline(), problem_type=problem_type, objective_func=objective_func),
        # NNNLPClassificationModel(path=path, name='NNNLPClassificationModel-BWD', params=get_nlp_param_baseline(), problem_type=problem_type, objective_func=objective_func, train_backwards=True),
    ]
    return models


def get_preset_models_language(path):
    models = [
        NNNLPLanguageModel(path=path, name='NLPLanguageModel', params=get_nlp_param_baseline()),
    ]
    return models


def get_preset_models_regression(path, problem_type, objective_func, num_boost_round=None):
    models = [
        SKLearnModel(path=path, name='DummyRegressor', model=DummyRegressor(), problem_type=problem_type, objective_func=objective_func),
        RFModel(path=path, name='RandomForestRegressor', model=RandomForestRegressor(n_jobs=-1), problem_type=problem_type, objective_func=objective_func),
        # SKLearnModel(path=path, name='LGBMRegressor', model=lgb.LGBMRegressor(n_jobs=-1, verbose=2, silent=False), problem_type=problem_type, objective_func=objective_func),
        LGBModel(path=path, name='LGBMRegressorCustom', params=lgb_get_param_baseline(problem_type), num_boost_round=num_boost_round, problem_type=problem_type, objective_func=objective_func),
        NNTabularModel(path=path, name='NNTabularModel', params=nn_get_param_baseline(problem_type), problem_type=problem_type, objective_func=objective_func),
    ]
    return models