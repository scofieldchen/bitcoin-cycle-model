import datetime as dt
from pathlib import Path

from rich.console import Console

from src.downloader.alternative import download_fear_greed_index
from src.downloader.bgeometrics import download_blockchain_metrics
from src.downloader.binance_funding import download_funding_rate
from src.downloader.binance_lsr import download_lsr
from src.downloader.yahoo_finance import download_ohlcv

console = Console()


def main() -> None:
    # 参数
    data_directory = Path("./data")

    # 创建数据目录
    data_directory.mkdir(parents=True, exist_ok=True)

    # 最新日期
    end_date = dt.datetime.now(tz=dt.timezone.utc)

    # 下载数据
    download_ohlcv(
        filepath=data_directory / "btcusd.csv",
        symbol="BTC-USD",
        start_date=dt.datetime(2014, 1, 1, tzinfo=dt.timezone.utc),
        end_date=end_date,
    )

    download_blockchain_metrics(
        data_directory,
        metric_names=[
            "sth_realized_price",
            "sth_sopr",
            "sth_nupl",
            "sth_mvrv",
            "nrpl",
            "rhodl",
        ],
    )

    download_fear_greed_index(data_directory / "fear_greed_index.csv")

    download_lsr(data_directory, "BTCUSDT")

    download_funding_rate(
        filepath=data_directory / "funding_rate.csv",
        symbol="BTCUSDT",
        start_date=dt.datetime(2019, 1, 1, tzinfo=dt.timezone.utc),
        end_date=end_date,
    )


if __name__ == "__main__":
    main()
