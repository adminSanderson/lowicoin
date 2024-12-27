from aiogram import types, Router, Dispatcher

router = Router()

@router.message()
async def echo(message: types.Message):
    await message.answer(message.text)

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
