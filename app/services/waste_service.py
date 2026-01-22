from sqlalchemy.orm import Session 
from app.models.container import Container 
from app.repositories import alert as alert_repo 
from app.schemas.alert import AlertCreate 

THRESHOLD_FILL_LEVEL=90 

def check_fill_level(db: Session, container_id: int, fill_level: int):
    if fill_level > THRESHOLD_FILL_LEVEL:
        alert_in = AlertCreate(
            container_id=container_id,
            message=f"Critical Fill Level: {fill_level}%"
        )
        return alert_repo.create_alert(db, alert_in)
    return None

def generate_optimization_route (db: Session):


    full_containers=db.query (Container).filter (Container.fill_level>50).all ()

    if not full_containers:
        return "No containers require collection."

    route_points=[]
    for c in full_containers:

        from app.models.device import Device 
        device=db.query (Device).filter (Device.id==c.device_id).first ()
        location=device.location if device else "Unknown"
        route_points.append (f"Container #{c.id } ({location }) - {c.fill_level }%")

    description="Optimized Route: "+" ->".join (route_points)
    return description 
