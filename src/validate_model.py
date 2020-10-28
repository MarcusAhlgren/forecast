import datetime
import numpy as np
import joblib
import optuna
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
import warnings
warnings.simplefilter("ignore")

def rmse(y_actual, y_predicted):
    rmse = np.sqrt(mean_squared_error(y_actual, y_predicted))
    return rmse

def save_model(model, path):
    joblib.dump(value = model, filename = path, compress=('bz2', 9))
    
def load_model(path):
    model = joblib.load(path)
    return model

class SARIMA(SARIMAX):
    def __init__(self, endog, **kwargs):
        super().__init__(endog, **kwargs)
        
    def train(self):
        self.model = self.fit()

    def pred(self, steps = 12, start = None, end = None):
        if start != None and end != None:
            preds = self.model.predict(start = start, end = end)
        else:
            preds = self.model.forecast(steps)
        return preds
        
class Pipeline:
    def __init__(self, train, test, n_validation_years = 3):
        self.train = train
        self.test = test
        self.n_folds = n_validation_years
    
    def gen_folds(self):
        folds = []
        for n in reversed(range(self.n_folds)):
            folds.append({"train": self.train.iloc[:-12*(n+1)],
                          "test": self.train.iloc[-12*(n+1):].iloc[:12]})
        self.folds = folds
    
    def validate_model(self, params):
        if not hasattr(self, "folds"):
            self.gen_folds()
        
        loss = 0
        for n, fold in enumerate(self.folds):
            #define and train model
            model = SARIMA(fold["train"], **params)
            model.train()
            
            #make predictions
            preds = model.pred(start = fold["test"].index[0], end = fold["test"].index[-1])
            fold["preds"] = preds
            
            #compute and print loss
            fold_loss = rmse(fold["test"], fold["preds"])
            fold["loss"] = fold_loss
            print(f"Fold {n} loss: {fold_loss}")
            
            loss += fold_loss / self.n_folds
        return loss
    
    def objective(self, trial):
        
        static_params = {"freq": "MS",
                         "trend": "c"}
        
        hyperparams = {
            "order": (trial.suggest_int("p", 0, 2),
                      trial.suggest_int("d", 1, 2),
                      trial.suggest_int("q", 0, 2)),
            "seasonal_order": (trial.suggest_int("P", 0, 2),
                               trial.suggest_int("D", 1, 2),
                               trial.suggest_int("Q", 0, 2), 24)
        }
        
        
        params = {**static_params, **hyperparams}
        loss = self.validate_model(params)
        return loss
    
    def optimize_hyperparams(self, n_trials = 3):
            study = optuna.create_study(direction = "minimize")
            study.optimize(self.objective, n_trials = n_trials, gc_after_trial = True)
            self.study = study