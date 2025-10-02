from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import get_current_user, create_access_token, verify_password
from app.schemas.user import User, UserCreate, UserLogin, Token
from app.schemas.asset import DigitalAsset, DigitalAssetCreate, DigitalAssetUpdate, Beneficiary, BeneficiaryCreate, DigitalAssetWithBeneficiaries
from app.schemas.event import DeathVerification, DeathVerificationCreate, MultisigApproval, MultisigApprovalCreate, AssetTransfer
from app.crud import user as user_crud
from app.crud import asset as asset_crud
from app.crud import event as event_crud
from app.models.user import User as UserModel
from app.models.event import DeathVerificationEvent, AssetTransfer as AssetTransferModel

app = FastAPI(
    title="Digital Legacy Vault API",
    description="A secure system for managing digital assets and automating transfers to beneficiaries upon verified death",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication endpoints
@app.post("/auth/register", response_model=User, tags=["Authentication"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@app.post("/auth/login", response_model=Token, tags=["Authentication"])
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, email=user_data.email, password=user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.get("/users/me", response_model=User, tags=["Users"])
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

# Asset endpoints
@app.post("/assets", response_model=DigitalAsset, tags=["Assets"])
def create_asset(
    asset: DigitalAssetCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return asset_crud.create_asset(db=db, asset=asset, owner_id=current_user.id)

@app.get("/assets", response_model=List[DigitalAsset], tags=["Assets"])
def read_assets(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return asset_crud.get_user_assets(db, user_id=current_user.id, skip=skip, limit=limit)

@app.get("/assets/{asset_id}", response_model=DigitalAssetWithBeneficiaries, tags=["Assets"])
def read_asset(
    asset_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    asset = asset_crud.get_asset(db, asset_id=asset_id)
    if not asset or asset.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    beneficiaries = asset_crud.get_asset_beneficiaries(db, asset_id=asset_id)
    return DigitalAssetWithBeneficiaries(
        **asset.__dict__,
        beneficiaries=beneficiaries
    )

@app.post("/assets/{asset_id}/beneficiaries", response_model=Beneficiary, tags=["Assets"])
def add_asset_beneficiary(
    asset_id: int,
    beneficiary: BeneficiaryCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    asset = asset_crud.get_asset(db, asset_id=asset_id)
    if not asset or asset.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return asset_crud.add_beneficiary(db, asset_id=asset_id, beneficiary=beneficiary)

# Death verification endpoints
@app.post("/death-verifications", response_model=DeathVerification, tags=["Death Verification"])
def create_death_verification(
    event: DeathVerificationCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return event_crud.create_death_verification(db, event=event, initiated_by=current_user.id)

@app.post("/death-verifications/{event_id}/approvals", response_model=MultisigApproval, tags=["Death Verification"])
def add_death_verification_approval(
    event_id: int,
    approval: MultisigApprovalCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return event_crud.add_approval(db, event_id=event_id, approval=approval, approver_id=current_user.id)

@app.get("/death-verifications/{event_id}", response_model=DeathVerification, tags=["Death Verification"])
def get_death_verification(event_id: int, db: Session = Depends(get_db)):
    event = event_crud.get_death_verification(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Transfer endpoints
@app.get("/transfers", response_model=List[AssetTransfer], tags=["Transfers"])
def read_transfers(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(AssetTransferModel).filter(
        (AssetTransferModel.from_user_id == current_user.id) | 
        (AssetTransferModel.to_user_id == current_user.id)
    ).all()

# Demo endpoints for presentation
@app.get("/demo/users", tags=["Demo"])
def demo_get_users(db: Session = Depends(get_db)):
    """Returns all users for demo purposes."""
    return user_crud.get_users(db)

@app.get("/demo/death-verifications", tags=["Demo"])
def demo_get_death_verifications(db: Session = Depends(get_db)):
    """Returns all death verification events for demo purposes."""
    return db.query(DeathVerificationEvent).all()

@app.get("/demo/asset-transfers", tags=["Demo"])
def demo_get_asset_transfers(db: Session = Depends(get_db)):
    """Returns all asset transfers for demo purposes."""
    return db.query(AssetTransferModel).all()

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Digital Legacy Vault API",
        "version": "1.0.0",
        "docs": "/docs",
        "demo_script": "Run python demo_script.py to see the full workflow"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
