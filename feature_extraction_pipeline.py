from utils.MLConfigparser import MLConfigParser
from utils.MLlogger import SingletonLogger
from feature_extraction.feature_engineering import FeatureEngineering


if __name__ =="__main__":
    config = MLConfigParser()
    logger = SingletonLogger()
    dataset_file = config.get(section="feature_engg",option="dataset_filelocation")
    featureengg = FeatureEngineering(configparser=config,logger=logger)
    ###############loading dataset##################
    df = featureengg.load_dataset(dataset_file)
    logger.info('feature engineering is complete')
    
