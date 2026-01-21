from sqlalchemy.orm import Session 
from app.models.container import Container 
from app.schemas.container import ContainerCreate, ContainerUpdate 

def get_container (db: Session, container_id: int):
    return db.query (Container).filter (Container.id==container_id).first ()

def get_containers (db: Session, skip: int=0, limit: int=100):
    return db.query (Container).offset (skip).limit (limit).all ()

def create_container (db: Session, container: ContainerCreate):
    db_container=Container (device_id=container.device_id,
    waste_type_id=container.waste_type_id,
    fill_level=container.fill_level)
    db.add (db_container)
    db.commit ()
    db.refresh (db_container)
    return db_container 

def update_container_fill_level (db: Session, container_id: int, fill_level: int):
    db_container=get_container (db, container_id)
    if not db_container:
        return None 

    db_container.fill_level=fill_level 
    db.add (db_container)
    db.commit ()
    db.refresh (db_container)
    return db_container 
