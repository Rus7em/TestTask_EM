from fastapi import APIRouter


router = APIRouter()


@router.post("/")
def add_products():
    pass

@router.get("/")
def get_product_list():
    pass

@router.get("/{id}")
def get_product():
    pass

@router.put("/{id}")
def edit_product():
    pass

@router.delete('/{id}')
def delete_product():
    pass
