from fastapi import APIRouter



router = APIRouter()

@router.post("/")
def add_order():
    pass

@router.get("/")
def get_order_list():
    pass

@router.get("/{id}")
def get_order():
    pass

@router.patch("/{id}/status")
def set_order_status():
    pass
