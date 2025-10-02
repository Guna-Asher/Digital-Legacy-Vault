from sqlalchemy.orm import Session
from app.models.asset import DigitalAsset, Beneficiary
from app.schemas.asset import DigitalAssetCreate, DigitalAssetUpdate, BeneficiaryCreate

def get_asset(db: Session, asset_id: int):
    return db.query(DigitalAsset).filter(DigitalAsset.id == asset_id).first()

def get_user_assets(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(DigitalAsset).filter(DigitalAsset.owner_id == user_id).offset(skip).limit(limit).all()

def create_asset(db: Session, asset: DigitalAssetCreate, owner_id: int):
    db_asset = DigitalAsset(**asset.dict(), owner_id=owner_id)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def update_asset(db: Session, asset_id: int, asset_update: DigitalAssetUpdate):
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None
    
    update_data = asset_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asset, field, value)
    
    db.commit()
    db.refresh(db_asset)
    return db_asset

def add_beneficiary(db: Session, asset_id: int, beneficiary: BeneficiaryCreate):
    db_beneficiary = Beneficiary(**beneficiary.dict(), asset_id=asset_id)
    db.add(db_beneficiary)
    db.commit()
    db.refresh(db_beneficiary)
    return db_beneficiary

def get_asset_beneficiaries(db: Session, asset_id: int):
    return db.query(Beneficiary).filter(Beneficiary.asset_id == asset_id).all()