from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

def get_data():
    # read data from openml page
    name = "biology"
    dataset_type = "class"
    data = fetch_openml(data_id=1494, as_frame=True)
    X = data.data
    y = data.target
    # split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.90, shuffle=True, stratify=y, random_state=42)

    return name, X_train, X_test, y_train, y_test, dataset_type