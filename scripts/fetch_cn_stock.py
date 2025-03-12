from typing import Literal

import qlib
from qlib.data import D

from config import CN_FOLDER_DIR, LOGGER
from constants import QLIB_DATA_DIR


def fetch_cn_stock(market: Literal["csi300", "csi500"]) -> None:
    qlib.init(provider_uri=QLIB_DATA_DIR)
    instruments = D.instruments(market=market)
    stocks = D.list_instruments(
        instruments=instruments, start_time="2007-01-01", as_list=True
    )

    fields = ["$open", "$high", "$low", "$close", "$volume"]
    data = D.features(
        instruments,
        fields,
        start_time="2007-01-01",
        freq="day",
    )

    modified_columns = ["open", "high", "low", "close", "volume"]
    LOGGER.info("Starting to fetch cn stock data...")

    for stock in stocks:
        try:
            single_stock_data = data.loc[stock]
            single_stock_data.columns = modified_columns
            single_stock_data.reset_index(names=["date"], inplace=True)
            single_stock_data = single_stock_data[["date"] + modified_columns]

            single_stock_data.to_csv(f"{CN_FOLDER_DIR}/{stock}.csv", index=True)

        except Exception as e:
            print(f"stock {stock} got error {e}")

    LOGGER.info("CN stock data fetched successfully")
