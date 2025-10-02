from sqlalchemy import Column, Integer, String, Text, Boolean, Enum, JSON, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class DigitalAsset(Base):
    __tablename__ = "digital_assets"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_type = Column(Enum('crypto_wallet', 'social_media', 'cloud_storage', 'documents', 'other'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    access_instructions = Column(JSON)
    metadata_ = Column("metadata", JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    owner = relationship("User")
    beneficiaries = relationship("Beneficiary", back_populates="asset")

class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("digital_assets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    share_percentage = Column(DECIMAL(5, 2), nullable=False)
    approval_required = Column(Boolean, default=False)
    has_approved = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    asset = relationship("DigitalAsset", back_populates="beneficiaries")
    user = relationship("User")