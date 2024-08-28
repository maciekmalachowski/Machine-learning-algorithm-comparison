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
        "Baseline",
        # "Linear",
        "Decision Tree",
        "Random Forest",
        "Extra Trees",
        "Xgboost",
        "LightGBM",
        "CatBoost",
        "Neural Network",
        "Nearest Neighbors"
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
            if not os.path.exists(f"AutoML/{data[2]}/{al}"):
                os.makedirs(f"AutoML/{data[2]}/{al}")

            if data[-1] == "reg":
                eval_metric = "mse"
            else:
                eval_metric = "accuracy"
                
            # create automl object
            automl = AutoML(
                mode="Compete", 
                total_time_limit=60, 
                results_path=f"AutoML/{data[2]}/{al}", 
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

        df = pd.DataFrame(ldb)
        os.makedirs('model_leaderboard', exist_ok=True)  
        df.to_csv('model_leaderboard/leaderboard.csv', index=False) 

def generate_plots():
    df = pd.read_csv("model_leaderboard/leaderboard.csv")
    datasets = df['dataset'].unique()
    algorithms = df['name'].unique()
    used_combos = []

    for alg1 in algorithms:
        for alg2 in algorithms:
            for data in datasets:
                if alg1 != alg2:
                    if (f"{data}-{alg1}-{alg2}" and f"{data}-{alg2}-{alg1}") not in used_combos:
                        metric1 = df.loc[(df['dataset']==data) & (df['name']==alg1), 'metric_value'].item()
                        metric2 = df.loc[(df['dataset']==data) & (df['name']==alg2), 'metric_value'].item()
                        plot_df = pd.DataFrame(data={'name': [alg1, alg2], 'metric_value': [metric1, metric2]})
                        plot_df = plot_df.pivot(columns="name", values="metric_value")

                        ax = sns.barplot(plot_df)
                        if metric1 > metric2:
                            ax.plot(0, 0.5, "*", markersize=50, color="yellow")

                        elif metric1 < metric2:
                            ax.plot(1, 0.5, "*", markersize=50, color="yellow")

                        ax.set(xlabel='', ylabel=df.loc[(df["dataset"]==data) & (df['name']==alg1), 'eval_metric'].to_numpy()[0])

                        plt.title(f"{data}")
                        for i in ax.containers:
                            ax.bar_label(i,)
                        
                        if df.loc[(df["dataset"]==data) & (df['name']==alg1), 'eval_metric'].to_numpy()[0] == 'accuracy':
                            ax.set(ylim=(0, 1))
                        
                        name1 = alg1.replace(" ", "-").lower()
                        name2 = alg2.replace(" ", "-").lower()
                        data_name = data.replace(" ", "-").lower()
                        
                        if not os.path.exists(f"model_leaderboard/{name1}-vs-{name2}"):
                            os.makedirs(f"model_leaderboard/{name1}-vs-{name2}")
                        plt.savefig(f'model_leaderboard/{name1}-vs-{name2}/{data_name}_{name1}-vs-{name2}.png')
                        plt.close()
                        
                        used_combos.append(f"{data}-{alg1}-{alg2}")
                        used_combos.append(f"{data}-{alg2}-{alg1}")

# generate_models()
generate_plots()

