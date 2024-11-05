import pandas as pd


class FeatureEngineering():
    def __init__(self,configparser,logger):
        self.config = configparser
        self.logger = logger
        

    def load_dataset(self,csvfile_path):
        final_dataset = self.config.get(section="feature_engg",option="featurized_dataset")
        df_org= pd.read_csv(csvfile_path)
        df_org = df_org.dropna()
        self.logger.info("dropping nan values")
        df_org = df_org[['text', 'label']] #keeping only required data
        self.logger.info("loaded dataset,removed nan values,keeping required data")
        df_org.to_csv(final_dataset)
    
    def encoding_labels(self,datset_path):
        df_org = pd.read_csv(datset_path)
        labels = df_org['label'].unique().tolist()
        num_labels = len(labels)
        id2label={id:label for id,label in enumerate(labels)}

        label2id={label:id for id,label in enumerate(labels)}

        self.config.set(section="feature_engg",option="id2label",value=id2label)
        self.config.set(section="feature_engg",option="label2id",value=label2id)
        self.config.set(section="feature_engg",option="num_labels",value=num_labels)

        df_org["label"]=df_org.label.map(lambda x: label2id[x.strip()])

        return df_org
    



