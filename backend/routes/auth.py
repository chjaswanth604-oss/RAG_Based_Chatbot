import uuid
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from models.user import UserRegister, UserLogin, TokenResponse, UserResponse
from utils.security import hash_password, verify_password, create_access_token
from database.mongodb import get_db
from middleware.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    try:
        db = get_db()
        users_col = db.get_collection("users")

        clean_email = user_data.email.lower().strip()
        # Check duplicate email
        existing_user = await users_col.find_one({"email": clean_email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email address already exists."
            )

        user_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        hashed_pwd = hash_password(user_data.password)

        new_user = {
            "_id": user_id,
            "name": user_data.name.strip(),
            "email": clean_email,
            "password_hash": hashed_pwd,
            "role": user_data.role,
            "created_at": now_iso
        }

        await users_col.insert_one(new_user)

        token = create_access_token(data={"sub": user_id, "role": user_data.role})

        user_resp = UserResponse(
            id=user_id,
            name=new_user["name"],
            email=new_user["email"],
            role=new_user["role"],
            created_at=new_user["created_at"]
        )

        return TokenResponse(access_token=token, user=user_resp)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed due to a server error: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    try:
        db = get_db()
        users_col = db.get_collection("users")

        clean_email = credentials.email.lower().strip()
        user = await users_col.find_one({"email": clean_email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(credentials.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_access_token(data={"sub": user["_id"], "role": user["role"]})

        user_resp = UserResponse(
            id=user["_id"],
            name=user["name"],
            email=user["email"],
            role=user["role"],
            created_at=user.get("created_at", "")
        )

        return TokenResponse(access_token=token, user=user_resp)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed due to a server error: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=current_user["_id"],
        name=current_user["name"],
        email=current_user["email"],
        role=current_user["role"],
        created_at=current_user.get("created_at", "")
    )

