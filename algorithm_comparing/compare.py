import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from supervised import AutoML

from datasets import abalone, adult, airlines_depdelay_1m,  allstate_claims_severity, amazon_commerce_reviews, amazon_employee_access, apsfailure, bank_marketing, banknote_authentication, bioresponse, black_friday, boston, buzzinsocialmedia_twitter, car, churn, click_prediction_small, cnae_9, colleges, connect_4, credit_approval, credit_g, diabetes, diamonds, electricity, higgs, house_sales, internet_advertisement, kddcup09_churn, kddcup09_upselling, mfeat_factors, moneyball, nyc_taxi_gree_dec2016, onlinenewspopularity, phishing_websites, santander_transaction_volume, segment, space_ga, spambase, us_crime, vehicle, wdbc, wine_quality

def generate_models():
    datasets = [
        abalone.get_data(), 
        # adult.get_data(), 
        # airlines_depdelay_1m.get_data(), 
        # allstate_claims_severity.get_data(), 
        # amazon_commerce_reviews.get_data(), 
        # amazon_employee_access.get_data(), 
        # apsfailure.get_data(), 
        # bank_marketing.get_data(), 
        # banknote_authentication.get_data(), 
        # bioresponse.get_data(), 
        # black_friday.get_data(), # more time needed
        # boston.get_data(), 
        # buzzinsocialmedia_twitter.get_data(), # more time needed
        # car.get_data(), 
        # churn.get_data(), 
        # click_prediction_small.get_data(), 
        # cnae_9.get_data(), 
        # colleges.get_data(), 
        # connect_4.get_data(), # more time needed
        # credit_approval.get_data(), 
        # credit_g.get_data(), 
        # diabetes.get_data(), 
        # diamonds.get_data(), 
        # electricity.get_data(), 
        # higgs.get_data(), 
        # house_sales.get_data(), 
        # internet_advertisement.get_data(), 
        # kddcup09_churn.get_data(), 
        # kddcup09_upselling.get_data(), 
        # mfeat_factors.get_data(), 
        # moneyball.get_data(), 
        # nyc_taxi_gree_dec2016.get_data(), # more time needed 
        # onlinenewspopularity.get_data(), 
        # phishing_websites.get_data(), 
        # santander_transaction_volume.get_data(),
        # segment.get_data(), 
        # space_ga.get_data(), 
        # spambase.get_data(), 
        # us_crime.get_data(), 
        # vehicle.get_data(), 
        # wdbc.get_data(), 
        # wine_quality.get_data() 
    ]

    algorithms=[
            'Baseline',
            'CatBoost',
            'Decision Tree',
            'Extra Trees',
            'LightGBM',
            # 'Nearest Neighbors',
            'Neural Network',
            'Random Forest',
            'Xgboost'
    ]

    ldb = {
            "dataset": [],
            "dataset_type": [],
            "name": [],
            "eval_metric": [],
            "metric_value": [],
            }

    for data in datasets:
        for al in algorithms:
            # create directions for AutoML
            if not os.path.exists(f"AutoML/{data[2]}/{al}"):
                os.makedirs(f"AutoML/{data[2]}/{al}")
            
            # various datasets need either rmse or accuracy as metric
            if data[-1] == "reg":
                eval_metric = "rmse"
            else:
                eval_metric = "accuracy"
                
            # create automl object
            automl = AutoML(
                mode="Compete", 
                total_time_limit=600, 
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

            # choose best model metric value
            if eval_metric == "rmse":
                best_value = pow(10,10)
            else:
                best_value = 0

            for m in automl._models:
                metric_value = m.get_final_loss()
                if eval_metric == "rmse":
                    if metric_value <= best_value:
                        best_value = metric_value
                else:
                    if metric_value >= best_value:
                        best_value = metric_value

            # update leaderboard
            ldb["dataset"] += [data[2]]
            ldb["dataset_type"] += [data[-1]]
            ldb["name"] += [m.get_type()]
            ldb["eval_metric"] += [automl._eval_metric]
            ldb["metric_value"] += [best_value]
            
            # save dataframe made of ldb to csv 
            df = pd.DataFrame(ldb)
            # os.makedirs('algorithms_info', exist_ok=True) 
            df.to_csv('algorithms_info/algorithm_leaderboard.csv', index=False) 

            del df

def compare():
    df = pd.read_csv("algorithms_info/algorithm_leaderboard.csv")
    datasets = df['dataset'].unique()
    algorithms = df['name'].unique()
    used_combos = []

    # comparison of algorithms each with each 
    for alg1 in algorithms:
        for alg2 in algorithms:
            if alg1 != alg2:
                name1 = alg1.replace(" ", "-").lower()
                name2 = alg2.replace(" ", "-").lower()
                score = {
                    name1: {
                        "binary": 0,
                        "multi": 0,
                        "reg": 0
                    },
                    name2: {
                        "binary": 0,
                        "multi": 0,
                        "reg": 0
                    },
                    "win": ""
                }
                # each comparison uses each dataset
                for data in datasets:
                    data_name = data.replace(" ", "-").lower()
                    # protection against comparing the same algorithms twice
                    if (f"{data_name}-{alg1}-{alg2}" and f"{data_name}-{alg2}-{alg1}") not in used_combos:
                        metric1 = df.loc[(df['dataset']==data) & (df['name']==alg1), 'metric_value'].item()
                        metric2 = df.loc[(df['dataset']==data) & (df['name']==alg2), 'metric_value'].item()
                        df_type = df.loc[(df['dataset']==data) & (df['name']==alg1), 'dataset_type'].item()

                        # it's necessary (for me) for creating seaborn plot
                        plot_df = pd.DataFrame(data={'name': [alg1, alg2], 'metric_value': [metric1, metric2]})
                        plot_df = plot_df.pivot(columns="name", values="metric_value")

                        # create comparison barplot
                        ax = sns.barplot(plot_df)

                        if df.loc[(df['dataset']==data) & (df['name']==alg1), 'eval_metric'].item() == 'accuracy':
                            # put a star on the winning bar (higher metric for accuracy)
                            if metric1 > metric2:
                                ax.plot(0, metric1/2, "*", markersize=50, color="yellow")
                                # adjust plot height
                                ax.set(ylim=(0, metric1+(metric1/5)))
                                # update score
                                if df_type=="binary":
                                    score[name1]['binary'] += 1
                                elif df_type=="multi":
                                    score[name1]['multi'] += 1
                                elif df_type=="reg":
                                    score[name1]['reg'] += 1

                            elif metric1 < metric2:
                                ax.plot(1, metric2/2, "*", markersize=50, color="yellow")
                                # adjust plot height
                                ax.set(ylim=(0, metric2+(metric2/5)))
                                # update score
                                if df_type=="binary":
                                    score[name2]['binary'] += 1
                                elif df_type=="multi":
                                    score[name2]['multi'] += 1
                                elif df_type=="reg":
                                    score[name2]['reg'] += 1
                            
                            else:
                                # adjust plot height in case of draw
                                ax.set(ylim=(0, metric1+(metric1/5)))

                        else:
                            # put a star on the winning bar (lower metric for rmse)
                            if metric1 < metric2:
                                ax.plot(0, metric1/2, "*", markersize=50, color="yellow")
                                # adjust plot height
                                ax.set(ylim=(0, metric2+(metric2/5)))
                                # update score
                                if df_type=="binary":
                                    score[name1]['binary'] += 1
                                elif df_type=="multi":
                                    score[name1]['multi'] += 1
                                elif df_type=="reg":
                                    score[name1]['reg'] += 1

                            elif metric1 > metric2:
                                ax.plot(1, metric2/2, "*", markersize=50, color="yellow")
                                # adjust plot height
                                ax.set(ylim=(0, metric1+(metric1/5)))
                                # update score
                                if df_type=="binary":
                                    score[name2]['binary'] += 1
                                elif df_type=="multi":
                                    score[name2]['multi'] += 1
                                elif df_type=="reg":
                                    score[name2]['reg'] += 1

                            else:
                                # adjust plot height in case of draw
                                ax.set(ylim=(0, metric1+(metric1/5)))

                        # set title and labels
                        plt.title(f"{data}")
                        ax.set(xlabel='', ylabel=df.loc[(df["dataset"]==data) & (df['name']==alg1), 'eval_metric'].to_numpy()[0])
                        for i in ax.containers:
                            ax.bar_label(i,)                           
                        
                        # create possible directions and save plots
                        if not os.path.exists(f"comparison_plots/{name1}-vs-{name2}"):
                            os.makedirs(f"comparison_plots/{name1}-vs-{name2}")
                        if not os.path.exists(f"C:/Users/Maciek/website-mljar/public/machine-learning/{name1}-vs-{name2}"):
                            os.makedirs(f"C:/Users/Maciek/website-mljar/public/machine-learning/{name1}-vs-{name2}")

                        plt.savefig(f'comparison_plots/{name1}-vs-{name2}/{data_name}_{name1}-vs-{name2}.png')
                        plt.savefig(f'C:/Users/Maciek/website-mljar/public/machine-learning/{name1}-vs-{name2}/{data_name}_{name1}-vs-{name2}.png')
                        plt.close()

                        # summarize the results and select the winning algorithm
                        score_sum1 = score[name1]['binary'] + score[name1]['multi'] + score[name1]['reg']
                        score_sum2 = score[name2]['binary'] + score[name2]['multi'] + score[name2]['reg']
                        if score_sum1 > score_sum2:
                            score["win"] = name1
                        elif score_sum1 < score_sum2:
                            score["win"] = name2
                        
                        # save score files
                        with open(f"comparison_plots/{name1}-vs-{name2}/score.json", "w") as outfile:
                            json.dump(score, outfile)
                        
                        with open(f"C:/Users/Maciek/website-mljar/public/machine-learning/{name1}-vs-{name2}/score.json", "w") as outfile:
                            json.dump(score, outfile)        

                        # append used comparison to used_combos
                        used_combos.append(f"{data_name}-{alg1}-{alg2}")
                        used_combos.append(f"{data_name}-{alg2}-{alg1}")

                        generate_md(f"C:/Users/Maciek/website-mljar/public/machine-learning/{name1}-vs-{name2}", f"machine-learning/{name1}-vs-{name2}", alg1, alg2)


def generate_md(path, rel_path, alg1, alg2):
    name1 = alg1.replace(" ", "-").lower()
    name2 = alg2.replace(" ", "-").lower()

    # load json files
    json_score = open(f"{path}/score.json", "r")
    json_resources = open(f"algorithms_info/algorithms_resources.json", "r")
    json_datasets = open(f"algorithms_info/datasets_info.json", "r")
    df = pd.read_csv("algorithms_info/algorithm_leaderboard.csv")

    score = json.load(json_score)
    resources = json.load(json_resources)
    datasets = json.load(json_datasets)

    # create markdown file
    md_file = open(f"C:/Users/Maciek/website-mljar/src/content/machine-learning/{name1}-vs-{name2}.md", "w")

    # create markdown content
    content = f'''---
title: "{alg1} vs {alg2}"
description: Comparison of {alg1} and {alg2} with examples on different datasets.
---

<section>
<div class="flex-col sm:flex-row hidden sm:flex bg-slate-50 rounded-lg">
<div class="basis-1/2 place-self-center">
<img src="/machine-learning/logo/{name1}_logo.png" class="not-prose w-96 mx-auto">
</div>
<div class="basis-1/2 place-self-center">
<img src="/machine-learning/logo/{name2}_logo.png" class="not-prose w-96 mx-auto">
</div>
</div>

<div class="flex flex-col sm:flex-row px-8">
<div class="basis-1/2 text-justify sm:mr-8 mb-8 sm:mb-0">
<img src="/machine-learning/logo/{name1}_logo.png" class="not-prose w-96 mx-auto sm:hidden bg-slate-50 rounded-lg">
<p>{resources[name1]["desc"]}</p>
<h2 class='mb-2'>References</h2>
<ul class='text-left'>
{resources[name1]["ref"]}
</ul>
<h2 class='mb-2'>License</h2>
<p>{resources[name1]["license"]}</p>
</div>

<div class="basis-1/2 text-justify sm:ml-8">
<img src="/machine-learning/logo/{name2}_logo.png" class="not-prose w-96 mx-auto sm:hidden bg-slate-50 rounded-lg">
<p>{resources[name2]["desc"]}</p>
<h2 class='mb-2'>References</h2>
<ul class='text-left'>
{resources[name2]["ref"]}
</ul>
<h2 class='mb-2'>License</h2>
<p>{resources[name2]["license"]}</p>
</div>
</div>

<hr>
<div class="flex flex-col sm:flex-row">
<div class="basis-1/2 text-center">
<h2 class="text-4xl mb-2 mt-2">Binary classification</h2>
<p class="text-2xl"><span class="text-[#0099cc]">{alg1}</span> <b>{score[name1]["binary"]}:{score[name2]["binary"]}</b> <span class="text-[#0099cc]">{alg2}</span></p>
<h2 class="text-4xl mb-2">Multiclass classification</h2>
<p class="text-2xl"><span class="text-[#0099cc]">{alg1}</span> <b>{score[name1]["multi"]}:{score[name2]["multi"]}</b> <span class="text-[#0099cc]">{alg2}</span></p>
<h2 class="text-4xl mb-2">Regression</h2>
<p class="text-2xl"><span class="text-[#0099cc]">{alg1}</span> <b>{score[name1]["reg"]}:{score[name2]["reg"]}</b> <span class="text-[#0099cc]">{alg2}</span></p>
</div>
<div class="basis-1/2 bg-slate-50 rounded-lg">
<img src="/machine-learning/logo/{score["win"]}_logo.png" class="not-prose w-72 mx-auto">
<img src='/machine-learning/compete.svg' class="not-prose w-64 mx-auto">
</div>
</div>
</section>

<hr>
'''
    types = ["Binary classification", "Multiclass classification", "Regression"]
    for type in types:
        content += f'''
<section>
<div class="w-full text-center text-3xl">
<h2>{type}</h2>
</div>
'''
        for plot in os.listdir(path):
            if (plot.endswith(".png")):
                dataset_name = os.path.relpath(plot).replace(f"_{name1}-vs-{name2}.png", "")
                metric1 = df.loc[(df['dataset']==dataset_name.capitalize()) & (df['name']==alg1), 'metric_value'].item()
                metric2 = df.loc[(df['dataset']==dataset_name.capitalize()) & (df['name']==alg2), 'metric_value'].item()
                if datasets[dataset_name]["type"] == type:
                    content += f'''
<div class="flex flex-col sm:flex-row">
<div class="basis-1/2 text-center">
<img src="/{rel_path}/{os.path.relpath(plot)}">
</div>
<div class="basis-1/2 text-center">
<h2 class="text-4xl mb-2 mt-2"><span class="text-[#0099cc]">{dataset_name.replace("_", " ").capitalize()}</span> dataset</h2>
<div class="mx-8 text-left">
<p><b>Metric:</b> {datasets[dataset_name]["metric"]}</p>
<p><b>{alg1}</b> {round(float(metric1),5):,} - vs - {round(float(metric2),5):,} <b>{alg2}</b></p>
<p classs="text-pretty">{datasets[dataset_name]["desc"]}</p>
<p><b>Category:</b> {datasets[dataset_name]["category"]}</p>
<p><b>Rows:</b> {datasets[dataset_name]["rows"]} <b>Columns:</b> {datasets[dataset_name]["cols"]}</p>
<p><b>Available at OpenML: </b><a href="{datasets[dataset_name]["link"]}" class="no-underline" target="_blank">{datasets[dataset_name]["link"]}</a></p>
</div>
</div>
</div>
<hr>
    '''
        content += '''</section>'''

    # save markdown content
    md_file.write(content)

    # close files to save resources
    json_score.close()
    json_resources.close()
    json_datasets.close()
    md_file.close()
    del df
    

generate_models()
# compare()




