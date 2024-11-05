from utils.MLConfigparser import MLConfigParser
from utils.MLlogger import SingletonLogger
from data_preparation.prepare import data_preparation
import os
if __name__ == "__main__":
    print(os.getcwd())
    config = MLConfigParser("config/config.json")
    logger = SingletonLogger()
    data =  data_preparation()
    ###############step 1 ######################
    logger.info("downloading dataset")
    dataset_url = config.get(section="data_preprocessing",option="dataset_url")
    output_dir = config.get(section="data_preprocessing",option="dataset_output_dir")
    data.download_and_extract_zip(url=dataset_url,output_dir=output_dir)
    logger.info("downloaded dataset")
    ########################step 2 ####################
    tsv_filepath = config.get(section="data_preprocessing",option="tsv_filename")
    csv_filename =config.get(section="data_preprocessing",option="output_csv")
    data.convert_tsv_to_csv(tsv_filepath,csv_filename)
    logger.info("dataset converted into csv")
    ################### step 3 #####################
    feature_selection = config.get(section="data_preprocessing",option="output_csv")
    print(feature_selection)
    final_dataset = config.get(section="data_preprocessing",option="featurized_dataset_outputfile")
    data.merge_and_save_columns(feature_selection,final_dataset)
    logger.info("final data set is ready")
