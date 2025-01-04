import os
import yaml
from dotenv import load_dotenv

# Function to load configuration settings
def load_config():
    """_summary_

    Returns:
        _type_: _description_
    """
    load_dotenv()

    # Load the YAML configuration file
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as stream:
        config = yaml.safe_load(stream)
    
    config['DATABASE']['DIR_PATH'] = os.getenv('LOCAL_DATABASE_ROOT_DIR', config['DATABASE']['DIR_PATH'])

    return config