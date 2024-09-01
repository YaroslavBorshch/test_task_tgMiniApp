from asyncio import sleep

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import json
# from ..bot import bot, dp
from aiogram.types import Update
from starlette.config import Config
from tortoise import Tortoise

from schemas.methods_data import LoginRequest, UserLoadRequest, BasedResponse, ChangeLinkRequest

from db.models.user import User
from db.setup import init_db

import random
import string

app = FastAPI()
config = Config(".env")

async def startup_event():
    await init_db(app)


async def shutdown_event():
    await Tortoise.close_connections()


def parse_tg_object(tg_info: str):
    try:
        dict_info = json.loads(tg_info)
    except:
        return False
    if 'initData' in dict_info:
        dict_info = dict_info['initData']
    else:
        return False

    if 'user' in dict_info:
        name = ''
        surname = ''
        try:
            username = dict_info['user']['username']
        except:
            username = ''
        try:
            name = dict_info['user']['firstName']
        except:
            name = ''
        try:
            surname = dict_info['user']['secondName']
        except: surname = ''

        return {
            'username': username,
            'name': name,
            'surname': surname,
            'tg_id': dict_info['user']['id']
        }
    return False


app.add_event_handler("startup", startup_event)
app.add_event_handler('shutdown', shutdown_event)

origins = [
    config("WEBAPP_FRONT_LINK"),  # 5173
    config("WEBAPP_BACK_LINK")    # 8000
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_user_difference(user: User, fields: dict) -> User | None:
    """
    Обновляет поля экземпляра User, если они отличаются от значений в словаре fields.

    Returns: Обновленный экземпляр модели User.
    """
    haveChanges = False
    for field_name, field_value in fields.items():
        # Пропускаем лишние поля, если такие были переданы и поле ссылки
        if not hasattr(user, field_name) or field_name == 'self_link':
            continue
        if getattr(user, field_name) != field_value:
            setattr(user, field_name, field_value)
            haveChanges = True

    return None if not haveChanges else user


async def get_user(user_entity: str) -> User | None:
    """
    Получить пользователя по тг_id или shared_link
    :param user_entity: str - tg_Id или уникальная ссылка пользователя
    :return: dict | None
    """
    user = await User.get_or_none(tg_id=user_entity)
    if not user:
        user = await User.get_or_none(self_link=user_entity)
    if user:
        return user
    return None


@app.post("/login", response_model=BasedResponse)
async def login(request: Request, login_data: LoginRequest):
    basedResponse = {
        'status': 200,
        'message': 'OK',
        'user_info': {},
        'user_exist': True,
    }
    # превращаем полученную строку с информацией из ТГ в словарь
    user_info = parse_tg_object(login_data.tg_info)
    # Если не удалось выпарсить информацию из tg-iniData, то возвращаем ошибку
    if not user_info:
        return JSONResponse({
            'status': 400,
            'message': 'Bad Request',
            'user_info': {},
            'user_exist': False,
        })

    # формируем массив с ключами таблицы как у модели пользователя
    user_info['birthday'] = login_data.birthday
    user_info['self_link'] = ''.join(
        [random.choice(string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase) for i in
         range(10)])
    # проверяем, если такой пользователь уже есть, то обновим по нему данные
    basedResponse['user_info'] = user_info
    user = await get_user(user_info['tg_id'])
    # Если пользователь уже сохранен
    if user:
        # то первым делом обновим информацию о ссылке пользователя на ту, что в бд
        user_info['self_link'] = user.self_link
        # Проверим есть ли различие в переданных данных
        user = check_user_difference(user, user_info)
        # Если различия есть - то сохраним их
        if user:
            await user.save()
        return JSONResponse(basedResponse)
    # сохраним пользователя
    await User.create(**user_info)
    return JSONResponse(basedResponse)


@app.post("/load_user_info", response_model=BasedResponse)
async def load_user_info(request: Request, user_data: UserLoadRequest):
    basedResponse = {
        'status': 404,
        'message': 'Not Found',
        'user_info': {},
        'user_exist': False,
    }
    # Если мы перешли сюда из полученной ссылки, то подгрузим данные по ней
    user = await get_user(user_data.shared_link)
    # Если удалось найти по ней данные, то обновим  респонс
    if user:
        basedResponse['status'] = 200
        basedResponse['message'] = 'OK'
        basedResponse['user_info'] = user.to_json
    # Теперь проверим а зарегистрирован ли пользователь который смотрим станицу
    user_info = parse_tg_object(user_data.tg_info)
    # Если он зареган, то отобразим в ответе
    if user_info:
        user = await get_user(user_info['tg_id'])
        if user:
            basedResponse['user_exist'] = True
    print(basedResponse)
    return JSONResponse(basedResponse)



@app.post('/change_link')
async def change_shared_link(request: Request, user_entity: ChangeLinkRequest):
    await sleep(2)
    basedResponse = {
        'status': 200,
        'message': 'OK',
    }

    user = await get_user(user_entity.tg_id)
    if not user:
        return JSONResponse({
            'status': 400,
            'message': 'Bad Request',
        })
    user.self_link = user_entity.shared_link
    await user.save()
    return basedResponse
