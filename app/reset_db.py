from app.database import engine 
from app.models import Base 


from app.models.user import User 
from app.models.container import Container 
from app.models.device import Device 
from app.models.waste_type import WasteType 
from app.models.alert import Alert 
from app.models.route import Route 
from app.models.sensor_data import SensorData 

print ("Dropping all tables...")
Base.metadata.drop_all (bind=engine)
print ("Tables dropped.Please restart the server to recreate them.")
