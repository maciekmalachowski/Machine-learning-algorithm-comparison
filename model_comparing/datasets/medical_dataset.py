import pandas as pd
from sklearn.model_selection import train_test_split

def get_data():
    name = "medical"
    dataset_type = "class"
    df = pd.read_csv("https://raw.githubusercontent.com/pplonski/datasets-for-start/master/breast_cancer_wisconsin/data.csv")
    
    # split data
    train, test = train_test_split(df, train_size=0.75, shuffle=True, random_state=42)
    # create X columns list and set y column
    x_cols = ["id", "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean", "compactness_mean", "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean", "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se", "compactness_se", "concavity_se", "concave points_se", "symmetry_se", "fractal_dimension_se", "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst", "compactness_worst", "concavity_worst", "concave points_worst", "symmetry_worst", "fractal_dimension_worst"]
    y_col = "diagnosis"
    # set input matrix
    X_train = train[x_cols]
    # set target vector
    y_train = train[y_col]
    # set input matrix
    X_test = test[x_cols]
    # set target vector
    y_test = test[y_col]

    return name, X_train, X_test, y_train, y_test, dataset_type
