import pandas as pd
import joblib
import os

from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score

MODEL_FILE = "clv_model_bundle.pkl"
Features_COLUMNS = ["Recency", "Frequency"]

if not os.path.exists(MODEL_FILE):
    # Read the dataset
    df = pd.read_excel("online_retail_II.xlsx")

    # Drop rows with missing values in the "Customer ID" column
    df.dropna(subset=["Customer ID"], inplace=True)

    # Convert "InvoiceDate" to datetime and "Customer ID" to integer
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Customer ID"] = df["Customer ID"].astype(int)

    # Filter out canceled transactions and invalid entries
    df = df[~df["Invoice"].astype(str).str.startswith("C", na=False)]
    df = df[df["Quantity"] > 0]
    df = df[df["Price"] > 0]

    # Calculate total amount for each transaction
    df["TotalAmount"] = df["Quantity"] * df["Price"]
    reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    # Create RFM features
    rfm = df.groupby("Customer ID").agg({
        "InvoiceDate": lambda x: (reference_date - x.max()).days,
        "Invoice": "nunique",
        "TotalAmount": "sum"
    }).reset_index()

    # Rename columns for clarity
    rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]


    # Prepare features and target variable for CLV prediction
    x = rfm[Features_COLUMNS]
    y = rfm["Monetary"]

    # Create CLV segments based on Monetary value
    rfm["clv_segment"] = pd.qcut(
        rfm["Monetary"],
        q=5,
        labels=False
    )

    # Stratified split to maintain the distribution of CLV segments in train and test sets
    from sklearn.model_selection import StratifiedShuffleSplit
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_idx, test_idx in split.split(x, rfm["clv_segment"]):
        x_train = x.iloc[train_idx]
        x_test = x.iloc[test_idx]

        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]
        x_test.to_excel("test_clv.xlsx", index=False)

    # Training an XGBoost regression model for CLV prediction
        final_clv_model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )

        final_clv_model.fit(x_train, y_train)
        xgb_predictions = final_clv_model.predict(x_test)

    # Dump the trained CLV model for future use
    joblib.dump(
        {
            "model": final_clv_model,
            "features": Features_COLUMNS
        },
        MODEL_FILE
    )
    print("CLV model trained and saved.")

# Inference phase for CLV prediction
else:
    bundle = joblib.load(MODEL_FILE)
    loaded_clv_model = bundle["model"]
    features = bundle["features"]
    test_clv_data = pd.read_excel("test_clv.xlsx")
    test_clv_features = test_clv_data[features]
    clv_predictions = loaded_clv_model.predict(test_clv_features)
    test_clv_data["CLV_Prediction"] = clv_predictions
    test_clv_data.to_excel("test_clv_with_predictions.xlsx", index=False)
    print("CLV predictions saved to test_clv_with_predictions.xlsx")



# Testing a variety of regression models to predict CLV and comparing their performance using MAE and R² metrics.

# Testing a simple linear regression model as a baseline for CLV prediction
# baseline_clv_model = LinearRegression()
# baseline_clv_model.fit(train_features, train_clv)
# baseline_prediction = baseline_clv_model.predict(test_features)

# baseline_mae = mean_absolute_error(test_clv, baseline_prediction)
# baseline_r2 = r2_score(test_clv, baseline_prediction)

# print("Baseline (Linear Regression) MAE:", baseline_mae)
# print("Baseline (Linear Regression) r2:", baseline_r2)


# # Testing a decision tree regression model for CLV prediction
# dt_clv_model = DecisionTreeRegressor()
# dt_clv_model.fit(train_features, train_clv)
# dt_prediction = dt_clv_model.predict(test_features)

# dt_mae = mean_absolute_error(test_clv, dt_prediction)
# dt_r2 = r2_score(test_clv, dt_prediction)

# print("Decision Tree Regression MAE:", dt_mae)
# print("Decision Tree Regression r2:", dt_r2)


