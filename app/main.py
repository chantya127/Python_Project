from fastapi import FastAPI
from app.routes.items import router as items_router
from app.routes.clock_in import router as clockin_router

app = FastAPI()


# Register routers for different resources
app.include_router(items_router, prefix="/items", tags=["Items"])
app.include_router(clockin_router, prefix="/clock-in", tags=["Clock-In Records"])
