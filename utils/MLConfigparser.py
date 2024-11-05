import json
import os

class MLConfigParser:
    _instance = None

    def __new__(cls, config_file='config/config.json'):
        if cls._instance is None:
            cls._instance = super(MLConfigParser, cls).__new__(cls)
            cls._instance.config_file = config_file
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as file:
                    cls._instance.config = json.load(file)
            else:
                cls._instance.config = {}
                cls._instance.save()  # Create a new file if it doesn't exist
        
        return cls._instance

    def get(self, section, option):
        """Get a value from the configuration."""
        return self.config.get(section, {}).get(option)

    def set(self, section, option, value):
        """Set a value in the configuration."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][option] = value
        self.save()

    def save(self):
        """Save the configuration back to the file."""
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file, indent=4)

    def get_ml_parameters(self):
        """Get machine learning parameters as a dictionary."""
        return self.config.get('ML_PARAMS', {})

    def get_data_paths(self):
        """Get data paths as a dictionary."""
        return self.config.get('DATA_PATHS', {})

    def get_model_parameters(self):
        """Get model parameters as a dictionary."""
        return self.config.get('MODEL_PARAMS', {})

# Usage Example
if __name__ == "__main__":
    # Create the singleton instance
    ml_config = MLConfigParser('ml_config.json')
    
    # Set some machine learning parameters
    ml_config.set('ML_PARAMS', 'learning_rate', 0.01)
    ml_config.set('ML_PARAMS', 'batch_size', 32)

    # Set some data paths
    ml_config.set('DATA_PATHS', 'train_data', '/path/to/train.csv')
    ml_config.set('DATA_PATHS', 'test_data', '/path/to/test.csv')

    # Set some model parameters
    ml_config.set('MODEL_PARAMS', 'num_epochs', 50)
    ml_config.set('MODEL_PARAMS', 'dropout_rate', 0.5)

    # Get and print all configurations
    print("ML Parameters:", ml_config.get_ml_parameters())
    print("Data Paths:", ml_config.get_data_paths())
    print("Model Parameters:", ml_config.get_model_parameters())
