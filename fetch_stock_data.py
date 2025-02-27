from typing import Dict, Optional

import finlab
import pandas as pd
from finlab import data
from scripts.config import LOGGER

from airflow.decorators import task


@task()
def fetch_stock_data() -> Optional[Dict[str, pd.DataFrame]]:
    try:
        LOGGER.info("Fetching stock data...")
        finlab.login("dePgtQJeiMDnpsXPL6PVbLosfcgiY9dIuPf/ZMlnMWKSSpoYpaMUzHDq6l/qVbOz#vip_m")
        stock_data = {
            "volume": data.get("price:成交股數"),
            "count": data.get("price:成交筆數"),
            "value": data.get("price:成交金額"),
            "close": data.get("price:收盤價"),
            "open": data.get("price:開盤價"),
            "high": data.get("price:最高價"),
            "low": data.get("price:最低價"),
            "adj_close": data.get("etl:adj_close"),
        }

        LOGGER.info("stock data fetched successfully")

        return stock_data

    except Exception as e:
        LOGGER.error(f"Error fetching stock data: {str(e)}", exc_info=True)
        raise
