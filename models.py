import os
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class GPUMetric(Base):
    __tablename__ = "gpu_metrics"
    time          = Column(DateTime(timezone=True), primary_key=True, default=datetime.utcnow)
    gpu_id        = Column(String, primary_key=True, nullable=False)
    node_id       = Column(String, nullable=False)
    power_watts   = Column(Float)
    gpu_util      = Column(Float)
    mem_util      = Column(Float)
    temp_c        = Column(Float)
    ghost_flag    = Column(Boolean, default=False)
    desync_flag   = Column(Boolean, default=False)
    cei_score     = Column(Float)
    mem_clock_mhz = Column(Integer)
    p_state       = Column(Integer)
    anomaly_score = Column(Float, default=0.0)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://optimizer:password@localhost/gpu_metrics")
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
