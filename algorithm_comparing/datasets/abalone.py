from sklearn.datasets import fetch_openml

def get_data():
    # read data from openml page
    name = "Abalone"
    dataset_type = "reg"
    data = fetch_openml(data_id=42726, as_frame=True)
    X = data.data
    y = data.target

    return X, y, name, dataset_type