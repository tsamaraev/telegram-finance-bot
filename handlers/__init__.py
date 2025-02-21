from aiogram import Router
from .user_handlers import router as user_router


router = Router()

router.include_router(user_router)
