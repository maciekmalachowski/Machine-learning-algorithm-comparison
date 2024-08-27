from sklearn.datasets import fetch_openml

def get_data():
    # read data from openml page
    name = "climate"
    dataset_type = "class"
    data = fetch_openml(data_id=1467, as_frame=True)
    X = data.data
    y = data.target

    return X, y, name, dataset_type