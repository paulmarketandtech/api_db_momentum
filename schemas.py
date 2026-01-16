from datetime import date as date_type

from pydantic import BaseModel, ConfigDict


class StockDataRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticker: str
    date: date_type
    close: float
    open: float
    high: float
    low: float


class YTDBestWorstRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date_type
    ticker: str
    pct_change: float
