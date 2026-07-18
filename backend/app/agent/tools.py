# from langchain.tools import tool

# from app.database import SessionLocal
# from app.models import HCP, Interaction


# @tool
# def get_all_hcp():
#     """
#     Returns all Healthcare Professionals.
#     """

#     db = SessionLocal()

#     try:

#         hcp = db.query(HCP).all()

#         if not hcp:
#             return "No HCP found."

#         return "\n".join(
#             [
#                 f"{i.id}. {i.name} | {i.speciality} | {i.location}"
#                 for i in hcp
#             ]
#         )

#     finally:
#         db.close()


# @tool
# def get_hcp_by_location(location: str):
#     """
#     Returns doctors from a specific location.
#     """

#     db = SessionLocal()

#     try:

#         doctors = db.query(HCP).filter(
#             HCP.location.ilike(f"%{location}%")
#         ).all()

#         if not doctors:
#             return f"No doctors found in {location}"

#         return "\n".join(
#             [
#                 f"{d.name} - {d.speciality} - {d.hospital}"
#                 for d in doctors
#             ]
#         )

#     finally:
#         db.close()


# @tool
# def get_interactions(hcp_id: int):
#     """
#     Returns interaction history of one HCP.
#     """

#     db = SessionLocal()

#     try:

#         interactions = db.query(Interaction).filter(
#             Interaction.hcp_id == hcp_id
#         ).all()

#         if not interactions:
#             return "No interactions found."

#         return "\n".join(
#             [
#                 f"{i.interaction_date}: {i.summary}"
#                 for i in interactions
#             ]
#         )

#     finally:
#         db.close()


from datetime import datetime
from typing import Optional

from langchain_core.tools import tool

from app.database import SessionLocal
from app.models import HCP, Interaction


def parse_date(date_value: Optional[str]):
    """
    Converts YYYY-MM-DD string to date object.
    Returns None if date is empty or invalid.
    """
    if not date_value:
        return None

    try:
        return datetime.strptime(date_value, "%Y-%m-%d").date()
    except Exception:
        return None


@tool
def get_all_hcp() -> str:
    """
    Returns all Healthcare Professionals from the CRM database.
    """
    db = SessionLocal()

    try:
        hcps = db.query(HCP).all()

        if not hcps:
            return "No HCP found."

        return "\n".join(
            [
                f"ID: {hcp.id} | Name: {hcp.name} | Speciality: {hcp.speciality} | "
                f"Hospital: {hcp.hospital} | Location: {hcp.location}"
                for hcp in hcps
            ]
        )

    finally:
        db.close()


@tool
def search_hcp(query: str) -> str:
    """
    Search HCPs by name, speciality, hospital, or location.
    """
    db = SessionLocal()

    try:
        hcps = db.query(HCP).filter(
            (HCP.name.ilike(f"%{query}%")) |
            (HCP.speciality.ilike(f"%{query}%")) |
            (HCP.hospital.ilike(f"%{query}%")) |
            (HCP.location.ilike(f"%{query}%"))
        ).all()

        if not hcps:
            return f"No HCP found for query: {query}"

        return "\n".join(
            [
                f"ID: {hcp.id} | Name: {hcp.name} | Speciality: {hcp.speciality} | "
                f"Hospital: {hcp.hospital} | Location: {hcp.location}"
                for hcp in hcps
            ]
        )

    finally:
        db.close()


@tool
def get_interactions(hcp_id: int) -> str:
    """
    Returns interaction history for a specific HCP.
    """
    db = SessionLocal()

    try:
        interactions = db.query(Interaction).filter(
            Interaction.hcp_id == hcp_id
        ).order_by(Interaction.created_at.desc()).all()

        if not interactions:
            return "No interactions found for this HCP."

        return "\n".join(
            [
                f"Interaction ID: {interaction.id} | "
                f"Date: {interaction.interaction_date} | "
                f"Summary: {interaction.summary} | "
                f"Products Discussed: {interaction.products_discussed} | "
                f"Follow-up Date: {interaction.follow_up_date}"
                for interaction in interactions
            ]
        )

    finally:
        db.close()


@tool
def log_interaction(
    hcp_id: int,
    summary: str,
    products_discussed: str = "",
    interaction_date: str = "",
    follow_up_date: str = ""
) -> str:
    """
    Log a new HCP interaction.

    The AI assistant should extract useful information from the user's message,
    summarize the conversation, identify products discussed, and store follow-up date if available.

    Dates should be passed in YYYY-MM-DD format.
    """
    db = SessionLocal()

    try:
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()

        if not hcp:
            return "HCP not found. Please provide a valid HCP ID."

        interaction = Interaction(
            hcp_id=hcp_id,
            interaction_date=parse_date(interaction_date),
            summary=summary,
            products_discussed=products_discussed,
            follow_up_date=parse_date(follow_up_date)
        )

        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        return (
            f"Interaction logged successfully. "
            f"Interaction ID: {interaction.id}, HCP: {hcp.name}"
        )

    finally:
        db.close()


@tool
def edit_interaction(
    interaction_id: int,
    summary: str = "",
    products_discussed: str = "",
    interaction_date: str = "",
    follow_up_date: str = ""
) -> str:
    """
    Edit an existing HCP interaction.

    Allows modification of summary, products discussed, interaction date, and follow-up date.
    Dates should be passed in YYYY-MM-DD format.
    """
    db = SessionLocal()

    try:
        interaction = db.query(Interaction).filter(
            Interaction.id == interaction_id
        ).first()

        if not interaction:
            return "Interaction not found. Please provide a valid interaction ID."

        if summary:
            interaction.summary = summary

        if products_discussed:
            interaction.products_discussed = products_discussed

        if interaction_date:
            interaction.interaction_date = parse_date(interaction_date)

        if follow_up_date:
            interaction.follow_up_date = parse_date(follow_up_date)

        db.commit()

        return f"Interaction {interaction_id} updated successfully."

    finally:
        db.close()


@tool
def suggest_next_action(hcp_id: int) -> str:
    """
    Suggest the next best action for a field representative based on recent HCP interactions.
    """
    db = SessionLocal()

    try:
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()

        if not hcp:
            return "HCP not found. Please provide a valid HCP ID."

        interactions = db.query(Interaction).filter(
            Interaction.hcp_id == hcp_id
        ).order_by(Interaction.created_at.desc()).limit(3).all()

        if not interactions:
            return (
                f"No previous interactions found for {hcp.name}. "
                "Suggested next action: schedule an introductory meeting and capture the HCP's interests."
            )

        recent_context = " ".join(
            [
                interaction.summary or ""
                for interaction in interactions
            ]
        )

        products = ", ".join(
            [
                interaction.products_discussed or ""
                for interaction in interactions
                if interaction.products_discussed
            ]
        )

        return (
            f"Recent context for {hcp.name}: {recent_context}. "
            f"Products discussed: {products if products else 'Not clearly recorded'}. "
            "Suggested next action: follow up on pending questions, share relevant clinical/product material, "
            "and schedule the next visit."
        )

    finally:
        db.close()
