# # In your main script:
# import sys
# from src.logger import logggggg # (Your logger from earlier!)
# from src.exception import CustomException

# logger = logggggg()

# try:
#     # Let's say we try to open a file that doesn't exist
#     with open("missing_file.txt", "r") as f:
#         data = f.read()

# except Exception as e:
#     # 1. Create our custom exception
#     logger.info(e)
#     custom_error = CustomException(e, sys)
    
#     # 2. Log it using our custom logger (it will go to logs/ folder)
#     logger.error(custom_error)
    
#     # 3. Stop the script
#     raise custom_error

from src.pipline.training_pipeline import TrainingPipeline
pipeline = TrainingPipeline()
pipeline.run_pipeline()