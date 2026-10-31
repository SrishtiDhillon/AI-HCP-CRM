"""Add one fictional demo HCP to the configured database without deleting records."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from app.database import Base, engine, SessionLocal
from app.models import HCP
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    hcp = db.query(HCP).filter(HCP.email == 'demo@example.com').first()
    if hcp is None:
        hcp = HCP(name='Dr Demo', speciality='Fictional specialty', hospital='Example Hospital',
                  location='Demo City', email='demo@example.com', phone='0000000000')
        db.add(hcp)
        db.commit()
        db.refresh(hcp)
    print(f'Fictional demo HCP ready: ID {hcp.id}. Use this ID in the form.')
