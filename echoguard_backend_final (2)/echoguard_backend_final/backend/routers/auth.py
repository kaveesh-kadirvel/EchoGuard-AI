# backend/routers/auth.py
from fastapi import APIRouter
from pydantic import BaseModel
from supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["Auth"])

class SignupRequest(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(req: SignupRequest):
    if supabase is None:
        return {"success": True, "message": "Demo: signup accepted."}
    try:
        res = supabase.auth.sign_up({
            "email": req.email,
            "password": req.password
        }, options={"data": {"full_name": req.full_name or ""}})
        # supabase returns a dict-like response
        if isinstance(res, dict) and res.get("user"):
            return {"success": True, "message": "Signup successful. Check email for confirmation."}
        return {"success": True, "message": "Signup request received (check email if configured)."}
    except Exception as e:
        return {"success": False, "message": str(e)}

@router.post("/login")
def login(req: LoginRequest):
    if supabase is None:
        return {"success": True, "message": "Demo: login accepted."}
    try:
        res = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })
        # handle different client return shapes
        if isinstance(res, dict) and res.get("data") and res["data"].get("user"):
            user = res["data"]["user"]
            return {"success": True, "message": "Login successful", "user": {"id": user.get("id"), "email": user.get("email")}}
        if getattr(res, "user", None):
            user = res.user
            return {"success": True, "message": "Login successful", "user": {"id": user.id, "email": user.email}}
        # fallback
        return {"success": False, "message": "Login failed"}
    except Exception as e:
        return {"success": False, "message": str(e)}
