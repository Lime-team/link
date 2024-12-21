from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramForbiddenError
from utils.states import Form_classic
from aiogram.fsm.context import FSMContext

from bot_models.classic_kb import kb_generation, give_kb, kb
from config import default_text, wellcome_text
from menu.mainkb import main_kb
from data.base_creation import DataBase

# Classic mode Router & db
db = DataBase()
router = Router()

# Routers FSM
@router.callback_query(F.data == 'pag:start:0')
async def fill_profile(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form_classic.for_who)
    await call.message.answer('Выбери чат:', reply_markup=kb(False))

@router.message(Form_classic.for_who, F.chat_shared)
async def next1(message: Message, state: FSMContext):
    await state.update_data(for_who=message.chat_shared.chat_id)
    await state.set_state(Form_classic.number_of)
    await message.answer('Участников (максимальное количество)', reply_markup=kb_generation(['10', '∞']))

@router.message(Form_classic.number_of)
async def next2(message: Message, state: FSMContext):
    if message.text.isdigit() or message.text == '∞':
        await state.update_data(number_of=message.text)
        await state.set_state(Form_classic.number_of_wins)
        await message.answer('Победителей:', reply_markup=kb_generation('1'))
    else: 
        await message.answer('Введи число!')

@router.message(Form_classic.number_of_wins)
async def next3(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(number_of_wins=message.text)
        await state.set_state(Form_classic.photo)
        await message.answer('Отправь картинку', reply_markup=kb_generation('Обычная картинка'))
    else:
        await message.answer('Число!')

@router.message(Form_classic.photo, F.photo)
async def next4(message: Message, state: FSMContext):
    photo_user = message.photo[-1].file_id
    await state.update_data(photo=photo_user)
    await state.set_state(Form_classic.short_description)
    await message.answer("Введи описание", reply_markup=kb_generation('Обычное описание'))

@router.message(Form_classic.photo, F.text == 'Обычная картинка')
async def next5(message: Message, state: FSMContext):
    photo = FSInputFile("bot_models//give.jpg")
    await state.update_data(photo=photo)
    
    await state.set_state(Form_classic.short_description)
    await message.answer("Короткое описание:", reply_markup=kb_generation('Стандартное'))

@router.message(Form_classic.short_description)
async def next6(message: Message, state: FSMContext, bot: Bot):
    default = default_text
    if message.text == 'Стандартное':
        await state.update_data(short_description=default)
    else:
        await state.update_data(short_description=message.text)

    data = await state.get_data()


    number_of = data['number_of']
    number_wins = data['number_of_wins']

    await message.answer('Give created in your channel!', reply_markup=kb_generation(['Another give', 'Menu'], one_time=True))

    text_info = f"""🎁 <b>Розыгрыш!</b> 🎁

Максимум участников: {number_of}
Победителей: {number_wins}

Описание: {data["short_description"]}"""
    try:
        await bot.send_photo(chat_id=data['for_who'], photo=data['photo'], caption=text_info, reply_markup=give_kb())
    except TelegramForbiddenError:
        await message.answer('Бот не в канале/нет прав админа')
    await state.clear()

@router.message(F.text == 'Another give')
async def another_give(message: Message, state: FSMContext):
    await state.set_state(Form_classic.for_who)
    await message.answer('Выбери чат', reply_markup=kb())

@router.message(F.text == 'Menu')
async def another_give(message: Message, state: FSMContext):
    await state.set_state(Form_classic.for_who)
    await message.answer(wellcome_text, reply_markup=main_kb.as_markup())

# Callback Data Join Btn
@router.callback_query(F.data == 'join')
async def next7(call: CallbackQuery, state: FSMContext):

    give_id = call.message.message_id


    new_data = call.message.caption.split('\n')

    number_of, number_wins = new_data[2:4]

    number_of = number_of.split(': ')[1]
    number_wins = int(number_wins.split(': ')[1])


    if number_of == '∞':
        number_of = 1000000


    db.create_db()
    db.insert_data(give_id=give_id, num_of=number_of, num_w=number_wins)

    nickname = call.from_user.username


    check = db.add_user(new_user=nickname, give_id=call.message.message_id)

    if check is True:
        await call.answer('Присоединился!')
        
    elif check is False:
        await call.answer('Уже участвуешь!')
        print(f'Give id: {call.message.message_id}')
    elif check == 'full':
        await call.answer('Мест нет!')



# Callback Data Start Btn        
@router.callback_query(F.data == '!start!')
async def launch(call: CallbackQuery, bot: Bot):

    user = await bot.get_chat_member(chat_id=call.message.chat.id, user_id=call.from_user.id)


    if user.status in ['administrator', 'creator']:

        give_id = call.message.message_id
        res = db.start_give(give_id=give_id)

        if len(res) == 0:
            await call.answer('Недостаточно победителей')
        else:
            text = """Победили...: \n"""
            for i, j in enumerate(res, 1):
                temp = f'{i} место - @{j}\n'
                text += temp


            await call.message.delete()
            await call.message.answer('Розыгрыш запущен')
            await call.message.answer(text)
    else:

        await call.answer("Нет прав админа")
