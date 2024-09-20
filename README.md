<h2 align="center">Check for yourself: <a href="https://mljar.com/machine-learning/" target="_blank">mljar.com/machine-learning</a></h2>

## Table of Contents

 - [First look](https://github.com/maciekmalachowski/Machine-learning-algorithm-comparison#first-look)
 - [Features](https://github.com/maciekmalachowski/Machine-learning-algorithm-comparison#features)
 - [Technologies and Libraries Used](https://github.com/maciekmalachowski/Machine-learning-algorithm-comparison#technologies)
 - [Usage](https://github.com/maciekmalachowski/Machine-learning-algorithm-comparison#usage)

<br>
 
<h1 align="center" id="first-look"> First look 👀 </h1>

#### This project is designed to automate the comparison of various machine learning algorithms on multiple datasets. 
#### It leverages the <a href="https://github.com/mljar/mljar-supervised" target="_blank">mljar-supervised</a> AutoML library to build models and compares their performance on both classification and regression tasks. 
#### The project enables automated model training, evaluation, leaderboard creation, and the generation of comparison plots between different algorithms.

<br>

<h1 align="center" id="features">Features ℹ</h1>

### 1. Dataset Fetching:
- The project uses the `fetch_openml` function from sklearn.datasets to download various datasets from `OpenML`.
- Datasets are categorized into three types: regression, binary classification, and multiclass classification, with `RMSE` used as the evaluation metric for regression tasks and `accuracy` used for both binary and multiclass classification tasks.
  
### 2. Model Generation:
- The `generate_models()` function automates the training of different algorithms (
            Baseline,
            Linear,
            CatBoost,
            Decision Tree,
            Extra Trees,
            LightGBM,
            Neural Network,
            Random Forest,
            Xgboost) across a variety of datasets.
- All models were trained with advanced feature engineering disabled and without ensembling. A 5-fold cross-validation with shuffle and stratification (for classification tasks) was applied. During training, various hyperparameter configurations (where applicable) were explored for each algorithm.
- Results of the best-performing models are logged in a leaderboard and saved to a CSV file.

### 3. Leaderboard:
- The project generates a leaderboard that tracks the performance of each algorithm on each dataset. Metrics like accuracy or RMSE are used, depending on the type of task (classification or regression).

### 4. Algorithm Comparison:
- The `compare()` function reads the leaderboard data and performs pairwise comparisons between algorithms across datasets.
- The comparison between algorithms is based on a scoring system that evaluates performance across binary classification, multiclass classification, and regression tasks. Scores are assigned for each category, and the algorithm with the highest overall score is declared the winner.
- The comparison results are saved as JSON files and plots for further analysis.

### 5. Report Generation:
- A Markdown file is generated for each algorithm comparison, including details on the datasets used, the metrics, and the winning algorithm. This makes it easy to publish the results in a user-friendly format for documentation or presentation.

<br>

<h1 align="center" id="technologies">Technologies and Libraries Used ⚙️</h1>

- `Python`: Core programming language used for scripting.
- `Scikit-learn`: Used for fetching datasets.
- `Mljar-supervised`: A Python package for AutoML, used to automate machine learning processes.
- `Pandas`: For handling and manipulating the leaderboard data.
- `Seaborn`: For generating comparison plots.
- `Matplotlib`: Used in conjunction with Seaborn for visualizations.
- `JSON`: For saving comparison scores and metadata in a structured format.
- `OS`: For directory management and file operations.

<br>

<h1 align="center" id="usage">Usage 🎈</h1>

Clone this repository and ensure you have the necessary dependencies installed. Run the `generate_models()` function to start training models on various datasets. Use `compare()` to generate comparisons between the algorithms and visualize the results.

This project is perfect for anyone looking to automate machine learning model comparison or experiment with various algorithms across different datasets.
