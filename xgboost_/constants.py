from os.path import join, abspath, dirname, pardir

# Directories
BASE_DIR = abspath(join(dirname(__file__), pardir))
outputdir = join(BASE_DIR, 'xgboost_/features/')
scoredir = join(BASE_DIR, 'xgboost_/scores/')
modeldir = join(BASE_DIR, 'xgboost_/models/')
logdir = join(BASE_DIR,'xgboost_/')
# Files
confdir = join(BASE_DIR, 'conf.ini')

# Logging format
LOG_FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"


