from sklearn.datasets import fetch_openml

def get_data():
    # read data from openml page
    name = "Banknote_authentication"
    dataset_type = "binary"
    data = fetch_openml(data_id=1462, as_frame=True)
    X = data.data
    y = data.target

    return X, y, name, dataset_type