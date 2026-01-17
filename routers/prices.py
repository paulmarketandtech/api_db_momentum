from datetime import date as date_type
from typing import Union

from fastapi import APIRouter

from database import session
from models import StockData
from schemas import StockDataRead

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/{ticker}/{date}")
def read_root(ticker: str, date: date_type, ohcl: Union[str, None] = None):
    ticker = ticker.upper()
    result = (
        session.query(StockData)
        .filter(StockData.ticker == ticker, StockData.date == date)
        .first()
    )
    if result is None:
        return {"error": "Not found"}
    return StockDataRead.model_validate(result)
