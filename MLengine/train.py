import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from MLengine.Dataloader import DataLoader
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import TrainingArguments, Trainer

class ModelTrain():
    def __init__(self,configparser,logger):
        self.config = configparser
        self.logger = logger

    
    
    def tokenization(self):
        tokernizer_model = self.config.get(section="tratrainig",option="tokenizer_model")
        tokenizer = AutoTokenizer.from_pretrained(tokernizer_model)
        return tokenizer
    
    def load_model(self):
        model_name = self.config.get(section="tratrainig",option="model_name")
        id2label   = self.config.get(section="feature_engg",option="id2label")
        label2id   = self.config.get(section="feature_engg",option="label2id")
        num_labels   = self.config.get(section="feature_engg",option="num_labels")
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels, id2label=id2label, label2id=label2id)
        return model
    

    def make_encodings(self,dataset_file):
        df_org = pd.read_csv(dataset_file)
        SIZE= df_org.shape[0]

        train_texts= list(df_org.text[:SIZE//2])

        val_texts=   list(df_org.text[SIZE//2:(3*SIZE)//4 ])

        test_texts=  list(df_org.text[(3*SIZE)//4:])

        train_labels= list(df_org.label[:SIZE//2])

        val_labels=   list(df_org.label[SIZE//2:(3*SIZE)//4])

        test_labels=  list(df_org.label[(3*SIZE)//4:])

        train_encodings = self.tokenizer(train_texts, truncation=True, padding=True)
        val_encodings  = self.tokenizer(val_texts, truncation=True, padding=True)
        test_encodings = self.tokenizer(test_texts, truncation=True, padding=True)

        train_dataloader = DataLoader(train_encodings, train_labels)

        val_dataloader = DataLoader(val_encodings, val_labels)

        test_dataset = DataLoader(test_encodings, test_labels)

        return (train_dataloader,val_dataloader,test_dataset)
    
    def compute_metrics(pred):
        """
        Computes accuracy, F1, precision, and recall for a given set of predictions.

        Args:
            pred (obj): An object containing label_ids and predictions attributes.
                - label_ids (array-like): A 1D array of true class labels.
                - predictions (array-like): A 2D array where each row represents
                an observation, and each column represents the probability of
                that observation belonging to a certain class.

        Returns:
            dict: A dictionary containing the following metrics:
                - Accuracy (float): The proportion of correctly classified instances.
                - F1 (float): The macro F1 score, which is the harmonic mean of precision
                and recall. Macro averaging calculates the metric independently for
                each class and then takes the average.
                - Precision (float): The macro precision, which is the number of true
                positives divided by the sum of true positives and false positives.
                - Recall (float): The macro recall, which is the number of true positives
                divided by the sum of true positives and false negatives.
        """
        # Extract true labels from the input object
        labels = pred.label_ids

        # Obtain predicted class labels by finding the column index with the maximum probability
        preds = pred.predictions.argmax(-1)

        # Compute macro precision, recall, and F1 score using sklearn's precision_recall_fscore_support function
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='macro')

        # Calculate the accuracy score using sklearn's accuracy_score function
        acc = accuracy_score(labels, preds)

        # Return the computed metrics as a dictionary
        return {
            'Accuracy': acc,
            'F1': f1,
            'Precision': precision,
            'Recall': recall
        }
    
    def model_train(self):
        training_args = TrainingArguments(
            # The output directory where the model predictions and checkpoints will be written
            output_dir=self.config.get(section="training",option="output_dir"),
            do_train=self.config.get(section="training",option='do_train'),
            do_eval=self.config.get(section="training",option='do_eval'),
            #  The number of epochs, defaults to 3.0
            num_train_epochs=self.config.get(section="training",option='num_train_epochs'),
            per_device_train_batch_size=self.config.get(section="training",option="per_device_train_batch_size"),
            per_device_eval_batch_size=self.config.get(section="trainging",option="per_device_eval_batch_size"),
            # Number of steps used for a linear warmup
            warmup_steps=self.config.get(section="training",option="warmup_steps"),
            weight_decay=self.config.get(section="training",option="weight_decay"),
            logging_strategy=self.config.get(section="training",option="logging_strategy"),
        # TensorBoard log directory
            logging_dir=self.config.get(section="training",option="logging_dir"),
            logging_steps=self.config.get(section="training",option="logging_steps"),
            evaluation_strategy=self.config.get(section="training",option="evaluation_strategy"),
            eval_steps=self.config.get(section="training",option='eval_steps'),
            save_strategy=self.config.get(section="training",option="save_strategy"),
            fp16=self.config.get(section="training",option="fp16"),
            load_best_model_at_end=self.config.get(section="training",option="load_best_model_at_end")
        )

        trainer = Trainer(
    # the pre-trained model that will be fine-tuned
        model=self.load_model(),
        # training arguments that we defined above
        args=training_args,
        train_dataset=self.make_encodings()[0],
        eval_dataset=self.make_encodings()[1],
        compute_metrics= self.make_encodings()[2]
        )
        trainer.train()
        return trainer
    
    def save_model(self,trainer,tokenizer,model_path):
        trainer.save_model(model_path)
        tokenizer.save_pretrained(model_path)