from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

class VerificationStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    REQUIRES_MORE_EVIDENCE = "requires_more_evidence"

class VerificationType(str, Enum):
    DEATH_CERTIFICATE = "death_certificate"
    MULTIPLE_WITNESSES = "multiple_witnesses"
    LEGAL_DOCUMENT = "legal_document"

class ApprovalStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"

class DeathVerificationBase(BaseModel):
    verification_type: VerificationType
    evidence_data: Dict[str, Any]
    required_approvals: int = 1

class DeathVerificationCreate(DeathVerificationBase):
    user_id: int

class DeathVerification(DeathVerificationBase):
    id: int
    user_id: int
    status: VerificationStatus
    current_approvals: int
    initiated_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MultisigApprovalBase(BaseModel):
    comments: Optional[str] = None

class MultisigApprovalCreate(MultisigApprovalBase):
    approval_status: ApprovalStatus

class MultisigApproval(MultisigApprovalBase):
    id: int
    event_id: int
    approver_id: int
    approval_status: ApprovalStatus
    approved_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class AssetTransferBase(BaseModel):
    metadata: Optional[Dict[str, Any]] = None

class AssetTransfer(AssetTransferBase):
    id: int
    asset_id: int
    from_user_id: int
    to_user_id: int
    transfer_date: datetime
    transfer_status: str
    death_event_id: int
    created_at: datetime

    class Config:
        from_attributes = True