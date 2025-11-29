from fastapi import APIRouter
import json, os
from supabase_client import supabase
from pydantic import BaseModel

router = APIRouter(prefix="/results", tags=["Results"])

class EventRequest(BaseModel):
    user_name: str
    message: str
    sentiment: str

@router.get("/get_results")
def get_results():

    demo_path = "demo_data/demo_data_offline.json"

    if os.path.exists(demo_path):
        with open(demo_path) as f:
            return json.load(f)

    if supabase:
        try:
            res = supabase.table("verified_results").select("*").order("created_at", desc=True).limit(10).execute()
            return {"examples": res.data}
        except:
            return {"error": "Supabase query failed"}
    
    return {"error": "No data available"}

@router.post("/add_event")
def add_event(req: EventRequest):
    try:
        if supabase:
            supabase.table("events").insert({
                "user_name": req.user_name,
                "message": req.message,
                "sentiment": req.sentiment
            }).execute()
            return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

    return {"success": False, "message": "Supabase not configured"}

@router.get("/verified")
def get_verified_results():
    if supabase:
        try:
            res = supabase.table("verified_results").select("*").order("created_at", desc=True).limit(20).execute()
            return res.data
        except Exception as e:
            return {"error": str(e)}
    
    return {"error": "Supabase offline"}

@router.get("/events")
def get_events():
    if supabase:
        try:
            res = supabase.table("events").select("*").order("created_at", desc=True).limit(30).execute()
            return res.data
        except Exception as e:
            return {"error": str(e)}

    return {"error": "Supabase offline"}

@router.get("/claims")
def get_claims():
    if supabase:
        try:
            res = supabase.table("claims").select("*").order("created_at", desc=True).limit(30).execute()
            return res.data
        except Exception as e:
            return {"error": str(e)}

    return {"error": "Supabase offline"}
