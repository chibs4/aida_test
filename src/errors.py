from fastapi import HTTPException


def failed_to_generate():
    return HTTPException(detail="Failed to generate link", status_code=500)


def link_already_exists(long_url: str):
    return HTTPException(
        detail=f"Long link is already in DB: {long_url}", status_code=400
    )


def link_not_found(rel_url: str):
    return HTTPException(detail=f"Short link not found: {rel_url}", status_code=400)


def link_too_long():
    return HTTPException(detail="Max length of the link is 5", status_code=400)
