from aiogram import Router

from .start import start_router
from .terms import terms_router
from .get_detail import detail_router

from middlewares import CheckUser

main_router_user = Router()

start_router.message.middleware(CheckUser())

main_router_user.include_routers(
    start_router,
    terms_router,
    detail_router
)