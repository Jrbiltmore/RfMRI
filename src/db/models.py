
# /RfMRI/src/db/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.db.database import Base
from datetime import datetime

class User(Base):
    """Model for the users who can access the MRI data analysis system."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    mri_analyses = relationship('MRIAnalysis', back_populates='user')

class MRIAnalysis(Base):
    """Model for MRI data analyses, linked to a User."""
    __tablename__ = 'mri_analyses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    result = Column(String(500))
    notes = Column(String(1000))

    # Relationships
    user = relationship('User', back_populates='mri_analyses')

class SessionLog(Base):
    """Model for tracking user sessions and activities within the system."""
    __tablename__ = 'session_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    login_time = Column(DateTime, default=datetime.utcnow)
    logout_time = Column(DateTime)
    session_duration = Column(Float)  # Duration in seconds

    user = relationship('User')
