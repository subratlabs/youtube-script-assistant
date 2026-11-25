from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.script import SavedScript
from app.schemas.script import SavedScriptCreate, SavedScriptResponse


router = APIRouter(
    prefix="/api/saved-scripts",
    tags=["Saved Scripts"],
)


@router.post("/", response_model=SavedScriptResponse)
def save_script(
    script_data: SavedScriptCreate,
    db: Session = Depends(get_db),
):
    saved_script = SavedScript(
        topic=script_data.topic,
        title=script_data.title,
        content=script_data.content,
    )

    try:
        db.add(saved_script)
        db.commit()
        db.refresh(saved_script)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save the script right now. Please try again later.",
        )

    return saved_script


@router.get("/", response_model=list[SavedScriptResponse])
def list_saved_scripts(
    db: Session = Depends(get_db),
):
    try:
        return (
            db.query(SavedScript)
            .order_by(SavedScript.created_at.desc())
            .all()
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve saved scripts right now. Please try again later.",
        )


@router.get("/{script_id}", response_model=SavedScriptResponse)
def get_saved_script(
    script_id: int,
    db: Session = Depends(get_db),
):
    try:
        saved_script = (
            db.query(SavedScript)
            .filter(SavedScript.id == script_id)
            .first()
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve the saved script right now. Please try again later.",
        )

    if saved_script is None:
        raise HTTPException(
            status_code=404,
            detail="Saved script not found",
        )

    return saved_script


@router.delete("/{script_id}")
def delete_saved_script(
    script_id: int,
    db: Session = Depends(get_db),
):
    try:
        saved_script = (
            db.query(SavedScript)
            .filter(SavedScript.id == script_id)
            .first()
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve the saved script right now. Please try again later.",
        )

    if saved_script is None:
        raise HTTPException(
            status_code=404,
            detail="Saved script not found",
        )

    try:
        db.delete(saved_script)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to delete the saved script right now. Please try again later.",
        )

    return {
        "message": "Saved script deleted successfully",
        "id": script_id,
    }


@router.put("/{script_id}", response_model=SavedScriptResponse)
def update_saved_script(
    script_id: int,
    script_data: SavedScriptCreate,
    db: Session = Depends(get_db),
):
    try:
        saved_script = (
            db.query(SavedScript)
            .filter(SavedScript.id == script_id)
            .first()
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve the saved script right now. Please try again later.",
        )

    if saved_script is None:
        raise HTTPException(
            status_code=404,
            detail="Saved script not found",
        )

    try:
        saved_script.topic = script_data.topic
        saved_script.title = script_data.title
        saved_script.content = script_data.content

        db.commit()
        db.refresh(saved_script)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update the saved script right now. Please try again later.",
        )

    return saved_script