from aiogram import Router

from .start import start_router
from .terms import terms_router
from .get_detail import detail_router
from .group import grorup_router
from .busket import busket_router
from .get_busket import get_busket_router

from middlewares import CheckUser, BusketIsEmpty

from filters import ChatTypeFilter

main_router_user = Router()

grorup_router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))
start_router.message.middleware(CheckUser())
get_busket_router.callback_query.middleware(BusketIsEmpty())
# start_router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))
main_router_user.include_routers(
    start_router,
    terms_router,
    detail_router,
    grorup_router,
    busket_router,
    get_busket_router
)
