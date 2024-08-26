import os
from supervised import AutoML
from sklearn.metrics import accuracy_score, mean_squared_error

from datasets import biology_dataset, climate_dataset, cyber_security_dataset, dating_dataset, energy_datset, financial_dataset, housing_dataset, hr_dataset, medical_dataset, sales_dataset, student_dataset, technological_dataset

datasets = [
    biology_dataset.get_data(), 
    # climate_dataset.get_data(), 
    # cyber_security_dataset.get_data(), 
    # dating_dataset.get_data(),
    # energy_datset.get_data(),
    # financial_dataset.get_data(),
    housing_dataset.get_data(),
    # hr_dataset.get_data(),
    # medical_dataset.get_data(),
    # sales_dataset.get_data(),
    # student_dataset.get_data(),
    # technological_dataset.get_data(),
    ]
algorithms=[
        # "Baseline",
        # "Linear",
        # "Decision Tree",
        # "Random Forest",
        # "Extra Trees",
        "Xgboost",
        "LightGBM",
        # "CatBoost",
        # "Neural Network",
        # "Nearest Neighbors"
    ]

for data in datasets:
    for al in algorithms:
        # make directions
        final_path = os.path.join(f"{os.getcwd()}", f"AutoML/{data[0]}/{al}")
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        # create automl object
        if data[-1] == "reg":
            eval_metric = "mse"
        else:
            eval_metric = "accuracy"
        automl = AutoML(
            mode="Explain", 
            total_time_limit=300, 
            results_path=final_path, 
            algorithms=[al], 
            train_ensemble=False,
            eval_metric=eval_metric,
            start_random_models=10, 
            hill_climbing_steps=3, 
            top_models_to_improve=3, 
            random_state=1234)
        # train automl
        automl.fit(data[1], data[3])

        automl.predict(data[2])