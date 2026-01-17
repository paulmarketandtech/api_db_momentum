from datetime import date as date_type

from fastapi import APIRouter

from database import session
from models import YTD20Best, YTD20Worst
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
