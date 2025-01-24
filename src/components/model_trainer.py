import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# modelling
from sklearn.model_selection import train_test_split , RandomizedSearchCV
from sklearn.metrics import mean_squared_error , r2_score , mean_absolute_error
from sklearn.linear_model import LinearRegression , Lasso , Ridge
from sklearn.ensemble import RandomForestRegressor , AdaBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import warnings
import os,sys
from dataclasses import dataclass
from src.utils import save_object , evaluate_models
from src.exception import CustomException
from src.logger import logging

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts" , "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self,train_array , test_array):
        
        try:
            logging.info("Spliting training and test input data")
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor(), 
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }
            
            model_report:dict = evaluate_models(X_train=X_train , y_train=y_train , X_test = X_test,y_test = y_test , models=models)
            
            ## To get the best model score from dict
            best_model_scores = max(sorted(model_report.values()))

            ## To get the best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_scores)
            ]
            
            best_model = models[best_model_name]

            if best_model_scores < 0.6:
                raise CustomException("Model score is less than 0.6")
            
            
            logging.info(f"Best found model on both training and testing datatset")
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )    
            
            predicted=best_model.predict(X_test) 
            r2_sq = r2_score(y_test , predicted)
            return r2_sq
        
        except Exception as e:
           
            raise CustomException(e,sys)
        