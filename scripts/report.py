import pandas as pd
import os
import logging
from datetime import datetime
import time

DATA_PATH = os.getenv("DATA_PATH", "data/sample_data.parquet")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

logging.basicConfig(filename="output/pipeline.log", level=logging.INFO)

start = time.time()

try:

    logging.info("Pipeline started")
    os.makedirs("output", exist_ok=True)

    logging.info("Loading data...")
    try:
        df = pd.read_parquet(DATA_PATH)
    except FileNotFoundError:
        logging.error("Data file not found")
        raise
    except Exception as e:
        logging.error(f"Error occurred while loading data: {e}")
        raise

    if len(df) < 100:
        logging.warning("Dataset too small, skipping report")
        exit()


    if (df["price"] < 0).any():
        raise ValueError("Negative price found in data")
    
    if not (df["qty"] > 0).any():
        raise ValueError("Invalid quantity found in data")

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
    summary.to_csv(f"output/report_{timestamp}.csv", index=False)
    summary.to_json(f"output/report_{timestamp}.json", orient="records")
    summary.to_parquet(f"output/report_{timestamp}.parquet")

    logging.info("Pipeline completed successfully")


except Exception as e:
    logging.error(f"Pipeline failed: {e}")
    raise

end = time.time()
logging.info(f"Execution time: {end - start:.2f} seconds")