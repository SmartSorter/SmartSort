from sqlalchemy.orm import Session 
from sqlalchemy import func 
from datetime import datetime, timedelta 
from app.models.container import Container 
from app.models.waste_type import WasteType 
from app.models.device import Device 
from app.models.alert import Alert 
from app.repositories import alert as alert_repo 

def get_waste_stats (db: Session):


    stats=db.query (WasteType.name,
    func.count (Container.id).label ("container_count"),
    func.avg (Container.fill_level).label ("avg_fill")).join (Container).group_by (WasteType.name).all ()

    return [{"waste_type": s [0], "count": s [1], "avg_fill": round (s [2], 2)}for s in stats]

def check_device_health (db: Session):



    inactive_devices=db.query (Device).filter (Device.is_active==False).all ()

    generated_alerts=[]
    for device in inactive_devices:



        container=db.query (Container).filter (Container.device_id==device.id).first ()
        if container:
            alert=alert_repo.create_alert (db, alert_repo.AlertCreate (container_id=container.id,
            message=f"Device {device.serial_number } is Offline/Inactive"))
            generated_alerts.append (alert)

    return generated_alerts 
