from datetime import date as date_type

from fastapi import APIRouter

from database import session
from models import StockData

router = APIRouter(prefix="/meta_data", tags=["meta_data"])


@router.get("/health")
def check_health():
    return {"status": "ok"}


@router.get("/tickers_number/{date}")
def no_of_tickers(date: date_type):
    result_stock_data = session.query(StockData).filter(StockData.date == date).all()
    return len(result_stock_data)
