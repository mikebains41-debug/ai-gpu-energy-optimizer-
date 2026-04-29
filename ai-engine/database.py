# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.
# Contact: Mikebains41@gmail.com
# Unauthorized use prohibited.

from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class GPUMetric(Base):
    __tablename__ = "gpu_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    cluster = Column(String)
    gpu_index = Column(Integer)
    power_draw = Column(Float)
    power_limit = Column(Float)
    temperature = Column(Float)
    memory_used = Column(Float)
    memory_total = Column(Float)
    gpu_util = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
