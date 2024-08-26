from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

def get_data():
    # read data from openml page
    name = "cyber_security"
    dataset_type = "class"
    data = fetch_openml(data_id=4534, as_frame=True)
    X = data.data
    y = data.target
   
    return X, y, name, dataset_type