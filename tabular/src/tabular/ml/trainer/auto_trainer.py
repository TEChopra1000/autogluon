
from tabular.ml.trainer.abstract_trainer import AbstractTrainer
from tabular.ml.models.model_presets.presets import get_preset_models


# Trainer handles model training details
class AutoTrainer(AbstractTrainer):
    def __init__(self, path, problem_type, objective_func=None, num_classes=None, low_memory=False, feature_types_metadata={}, compute_feature_importance=False, searcher=None, scheduler=None):
        super().__init__(path=path, problem_type=problem_type, objective_func=objective_func, num_classes=num_classes, low_memory=low_memory, feature_types_metadata=feature_types_metadata, compute_feature_importance=compute_feature_importance, searcher=searcher, scheduler=scheduler)
        self.num_boost_round = 100000

    def get_models(self):
        return get_preset_models(path=self.path, problem_type=self.problem_type, objective_func=self.objective_func, num_boost_round=self.num_boost_round, num_classes=self.num_classes)

    def train(self, X_train, y_train, X_test=None, y_test=None, hyperparameter_tune=False, feature_prune=False):
        models = self.get_models()
        
        if (y_test is None) or (X_test is None):
            X_train, X_test, y_train, y_test = self.generate_train_test_split(X_train, y_train)
        
        self.train_multi_and_ensemble(X_train, X_test, y_train, y_test, models, hyperparameter_tune=hyperparameter_tune, feature_prune=feature_prune)