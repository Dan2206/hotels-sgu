import asyncio
import logging
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from project.core.config import settings
from project.api import booking
from project.api import booking_client
from project.api import buyer
from project.api import client
from project.api import healthcheck
from project.api import hotel
from project.api import price
from project.api import price_service
from project.api import residence
from project.api import residence_client
from project.api import room
from project.api import room_type
from project.api import room_type_book
from project.api import service
from project.api import service_rendered
from project.api import user
from project.api import auth

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app_options = {}
    if settings.ENV.lower() == "prod":
        app_options = {
            "docs_url": None,
            "redoc_url": None,
        }
    if settings.LOG_LEVEL in ["DEBUG", "INFO"]:
        app_options["debug"] = True

    app = FastAPI(root_path=settings.ROOT_PATH, **app_options)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(healthcheck.router, prefix="/api/healthcheck", tags=["Healthcheck APIs"])
    app.include_router(client.router, prefix="/api/client", tags=["Clients APIs"])
    app.include_router(hotel.router, prefix="/api/hotel", tags=["Hotels APIs"])
    app.include_router(room.router, prefix="/api/room", tags=["Rooms APIs"])
    app.include_router(room_type_book.router, prefix="/api/room-type-book", tags=["Rooms Types Book APIs"])
    app.include_router(room_type.router, prefix="/api/room-type", tags=["Room Types APIs"])
    app.include_router(price.router, prefix="/api/price", tags=["Prices APIs"])
    app.include_router(buyer.router, prefix="/api/buyer", tags=["Buyers APIs"])
    app.include_router(booking.router, prefix="/api/booking", tags=["Bookings APIs"])
    app.include_router(booking_client.router, prefix="/api/booking-client", tags=["Booking Clients APIs"])
    app.include_router(residence.router, prefix="/api/residence", tags=["Residences APIs"])
    app.include_router(residence_client.router, prefix="/api/residence-client", tags=["Residence Clients APIs"])
    app.include_router(service.router, prefix="/api/service", tags=["Services APIs"])
    app.include_router(service_rendered.router, prefix="/api/service-rendered", tags=["Service Rendered APIs"])
    app.include_router(price_service.router, prefix="/api/price-service", tags=["Price Services APIs"])
    app.include_router(user.router, prefix="/api/user", tags=["Users APIs"])
    app.include_router(auth.router, tags=["Auth APIs"])

    return app


app = create_app()


async def run() -> None:
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    logger.debug(f"{settings.postgres_url}=")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
