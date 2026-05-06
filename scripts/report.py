import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Pipeline started")

try:
    os.makedirs("output", exist_ok=True)

    logging.info("Loading data...")
    try:
        df = pd.read_parquet("data/sample_data.parquet")
    except FileNotFoundError:
        logging.error("Data file not found")
        raise
    except Exception as e:
        logging.error(f"Error occurred while loading data: {e}")
        raise

    logging.info("Processing data...")
    df["revenue"] = df["price"] * df["qty"]
    df["transaction_count"] = 1

# Compute summary
    summary = df.groupby("category").agg(
        total_revenue=("revenue", "sum"),
        total_quantity=("qty", "sum"),
        avg_price=("price", "mean"),
        transaction_count=("transaction_count", "sum")
    ).reset_index()

    logging.info("Saving report...")
    summary.to_csv("output/report.csv", index=False)

    logging.info("Pipeline completed successfully")


except Exception as e:
    logging.error(f"Pipeline failed: {e}")
    raise