import fastapi_swagger_dark as fsd
from fastapi import APIRouter, FastAPI

from routers import meta_data, prices, returns

app = FastAPI(docs_url=None)
router = APIRouter()

fsd.install(router)
app.include_router(router)
app.include_router(returns.router)
app.include_router(prices.router)
app.include_router(meta_data.router)
