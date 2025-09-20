from fastapi import FastAPI
from routers import get_metrics, get_notification
from fastapi.middleware.cors import CORSMiddleware
from events_utils.events_handler import EventsHandler


events_handler = EventsHandler()

fastapi_application = FastAPI()
fastapi_application.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"])

fastapi_application.include_router(get_metrics.router)
fastapi_application.include_router(get_notification.router)

@fastapi_application.on_event("startup")
async def startup_event():
    events_handler.send_events_subscription()
