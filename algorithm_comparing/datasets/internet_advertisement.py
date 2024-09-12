from sklearn.datasets import fetch_openml

def get_data():
    # read data from openml page
    name = "Internet_advertisements"
    dataset_type = "binary"
    data = fetch_openml(data_id=40978, as_frame=True)
    X = data.data
    y = data.target

    return X, y, name, dataset_type