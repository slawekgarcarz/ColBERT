#TODO: apply this to all the other files
import os
import path

SRC_DIR = path.Path(os.path.abspath(os.path.dirname(__file__))).abspath()
DATA_DIR = path.Path(os.path.dirname(__file__)).joinpath("./data").abspath()
RESULTS_DIR = path.Path(os.path.dirname(__file__)).joinpath("./results").abspath()
CORRECT_RESULTS_DIR = path.Path(os.path.dirname(__file__)).joinpath("./correct_results").abspath()
JOBS_DIR = path.Path(os.path.dirname(__file__)).joinpath("./jobs").abspath()
LOGS_DIR = path.Path(os.path.dirname(__file__)).joinpath("./logs").abspath()
