
from utils.MLConfigparser import MLConfigParser
from utils.MLlogger import SingletonLogger
from MLengine.train import ModelTrain
if __name__=="__main__":
    config = MLConfigParser()
    logger = SingletonLogger()
    model = ModelTrain(configparser=config,logger=SingletonLogger)
    #tokenizar initialization
    tokenizer = model.tokenization()
    #load model
    model_loaded = model.model_loaded()
    #make encoding to fit the labels
    datset_file = config.get(section="training",option="featurized_dataset")
    encodings = model.make_encodings(dataset_file=datset_file)
    #Train model
    trained_model = model.model_train()
    #save model
    model_path = config.get(section="training",option="output_dir")
    model.save_model(trainer=trained_model,tokenizer=tokenizer,model_path=model_path)
