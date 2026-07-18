from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import HCP, Interaction
from app.schemas import (
    HCPCreate,
    HCPResponse,
    InteractionCreate,
    InteractionResponse
)

router = APIRouter()


@router.post("/hcp", response_model=HCPResponse)
def create_hcp(
    hcp: HCPCreate,
    db: Session = Depends(get_db)
):
    new_hcp = HCP(**hcp.model_dump())

    db.add(new_hcp)
    db.commit()
    db.refresh(new_hcp)

    return new_hcp


@router.get("/hcp", response_model=list[HCPResponse])
def get_all_hcp(
    db: Session = Depends(get_db)
):
    hcp_list = db.query(HCP).all()

    return hcp_list



@router.post("/interaction", response_model=InteractionResponse)
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):
    new_interaction = Interaction(
        **interaction.model_dump()
    )

    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return new_interaction



@router.get("/interaction/{hcp_id}", response_model=list[InteractionResponse])
def get_interactions(
    hcp_id: int,
    db: Session = Depends(get_db)
):
    interactions = db.query(Interaction).filter(
        Interaction.hcp_id == hcp_id
    ).all()

    return interactions



@router.put("/interaction/{id}", response_model=InteractionResponse)
def update_interaction(
    id: int,
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):
    existing_interaction = db.query(Interaction).filter(
        Interaction.id == id
    ).first()

    if not existing_interaction:
        return {"message": "Interaction not found"}

    existing_interaction.hcp_id = interaction.hcp_id
    existing_interaction.interaction_date = interaction.interaction_date
    existing_interaction.summary = interaction.summary
    existing_interaction.products_discussed = interaction.products_discussed
    existing_interaction.follow_up_date = interaction.follow_up_date

    db.commit()
    db.refresh(existing_interaction)

    return existing_interaction



from fastapi import HTTPException

@router.delete("/interaction/{id}")
def delete_interaction(
    id: int,
    db: Session = Depends(get_db)
):
    interaction = db.query(Interaction).filter(
        Interaction.id == id
    ).first()

    if not interaction:
        raise HTTPException(
            status_code=404,
            detail="Interaction not found"
        )

    db.delete(interaction)
    db.commit()

    return {"message": "Interaction deleted successfully"}