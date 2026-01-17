from sqlalchemy import Boolean, Column, Date, Float, Integer, String, UniqueConstraint

from database import Base


class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    ytd = Column(Float, nullable=True)
    weekly_change = Column(Float, nullable=True)
    ma50 = Column(Float, nullable=True)
    ma50_above = Column(Boolean, nullable=True)
    ma100 = Column(Float, nullable=True)
    ma100_above = Column(Boolean, nullable=True)
    ma200 = Column(Float, nullable=True)
    ma200_above = Column(Boolean, nullable=True)
    previous_correction = Column(Float, nullable=True)
    last_correction = Column(Float, nullable=True)
    weekly_change = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint("ticker", "date", name="unique_ticker_date"),)


class YTD20Best(Base):
    __tablename__ = "ytd_best"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    pct_change = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint("ticker", "date"),)


class YTD20Worst(Base):
    __tablename__ = "ytd_worst"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    pct_change = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint("ticker", "date"),)
