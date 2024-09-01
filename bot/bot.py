import asyncio
import logging

from aiogram import Bot, Dispatcher
from starlette.config import Config

config = Config(".env")

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

inlineWebAppButton = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Лучшее нажимать прямо на ссылку",
                          web_app=WebAppInfo(url=config("WEBAPP_FRONT_LINK")))]])

inlineLinkButton = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Birthday count TgMiniApp link", url=config("WEBAPP_PRETTY_LINK"))]])


@router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer('Что бы узнать как лучше открывать миниАпп: /help', reply_markup=inlineWebAppButton)


@router.message(Command('help'))
async def start_handler(message: Message):
    await message.answer('Лучше входить по ссылке, потому что через кнопки и инлайн кнопки \n'
                         'приложение может работать некорректно тк не передается инфа по пользователю',
                         reply_markup=inlineWebAppButton)


@router.message()
async def start_handler(message: Message):
    await message.answer('а вот как раз ссылка',
                         reply_markup=inlineLinkButton)


async def main():
    bot = Bot(token=config("TOKEN_BOT"))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
