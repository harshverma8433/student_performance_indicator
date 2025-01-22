import sys # The sys module in Python provides various functions and variables that are used to manipulate different parts of the Python runtime environment
import logging
def error_message_details(error , error_detail:sys):
    _,_,exc_tb = error_detail.exc_info() # this exc_tb is exttract traceback info which show that on which line which file the exception has occured basically all the information is stored in the exc_tb
    
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,
        line_number,
        str(error)
    )
    
    return error_message

class CustomException(Exception):
    def __init__(self , error_message , error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message , error_detail=error_detail)
        
    def __str__(self):
        return self.error_message
        
        
        
'''
    A class in Python is a blueprint for creating objects. It groups together data (attributes) and functions (methods) that operate on that data.
    
    The __init__ method is a special method in Python. It is called automatically when an object of the class is created.
    
    self is a reference to the current object of the class. and It’s used to access attributes and methods of the object.

    The __str__ method in Python is a special method that defines how an object is represented as a string.
    


'''

if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logging.info("Divide By Zero")
        raise CustomException(e,sys)
