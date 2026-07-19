import logging 
import sys 

def error_handler(error_message: str, error_key: sys):
    """
    Handles errors by returning a formatted error message.

    Args:
        error_message (str): The raw error message.
        error_key (sys): The sys module to get the exception information.
    """
    # Get the exception information
    _, _, exc_tb = error_key.exc_info()
    
    filename = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    
    # Format the message
    message = f"Error in file: {filename}, line: {line_number} - {error_message}"
    
    # We remove the logging.error() from here because you usually 
    # want to log the exception inside your main script's try/except block.
    
    return message # FIXED: Return the string, do not raise it!


class CustomException(Exception):
    """
    Custom exception class that extends the built-in Exception class.
    """

    def __init__(self, error_message: str, error_key: sys):
        """
        Initializes the CustomException with an error message and sys module.

        Args:
            error_message (str): The error message.
            error_key (sys): The sys module to get the exception information.
        """
        super().__init__(error_message)
        self.error_message = error_handler(error_message, error_key)
        
    def __str__(self):
        """
        Returns a string representation of the CustomException.
        """
        return self.error_message