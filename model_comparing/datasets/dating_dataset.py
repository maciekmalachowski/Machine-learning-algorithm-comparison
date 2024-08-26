from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

def get_data():
    name = "dating"
    dataset_type = "class"
    # read data from openml page
    data = fetch_openml(data_id=40536, as_frame=True)
    X = data.data
    y = data.target
    y = y.astype("int")

    return X, y, name, dataset_type