# # Testing a random forest regression model for CLV prediction
# rf_clv_model = RandomForestRegressor()
# rf_clv_model.fit(train_features, train_clv)
# rf_prediction = rf_clv_model.predict(test_features)

# rf_mae = mean_absolute_error(test_clv, rf_prediction)
# rf_r2 = r2_score(test_clv, rf_prediction)

# print("Random Forest Regression MAE:", rf_mae)
# print("Random Forest Regression Regression r2:", rf_r2)


# # Testing a ridge regression model for CLV prediction
# ridge_clv_model = Ridge(alpha=1.0)

# ridge_clv_model.fit(train_features, train_clv)
# ridge_predictions = ridge_clv_model.predict(test_features)

# ridge_mae = mean_absolute_error(test_clv, ridge_predictions)
# ridge_r2 = r2_score(test_clv, ridge_predictions)

# print("Ridge MAE:", ridge_mae)
# print("Ridge R²:", ridge_r2)


# # Testing a lasso regression model for CLV prediction
# lasso_clv_model = Lasso(alpha=0.01, max_iter=5000)

# lasso_clv_model.fit(train_features, train_clv)
# lasso_predictions = lasso_clv_model.predict(test_features)

# lasso_mae = mean_absolute_error(test_clv, lasso_predictions)
# lasso_r2 = r2_score(test_clv, lasso_predictions)

# print("Lasso MAE:", lasso_mae)
# print("Lasso R²:", lasso_r2)


# # Testing an elastic net regression model for CLV prediction
# elastic_clv_model = ElasticNet(alpha=0.01, l1_ratio=0.5)

# elastic_clv_model.fit(train_features, train_clv)
# elastic_predictions = elastic_clv_model.predict(test_features)

# elastic_mae = mean_absolute_error(test_clv, elastic_predictions)
# elastic_r2 = r2_score(test_clv, elastic_predictions)

# print("ElasticNet MAE:", elastic_mae)
# print("ElasticNet R²:", elastic_r2)


# # Testing a gradient boosting regression model for CLV prediction
# gbr_clv_model = GradientBoostingRegressor(
#     n_estimators=200,
#     learning_rate=0.05,
#     random_state=42
# )

# gbr_clv_model.fit(train_features, train_clv)
# gbr_predictions = gbr_clv_model.predict(test_features)

# gbr_mae = mean_absolute_error(test_clv, gbr_predictions)
# gbr_r2 = r2_score(test_clv, gbr_predictions)

# print("Gradient Boosting MAE:", gbr_mae)
# print("Gradient Boosting R²:", gbr_r2)


# Testing an XGBoost regression model for CLV prediction
# xgb_clv_model = XGBRegressor(
#     n_estimators=300,
#     learning_rate=0.05,
#     max_depth=4,
#     random_state=42
# )

# xgb_clv_model.fit(train_features, train_clv)
# xgb_predictions = xgb_clv_model.predict(test_features)

# xgb_mae = mean_absolute_error(test_clv, xgb_predictions)
# xgb_r2 = r2_score(test_clv, xgb_predictions)

# print("XGBoost MAE:", xgb_mae)
# print("XGBoost R²:", xgb_r2)


# # Create a DataFrame to compare the performance of all models
# model_comparison = pd.DataFrame({
#     "Model": [
#         "Linear Regression",
#         "Ridge",
#         "Lasso",
#         "ElasticNet",
#         "Decision Tree",
#         "Random Forest",
#         "Gradient Boosting",
#         "XGBRegressor"
#     ],
#     "MAE": [
#         baseline_mae,
#         ridge_mae,
#         lasso_mae,
#         elastic_mae,
#         dt_mae,
#         rf_mae,
#         gbr_mae,
#         xgb_mae
#     ],
#     "R2": [
#         baseline_r2,
#         ridge_r2,
#         lasso_r2,
#         elastic_r2,
#         dt_r2,
#         rf_r2,
#         gbr_r2,
#         xgb_r2
#     ]
# })

# model_comparison.sort_values("MAE")

