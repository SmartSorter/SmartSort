from sqlalchemy.orm import Session 
from app.models.route import Route 
from app.schemas.route import RouteCreate 

def get_route (db: Session, route_id: int):
    return db.query (Route).filter (Route.id==route_id).first ()

def get_routes (db: Session, skip: int=0, limit: int=100):
    return db.query (Route).offset (skip).limit (limit).all ()

def create_route (db: Session, route: RouteCreate):
    db_route=Route (description=route.description)
    db.add (db_route)
    db.commit ()
    db.refresh (db_route)
    return db_route 
