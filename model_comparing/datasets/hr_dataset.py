import pandas as pd
from sklearn.model_selection import train_test_split

def get_data():
    name = "hr"
    dataset_type = "class"
    train = pd.read_csv("https://raw.githubusercontent.com/pplonski/datasets-for-start/master/employee_attrition/HR-Employee-Attrition-train.csv")
    test = pd.read_csv("https://raw.githubusercontent.com/pplonski/datasets-for-start/master/employee_attrition/HR-Employee-Attrition-test.csv")
    # split data
    # create X columns list and set y column
    x_cols = ["Age", "BusinessTravel", "DailyRate", "Department", "DistanceFromHome", "Education", "EducationField", "EmployeeCount", "EmployeeNumber", "EnvironmentSatisfaction", "Gender", "HourlyRate", "JobInvolvement", "JobLevel", "JobRole", "JobSatisfaction", "MaritalStatus", "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked", "Over18", "OverTime", "PercentSalaryHike", "PerformanceRating", "RelationshipSatisfaction", "StandardHours", "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager"]
    y_col = "Attrition"
    # set input matrix
    X_train = train[x_cols]
    # set target vector
    y_train = train[y_col]
    # set input matrix
    X_test = test[x_cols]
    # set target vector
    y_test = test[y_col]

    return name, X_train, X_test, y_train, y_test, dataset_type
