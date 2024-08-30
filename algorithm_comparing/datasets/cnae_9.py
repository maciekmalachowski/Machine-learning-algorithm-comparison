from sklearn.datasets import fetch_openml

def get_data():
    # read data from openml page
    name = "cnae_9"
    dataset_type = "multi"
    data = fetch_openml(data_id=1468, as_frame=True)
    X = data.data
    y = data.target

    return X, y, name, dataset_type