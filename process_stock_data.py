import functools as ft

import pandas as pd
from scripts.config import LOGGER, OUTPUT_DIR
from tqdm import tqdm

from airflow.decorators import task


@task()
def process_and_save_stock_data(stock_data):
    try:
        LOGGER.info("Starting stock data preprocessing...")
        stock_ids = stock_data["volume"].columns.tolist()

        for idx, stock_id in tqdm(enumerate(stock_ids)):
            LOGGER.info(f"Processing {idx+1/len(stock_ids)}: {stock_id}")

            dfs = [stock_data[key][[stock_id]].rename(columns={stock_id: key}) for key in stock_data]
            df = ft.reduce(lambda left, right: pd.merge(left, right, on="date", how="outer"), dfs)
            df = df.dropna(how="all").fillna(method="ffill").fillna(method="bfill")
            df["stock_id"] = stock_id

            output_path = f"{OUTPUT_DIR}/{stock_id}.csv"
            df.to_csv(output_path, index=True)
            LOGGER.info(f"Saved {stock_id} data to {output_path}")

        LOGGER.info("Stock data preprocessing completed successfully")

    except Exception as e:
        LOGGER.error(f"Error preprocessing stock data: {str(e)}", exc_info=True)
        raise
