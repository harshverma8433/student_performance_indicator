import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
# ColumnTransformer is used to create a pipleline where multiple transformer are chained together.
from sklearn.impute import SimpleImputer # for missing values
from sklearn.pipeline import Pipeline # for creating a pipeline
from sklearn.preprocessing import OneHotEncoder # for categorical data
from sklearn.preprocessing import StandardScaler # for scaling the data

from ..exception import CustomException
from ..logger import logging
from ..utils import save_object

@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")
class DataTransformation:
    def __init__(self):
        self.data_transformationConfig = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        
        '''
            this function is responsible for the data transformation
        '''
        try:
            num_cols = ["writing_score" , "reading_score"]
            cat_cols = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer" , SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer" , SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder(sparse_output=True)),
                    ("scaler",StandardScaler(with_mean=False))                    
                ]
            )
            
            logging.info("Numerical columns standard scaling completed")
            
            logging.info("Categorical columns encoding completed")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline" , num_pipeline,num_cols),
                    ("cat_pipeline" , cat_pipeline,cat_cols)
                ]
            )
            
            return preprocessor
        
        except Exception as e:
            raise CustomException(e , sys)
    
    def initiate_data_transformation(self,train_path , test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Read train and test data completed")

            logging.info("Obtaining Preprocessing object")
            
            preprocessing_obj = self.get_data_transformer_object()

            target_col_names = "math_score" 
            numerical_cols = ["writing_score" , "reading_score"]
            
            input_features_train_df = train_df.drop(columns=[target_col_names] , axis=1)
            target_feature_train_df=train_df[target_col_names]

            input_feature_test_df=test_df.drop(columns=[target_col_names],axis=1)
            target_feature_test_df=test_df[target_col_names]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformationConfig.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformationConfig.preprocessor_obj_file_path,
            )
             
        except Exception as e:
            raise CustomException(e , sys)
        