from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import waste_types, devices, containers, users, alerts, routes, sensor_data, auth, analytics

app = FastAPI(
    title="SmartSort Backend",
    description="API for Smart Waste Management System",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(waste_types.router)
app.include_router(devices.router)
app.include_router(containers.router)
app.include_router(users.router)
app.include_router(alerts.router)
app.include_router(routes.router)
app.include_router(sensor_data.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"status": "Database connected, tables created, API ready"}
