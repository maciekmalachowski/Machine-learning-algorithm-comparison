from sklearn.datasets import fetch_openml

def get_data():
    # read data from openml page
    name = "Speed Dating"
    dataset_type = "class"
    data = fetch_openml(data_id=40536, as_frame=True)
    X = data.data
    y = data.target
    y = y.astype("int")

    return X, y, name, dataset_type