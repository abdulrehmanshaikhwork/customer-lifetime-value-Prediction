import pandas as pd
import joblib
import os

from sklearn.model_selection import StratifiedShuffleSplit
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