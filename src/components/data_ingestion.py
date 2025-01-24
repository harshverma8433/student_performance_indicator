'''
    data ingestion - It involves collecting raw data from various sources and converting it into a format that can be easily analyzed and processed
'''

import os
import sys

from ..logger import logging
from ..exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Define the data class 
# Defines paths for the raw data, training data, and testing data files
@dataclass
class DataIngestionConfig:
    train_data_path : str=os.path.join('artifact' , "train.csv")
    test_data_path : str=os.path.join('artifact' , "test.csv")
    raw_data_path : str=os.path.join('artifact' , "raw.csv")


# This class orchestrates the data ingestion process.
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    #This method handles the ingestion process
    def initiate_data_ingestion(self):
        logging.info("ENter the data ingestion method or commponent")
        try:
            # Read the raw data from the file
            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir, "../../notebook/dataset/StudentsPerformance.csv")
            df = pd.read_csv(file_path)
            logging.info('Read the dataset as dataframe')
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set , test_set = train_test_split(df , test_size=0.2 , random_state=42 )

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            
            logging.info("Ingestion of data is completed")
            
            return(
                self.ingestion_config.train_data_path ,
                self.ingestion_config.test_data_path ,
                
            )
            
        except Exception as e:
            raise CustomException (e,sys)


if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()