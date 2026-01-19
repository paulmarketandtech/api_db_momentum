from datetime import date as date_type
from typing import Literal

from fastapi import APIRouter
from sqlalchemy import asc, desc, select

from database import session
from models import StockData, YTD20Best, YTD20Worst
from schemas import YTDBestWorstRead

router = APIRouter(prefix="/returns", tags=["returns"])


@router.get("/ytd-best/{date}")
def get_ytd_best(date: date_type):
    results = session.query(YTD20Best).filter(YTD20Best.date == date).all()
    return [YTDBestWorstRead.model_validate(r) for r in results]


@router.get("/ytd-worst/{date}")
def get_ytd_worst(date: date_type):
    results = session.query(YTD20Worst).filter(YTD20Worst.date == date).all()
    return [YTDBestWorstRead.model_validate(r) for r in results]


@router.get("/period/{start_date}/{end_date}/{limit}/{order_direction}")
def get_top_stocks_by_period_change(
    start_date: date_type,
    end_date: date_type,
    limit: int,
    order_direction: Literal["best", "worst"] = "best",
):
    """
    Returns top/bottom N stocks by % change between close price on start_date
    and close price on end_date.
    Only includes tickers that have data on BOTH dates.
    """
    # Subquery for start price
    start_prices = (
        select(StockData.ticker, StockData.close.label("start_close"))
        .where(StockData.date == start_date)
        .subquery()
    )

    # Subquery for end price
    end_prices = (
        select(StockData.ticker, StockData.close.label("end_close"))
        .where(StockData.date == end_date)
        .subquery()
    )

    # Main query - inner join both dates
    stmt = (
        select(
            start_prices.c.ticker,
            start_prices.c.start_close,
            end_prices.c.end_close,
            ((end_prices.c.end_close / start_prices.c.start_close - 1) * 100).label(
                "pct_change"
            ),
        )
        .select_from(start_prices)
        .join(end_prices, start_prices.c.ticker == end_prices.c.ticker)
    )

    # Apply ordering
    if order_direction.lower() == "best":
        stmt = stmt.order_by(desc("pct_change"))
    else:
        stmt = stmt.order_by("pct_change")  # asc is default

    # Limit & execute
    results = session.execute(stmt.limit(limit)).all()

    # Nicer output format
    return [
        {
            "ticker": row.ticker,
            "start_date": start_date,
            "start_close": (
                round(float(row.start_close), 4) if row.start_close else None
            ),
            "end_date": end_date,
            "end_close": round(float(row.end_close), 4) if row.end_close else None,
            "pct_change": (
                round(float(row.pct_change), 2) if row.pct_change is not None else None
            ),
        }
        for row in results
    ]
