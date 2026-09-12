from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
)

from app.core.oauth import oauth
from app.core.security import (
    create_access_token,
    create_refresh_token,
)
from app.crud.users import (
    create_user,
    get_user_by_email,
)
from app.db.database import get_db
from app.schemas.users import UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["OAuth"],
)


def generate_tokens(user):
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


def get_or_create_user(
    db: Session,
    email: str,
    name: str,
):
    user = get_user_by_email(db, email)

    if user is None:
        random_password = secrets.token_urlsafe(32)
        hashed_password = hash_password(random_password)

        user_data = UserCreate(
            name=name,
            email=email,
            password=random_password,
        )

        user = create_user(
            db,
            user_data,
            hashed_password=hashed_password,
        )

    return user


# ---------------- GOOGLE ----------------

@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    email = user_info["email"]
    name = user_info.get("name") or email.split("@")[0]

    user = get_or_create_user(db, email, name)

    return {
        "message": "Google OAuth successful",
        **generate_tokens(user),
    }


# ---------------- GITHUB ----------------

@router.get("/github/login")
async def github_login(request: Request):
    redirect_uri = request.url_for("github_callback")

    return await oauth.github.authorize_redirect(
        request,
        redirect_uri,
    )


@router.get("/github/callback")
async def github_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    token = await oauth.github.authorize_access_token(request)

    profile_response = await oauth.github.get(
        "user",
        token=token,
    )
    profile = profile_response.json()

    email = profile.get("email")

    # GitHub may hide the email in the main profile.
    if not email:
        emails_response = await oauth.github.get(
            "user/emails",
            token=token,
        )
        emails = emails_response.json()

        primary_email = next(
            (
                item
                for item in emails
                if item.get("primary") and item.get("verified")
            ),
            None,
        )

        if primary_email is None:
            raise HTTPException(
                status_code=400,
                detail="GitHub account has no verified email",
            )

        email = primary_email["email"]

    name = (
        profile.get("name")
        or profile.get("login")
        or email.split("@")[0]
    )

    user = get_or_create_user(db, email, name)

    return {
        "message": "GitHub OAuth successful",
        **generate_tokens(user),
    }