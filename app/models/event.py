from sqlalchemy import Column, Integer, String, Enum, JSON, TIMESTAMP, ForeignKey, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class DeathVerificationEvent(Base):
    __tablename__ = "death_verification_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum('pending', 'verified', 'rejected', 'requires_more_evidence'), nullable=False)
    verification_type = Column(Enum('death_certificate', 'multiple_witnesses', 'legal_document'), nullable=False)
    evidence_data = Column(JSON)
    required_approvals = Column(Integer, default=1)
    current_approvals = Column(Integer, default=0)
    initiated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", foreign_keys=[user_id])
    initiator = relationship("User", foreign_keys=[initiated_by])
    approvals = relationship("MultisigApproval", back_populates="event")
    transfers = relationship("AssetTransfer", back_populates="death_event")

class MultisigApproval(Base):
    __tablename__ = "multisig_approvals"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("death_verification_events.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approval_status = Column(Enum('approved', 'rejected', 'pending'), default='pending')
    comments = Column(Text)
    approved_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())

    event = relationship("DeathVerificationEvent", back_populates="approvals")
    approver = relationship("User")

class AssetTransfer(Base):
    __tablename__ = "asset_transfers"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("digital_assets.id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transfer_date = Column(TIMESTAMP, server_default=func.now())
    transfer_status = Column(Enum('pending', 'completed', 'failed'), default='pending')
    death_event_id = Column(Integer, ForeignKey("death_verification_events.id"), nullable=False)
    metadata_ = Column("metadata", JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())

    asset = relationship("DigitalAsset")
    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])
    death_event = relationship("DeathVerificationEvent", back_populates="transfers")