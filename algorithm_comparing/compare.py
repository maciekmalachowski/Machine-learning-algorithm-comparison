import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from supervised import AutoML

from datasets import biology_dataset, climate_dataset, cyber_security_dataset, dating_dataset, energy_dataset, financial_dataset, housing_dataset, hr_dataset, medical_dataset, sales_dataset, student_dataset, technological_dataset

def generate_models():
    datasets = [
    biology_dataset.get_data(), 
    climate_dataset.get_data(), 
    cyber_security_dataset.get_data(),
    dating_dataset.get_data(),
    energy_dataset.get_data(),
    financial_dataset.get_data(),
    housing_dataset.get_data(),
    hr_dataset.get_data(),
    medical_dataset.get_data(),
    sales_dataset.get_data(),
    student_dataset.get_data(),
    technological_dataset.get_data(),
    ]

    algorithms=[
            # "Baseline",
            # "Linear",
            # "Decision Tree",
            # "Random Forest",
            # "Extra Trees",
            "Xgboost",
            # "LightGBM",
            # "CatBoost",
            # "Neural Network",
            # "Nearest Neighbors"
        ]

    ldb = {
            "dataset": [],
            "name": [],
            "eval_metric": [],
            "metric_value": [],
            }

    for data in datasets:
        for al in algorithms:
            # make directions
            final_path = os.path.join(f"{os.getcwd()}", f"AutoML/{data[2]}/{al}")
            if not os.path.exists(final_path):
                os.makedirs(final_path)

            if data[-1] == "reg":
                eval_metric = "mse"
            else:
                eval_metric = "accuracy"
                
            # create automl object
            automl = AutoML(
                mode="Compete", 
                total_time_limit=60, 
                results_path=final_path, 
                algorithms=[al], 
                train_ensemble=False,
                golden_features=False,
                features_selection=False,
                stack_models=False,
                kmeans_features=False,
                explain_level=0,
                boost_on_errors=False,
                eval_metric=eval_metric,
                validation_strategy={
                "validation_type": "kfold",
                "k_folds": 5,
                "shuffle": True,
                "stratify": True,
                "random_seed": 123
                },
                start_random_models=10, 
                hill_climbing_steps=3, 
                top_models_to_improve=3, 
                random_state=1234)
            
            # train automl
            automl.fit(data[0], data[1])

            # choose best model
            best_value = 0
            for m in automl._models:
                if m.get_final_loss() < 0:
                    metric_value = m.get_final_loss()*(-1)
                else:
                    metric_value = m.get_final_loss()
                if metric_value >= best_value:
                    best_value = metric_value

            # update leaderboard
            ldb["dataset"] += [data[2]]
            ldb["name"] += [m.get_type()]
            ldb["eval_metric"] += [automl._eval_metric]
            ldb["metric_value"] += [best_value]

        ldb = pd.DataFrame(ldb)
        os.makedirs('model_leaderboard', exist_ok=True)  
        ldb.to_csv('model_leaderboard/leaderboard.csv', index=False) 

def generate_plots():
    df = pd.read_csv("leaderboard.csv")
    for index, row1 in df.iterrows():
        for index, row2 in df.iterrows():
            if row1['name'] != row2['name']:
                plot_df = pd.DataFrame(data={'name': [row1['name'], row2['name']], 'metric_value': [row1['metric_value'], row2['metric_value']]})
                plot_df = plot_df.pivot(columns="name", values="metric_value")
                ax = sns.barplot(plot_df)
                ax.set(xlabel='', ylabel=row1['eval_metric']) # ylabel to change
                ax.set(ylim=(0, 1))
                plt.title(f"{row1['dataset']}: {row1['name']} - {row2['name']}")
                for i in ax.containers:
                    ax.bar_label(i,)
                if not os.path.exists(f"model_leaderboard/{row1['dataset']}"):
                    os.makedirs(f"model_leaderboard/{row1['dataset']}")
                plt.savefig(f'model_leaderboard/{row1['dataset']}/{row1['name']}-{row2['name']}.png')
                plt.close()


# generate_models()
generate_plots()

