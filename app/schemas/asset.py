from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

class AssetType(str, Enum):
    CRYPTO_WALLET = "crypto_wallet"
    SOCIAL_MEDIA = "social_media"
    CLOUD_STORAGE = "cloud_storage"
    DOCUMENTS = "documents"
    OTHER = "other"

class DigitalAssetBase(BaseModel):
    asset_type: AssetType
    name: str
    description: Optional[str] = None
    access_instructions: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class DigitalAssetCreate(DigitalAssetBase):
    pass

class DigitalAssetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    access_instructions: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class DigitalAsset(DigitalAssetBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BeneficiaryBase(BaseModel):
    user_id: int
    share_percentage: float
    approval_required: bool = False

class BeneficiaryCreate(BeneficiaryBase):
    pass

class Beneficiary(BeneficiaryBase):
    id: int
    asset_id: int
    has_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class DigitalAssetWithBeneficiaries(DigitalAsset):
    beneficiaries: List[Beneficiary] = []

    class Config:
        from_attributes = True