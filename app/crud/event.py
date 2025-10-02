from sqlalchemy.orm import Session
from app.models.event import DeathVerificationEvent, MultisigApproval, AssetTransfer
from app.models.asset import DigitalAsset, Beneficiary
from app.schemas.event import DeathVerificationCreate, MultisigApprovalCreate

def create_death_verification(db: Session, event: DeathVerificationCreate, initiated_by: int):
    db_event = DeathVerificationEvent(
        **event.dict(),
        initiated_by=initiated_by,
        status="pending"
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_death_verification(db: Session, event_id: int):
    return db.query(DeathVerificationEvent).filter(DeathVerificationEvent.id == event_id).first()

def add_approval(db: Session, event_id: int, approval: MultisigApprovalCreate, approver_id: int):
    db_approval = MultisigApproval(
        **approval.dict(),
        event_id=event_id,
        approver_id=approver_id
    )
    db.add(db_approval)
    db.commit()
    db.refresh(db_approval)
    
    # Update approval count
    event = get_death_verification(db, event_id)
    if approval.approval_status == "approved":
        event.current_approvals += 1
        
        # Check if enough approvals for verification
        if event.current_approvals >= event.required_approvals:
            event.status = "verified"
            # Trigger asset transfer
            trigger_asset_transfer(db, event_id)
    
    db.commit()
    return db_approval

def trigger_asset_transfer(db: Session, event_id: int):
    event = get_death_verification(db, event_id)
    if event.status != "verified":
        return
    
    # Get all assets of the deceased user
    assets = db.query(DigitalAsset).filter(DigitalAsset.owner_id == event.user_id).all()
    
    for asset in assets:
        beneficiaries = db.query(Beneficiary).filter(Beneficiary.asset_id == asset.id).all()
        
        for beneficiary in beneficiaries:
            transfer = AssetTransfer(
                asset_id=asset.id,
                from_user_id=event.user_id,
                to_user_id=beneficiary.user_id,
                death_event_id=event_id,
                transfer_status="pending",
                metadata={
                    "share_percentage": float(beneficiary.share_percentage),
                    "asset_type": asset.asset_type
                }
            )
            db.add(transfer)
    
    db.commit()