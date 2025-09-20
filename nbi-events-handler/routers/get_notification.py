from fastapi import APIRouter
from mongodb.initializer import query_utils, mongo_nwdaf_collection


router = APIRouter()

@router.post("/notification")
def get_notification(request: dict):

    if request and request["event"]:
        query_utils.insert_data(
            collection=mongo_nwdaf_collection,
            data=request)
