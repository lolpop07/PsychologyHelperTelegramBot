# -*- coding: utf-8 -*-

import logging
import emoji
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import csv


logging.basicConfig(level=logging.INFO)

logging.basicConfig(filename='BotLog.log', filemode='w', level=logging.INFO)
f = open('BOT_API_KEY.txt', 'r')
API_KEY = f.readline()  # read the API_KEY from file
f.close()

bot = Bot(token=API_KEY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):

    gender = State()  # Will be represented in storage as 'Form:gender'
    name = State()
    phone = State()
    question_1 = State()
    question_1a = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    Insta = State()


@dp.message_handler(commands=['start'])
async def cmd_start_handler(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await Form.gender.set()
    markup = types.ReplyKeyboardMarkup()
    markup.add('Приятно познакомиться!')
    await bot.send_message(message.chat.id, 'Привет! Я Ксения Абрамова. Квалифицированный психолог и счастливая жена '
                                            '- уже 5 лет в отношениях. По моим рекомендациям уже больше 30 пар '
                                            'построили крепкие и счастливые отношениям с min ссор и max любви и '
                                            'понимания.', reply_markup=markup)


@dp.message_handler(commands=['help'])
async def cmd_help_handler(message: types.Message):
    '''

    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    text = 'Привет, я бот - помошник Ксении. Для того, чтобы начать, отправьте /start.\nДля того, чтобы сбросить все ' \
           'варианты ответов, отправьте /cancel'
    await bot.send_message(message.chat.id, text, reply_markup=markup)


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Отменяем ваши решения', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await bot.send_message(message.chat.id, 'Отмена завершена', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text='Приятно познакомиться!', state='*')
async def greet_handler(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup()
    markup.add('Начать тест')
    await bot.send_message(message.chat.id, 'Теперь о тесте. Он предназначен помочь тебе лучше разобраться в теме '
                                            'отношений. На каждый твой ответ я буду давать обратную связь. Так ты '
                                            'сможешь не только выявить пробелы, но и сразу разобраться как '
                                            'действовать эффективнее в будущем.', reply_markup=markup)

@dp.message_handler(text='Начать тест', state='*')
async def start_quest(message: types.Message, state: FSMContext):
    await Form.gender.set()

    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Мужской', callback_data='M'))
    markup.add(types.InlineKeyboardButton(text='Женский', callback_data='F'))

    await bot.send_message(message.chat.id,'Ваш пол?', reply_markup=markup)

@dp.callback_query_handler(state=Form.gender)
async def process_gender(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = call.data
        await Form.next()

        await bot.send_message(call.message.chat.id, 'Ваше имя?', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await bot.send_message(message.chat.id,"Ваш номер телефона?")

@dp.message_handler(state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await Form.next()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Да', callback_data='Да'))
    markup.add(types.InlineKeyboardButton(text='Нет', callback_data='Нет'))
    await bot.send_message(message.chat.id, 'Вы сейчас в отношениях?', reply_markup=markup)



@dp.callback_query_handler(state=Form.question_1)
async def process_question_1(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_1'] = call.data
        if call.data == 'Да':
            text = 'Вы хотите:\nА. закончить эти отношения и построить новые гармоничные и счастливые;\n\nВ. ' \
                   'реанимировать нынешние отношения и наполнить их любовью и взаимопониманием? '
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton(text='A',callback_data='A'),types.InlineKeyboardButton(text='B',callback_data='B'))
            await Form.question_1a.set()
        else:
            text = 'Это лучший момент, чтобы проходить этот тест и разбираться в теме отношений.\nПриступим!'
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Приступим',callback_data='Приступим'))
            await Form.question_1a.set()
        await bot.send_message(call.message.chat.id,text, reply_markup=markup)


@dp.callback_query_handler(state=Form.question_1a)
async def process_question_1a(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['question_1a'] = call.data
        if call.data == 'A':
            text='Спасибо за откровенность! Такое решение часто трудно принять, но лучше понять это как можно ' \
                 'раньше.\nТогда вы сможете построить действительно крутые и доверительные отношения с тем, ' \
                 'кто будет подходить вам на 100%. И не будете тратить время на того, с кем вы уже сейчас видите, ' \
                 'что ничего не получается.\nПродолжайте тест. Здесь вы сможете увидеть промахи, которые вы допустили ' \
                 'при выборе текущего партнёра и получите полезные данные о том, что обязательно нужно обсудить в ' \
                 'начале отношений. Тогда ещё на стадии выбора партнёра вы будете уверены, что выбираете себе самого ' \
                 'подходящего. '
            await bot.send_message(call.message.chat.id,text)
            text='Вспомните, как вы выбирали себе текущего партнёра?\n\nА. По внутренним ощущениям - есть ли ' \
                 'притяжение к партнёру, влечение, нравится ли внешность...\n\nВ. По общим интересам - есть ли о чём ' \
                 'поговорить, есть ли общие шутки, весело ли вместе '
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='A',callback_data='A'),types.InlineKeyboardButton(text='B', callback_data='B'))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await Form.next()
        elif call.data == 'B':
            text='Здорово! Часто при первых трудностях люди хотят всё бросить и начать новые отношения. Вы молодчина, ' \
                 'что хотите сохранить то, что уже создано.\nИногда в моменты кризиса с партнёром нужно вернуться на ' \
                 'точку "0" - а почему мы вообще вместе? Вернёмся назад. '
            await bot.send_message(call.message.chat.id, text)
            text='Вспомните, как вы выбирали себе текущего партнёра?\n\nА. По внутренним ощущениям - есть ли ' \
                 'притяжение к партнёру, влечение, нравится ли внешность...\n\nВ. По общим интересам - есть ли о чём ' \
                 'поговорить, есть ли общие шутки, весело ли вместе '
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='A',callback_data='A'),
                       types.InlineKeyboardButton(text='B', callback_data='B'))
            await bot.send_message(call.message.chat.id,text, reply_markup=markup)
            await Form.next()
        else:
            text = 'Представь, что ты сейчас выбираешь себе партнёра для будущих отношений. Как будешь ' \
                   'выбирать?\n\nА. По внутренним ощущениям - есть ли притяжение к партнёру, влечение, нравится ли ' \
                   'внешность...\n\nВ. По общим интересам - есть ли о чём поговорить, есть ли общие шутки, ' \
                   'весело ли вместе '
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='A',callback_data='A'),
                       types.InlineKeyboardButton(text='B', callback_data='B'))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
            await Form.next()


@dp.callback_query_handler(state=Form.question_2)
async def process_question_2(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    await Form.next()
    async with state.proxy() as data:
        data['question_2'] = call.data
        if call.data == 'A':
            text = 'Такие отношения начинаются быстро, ярко и красиво... К сожалению, как правило и заканчиваются ' \
                   'также быстро - в ближайшие полгода-2 года. В худшем случае тянутся ещё дольше. В редких случаях ' \
                   'по другим вопросам люди тоже совпадают, но это случайность, на которую я не советую расчитывать\n\n' \
                   'А. Меня такой вариант устраивает, хочу экспериментировать над своей жизнью\n\n' \
                   'В. Меня такой вариант не устраивает, хочу построить долгосрочные отношения'
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='A',callback_data='A'),
                       types.InlineKeyboardButton(text='B', callback_data='B'))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)
        else:
            text = 'Something \n\n' \
                   'А. Меня такой вариант устраивает, хочу экспериментировать над своей жизнью\n\n' \
                   'В. Меня такой вариант не устраивает, хочу построить долгосрочные отношения'
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='A',callback_data='A'),
                       types.InlineKeyboardButton(text='B', callback_data='B'))
            await bot.send_message(call.message.chat.id, text, reply_markup=markup)


@dp.callback_query_handler(state=Form.question_3)
async def process_question_3(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_3'] = call.data
    if call.data == 'A':
        text = 'Спасибо за честность! Желаю вам удачи в построении отношений) дальнейшая информация из теста ' \
               'неактуальна при таком подходе. '
        await bot.send_message(call.message.chat.id, text)
        async with state.proxy() as data:
            await save_answers(data)
        await state.finish()
    else:
        await Form.next()
        text = 'Выбрать партнёра в отношения не джинсы купить. Если вытянутся коленки - вы сможете их выбросить в ' \
               'любой момент. А отношения закончить так стремительно очень сложно, особенно, когда уже есть ' \
               'привязанность.\n\nРекомендую сначала разобраться с фундаментальными вопросами, от которых и зависит ' \
               'успех в выборе партнёра. '
        await bot.send_message(call.message.chat.id, text)
        text = 'На первой встрече вы говорите о...\n\nА. Об интересах друг друга\n\nВ. О планах и целях на ' \
               'жизнь\n\nС. О чём-то интересном и весёлом '
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='A', callback_data='A'),
                   types.InlineKeyboardButton(text='B', callback_data='B'),
                   types.InlineKeyboardButton(text='C', callback_data='C'))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)


@dp.callback_query_handler(state=Form.question_4)
async def process_question_4(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_4'] = call.data
    if call.data == 'A':
        text = 'Вы пытались))) На самом деле это очень сложно - пытаться отсеивать людей для отношений. Многие могут ' \
               'быть очень обаятельными и действительно сходиться в различных интересах с вами. Но успех отношений ' \
               'зависит от совпадения в фундаментальных взглядах на жизнь и семью.\nРекомендую сначала разобраться с ' \
               'этими фундаментальными вопросами, от которых и зависит успех в выборе партнёра. Это убережёт вас от ' \
               'траты сил, времени, нервов и денег. '
    elif call.data == 'B':
        text = 'Это абсолютно правильное решение.\nЛюдей, которые совпадают с вами по интересам может быть 5000000 в ' \
               'мире, а тех, кто смотрит на жизнь и семью также, как и вы - 1000. Именно об этом и стоит говорить на ' \
               'первом свидании.\n\nЕсли понимание это есть, но эти фундаментальные моменты ещё не определены - ' \
               'рекомендую обучиться тому, как их определять и как исходя из этого прописывать портрет желаемого ' \
               'партнёра. '
    else:
        text = 'Эта неловкость на свидании нормальна и понятна. К такому мероприятию нужно быть готовым ' \
               'психологически, потому что вершится ваша судьба. От того, с кем вы её свяжете - зависит ваша ' \
               'удовлетворённость собой и жизнью.\n\nРекомендую не робеть, а обсуждать важные фундаментальные ' \
               'моменты, на которых будет строиться ваша будущая семья.\n\nЕсли такого представления ещё нет или не ' \
               'всё определено - рекомендую обучиться тому, как прописывать идеальную картину своей семьи и далее из ' \
               'неё уже будет следовать портрет идеального партнёра. '

    await bot.send_message(call.message.chat.id, text)
    await Form.next()
    text = 'Когда у вас первый секс?\n\nА. Чем раньше, тем лучше, нужно понять сексуальную совместимость и удовлетворить потребность.\n\nВ. После того, как выстроены крепкие дружеские отношения.\n\nС. После свадьбы.'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='A', callback_data='A'),
               types.InlineKeyboardButton(text='B', callback_data='B'),
               types.InlineKeyboardButton(text='C', callback_data='C'))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup)


@dp.callback_query_handler(state=Form.question_5)
async def process_question_5(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_5'] = call.data
    text = 'На самом деле действительно самый верный вариант - заниматься сексом как можно ПОЗЖЕ.\nСекс - это очень ' \
           'сильная привязка - телесная и эмоциоанльная. И после него уже очень трудно холодно оценить, подходит ли ' \
           'вам этот потенциальный патрнёр на роль спутника жизни, с которым вы будете строить крепкую семью, ' \
           'воспитывать детей. Точно ли вы хотите прожить с ним всю жизнь? А чтобы ваши дети были похожи на этого ' \
           'человек? Чтобы они переняли что-то от него?\nА уверенны ли вы, что этот человек не сбежит при виде первых ' \
           'семейных или жизненных трудностей?\nПосле секса очень трудно отвечать на эти вопросы. Поэтому по старым ' \
           'традициям люди занимались сексом уже после свадьбы, чтобы максимально непредвзято выбрать себе партнёра ' \
           'на жизнь. '
    await bot.send_message(call.message.chat.id, text)
    await Form.next()
    text = 'Когда съезжаться?\n\nА. Сразу, приду на свидание с чемоданом и котом.\n\nВ. Через месяц. Чтобы не платить ' \
           'за аренду или сэкономить на коммуналке и еде.\n\nС. После первого секса. Так секс будет чаще.\n\nD. После ' \
           'того, как вы решили быть семьей. '
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='A', callback_data='A'),
               types.InlineKeyboardButton(text='B', callback_data='B'),
               types.InlineKeyboardButton(text='C', callback_data='C'),
               types.InlineKeyboardButton(text='D', callback_data='D'))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup)


@dp.callback_query_handler(state=Form.question_6)
async def process_question_6(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_6'] = call.data
    await Form.next()
    text='Конечно, это очень приятно, когда доступ к сексу с самого утра и можно меньше или вообще не платить за ' \
         'квартиру (девичий лайфхак). Но съезжаться всё-таки рекомендую, когда вы уже решили, быть семьей. Может ещё ' \
         'не зарегистрировались как семья, но это уже в ближайших планах. Не рекомендую съезжаться "попробовать". ' \
         'Самый ужасный повод. Ради секса или экономии и то понятнее и честнее. "Попробовать" нужно очень неуверенным ' \
         'в стабильности своего мнения мальчикам или девочкам. Никогда не соглашайтесь на такой. Зависните в ' \
         'непонятных для себя ролях. Где вы и не семья, и не свободны. И каждый берёт на себя ответственность только ' \
         'на половинку. Итог: нет развития, стабильности и процветания у семьи + идеальная почва для эмоциональных ' \
         'качелей и замешательства. '
    await bot.send_message(call.message.chat.id, text)
    text='Сколько раз за жизнь стоит проходить обучение по теме отношений и семьи:\n\nА. Единожды, чтобы найти себе ' \
         'подходящего партнёра, а дальше уже сами сообразим.\n\nВ. Несколько раз перед важными этапами в отношениях: ' \
         'перед началом отношений, перед женитьбой, перед детьми.\n\nС. Регулярно, минимум 1 раз в год, ' \
         'на разные темы, касающиеся темы отношений. '
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='A', callback_data='A'),
               types.InlineKeyboardButton(text='B', callback_data='B'),
               types.InlineKeyboardButton(text='C', callback_data='C'))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup)


@dp.callback_query_handler(state=Form.question_7)
async def process_question_7(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_7'] = call.data
    await Form.next()
    text='Конечно, кажется чему там уже учиться, когда находишь себе подходящего партнёра... Но представьте, ' \
         'что вы как руководитель нашли себе прекрасного работника: он позитивный, внимательный, легко обучается, ' \
         'приходит вовремя, заботится о будущем компании, придумывает действительно крутые и жизнеспособные идеи... ' \
         'НО! Вы забыли выдать ему должностные инструкции. И в общем, работник интуитивно справляется, ' \
         'где-то успевает сообразить, что нужно делать на его должности и рабочем месте, но знай он точно, ' \
         'что от него требуется и за что он получается зарплату - справлялся бы вообще идеально. То же самое с ' \
         'другими аспектами семьи. Как договориться, как слышать друг друга, как стать ещё более сплачённой командой, ' \
         'как распределить роли, а как их распределить среди детей... это бесконечный путь самосовершенствования и ' \
         'сплочения сначала двоих, а потом и нескольких людей в крепкую команду. То, что я описываю - несуществующая ' \
         'идеальная семья. Таких примеров почти нет в нашем окружении. Но, обучаясь хотя бы раз в год, ' \
         'можно всё больше быть такой сплочённой и гармоничной сначала парой, а потом и семьей! '
    await bot.send_message(call.message.chat.id, text)
    text='Кстати, я готовлю курс по теме отношений. В живом формате мы проводили его несколько раз, но настало время ' \
         'помочь ребятам и из других городов разобраться с этой темой.\n\nХотелось бы тебе получить информацию об ' \
         'этом курсе, когда он будет готов? '
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Да, очень.', callback_data='A'),
               types.InlineKeyboardButton(text='Да, хочу, но на будущее.', callback_data='B'),
               types.InlineKeyboardButton(text='Порекомендую тебя Ксения друзьям.', callback_data='C'))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup)

@dp.callback_query_handler(state=Form.question_8)
async def process_question_8(call: types.CallbackQuery, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['question_8'] = call.data

    await Form.next()
    text='Здорово)) напиши свой Инстаграм - я пришлю тебе информацию сразу, как будет готова полная программа курса.'
    await bot.send_message(call.message.chat.id, text)

@dp.message_handler(state=Form.Insta)
async def process_Insta(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['Insta'] = message.text
        await save_answers(data)

    await state.finish()
    text='Наш тест окончен)\nЯ рада, что ты дошёл до конца!\nТы молодчина) даже если были допущены ошибки во время ' \
         'построения прошлых или текущих отношений - все их можно исправить и не допускать вновь! Если у меня ' \
         'получилось, то у тебя тоже получится. Обняла! Пока! :red_heart:'
    text=emoji.emojize(text)
    await bot.send_message(message.chat.id, text)
    

async def save_answers(data):
    with open('answers.csv', 'a', encoding='utf-8', newline='') as file:
        w = csv.writer(file, dialect='excel')
        w.writerow(data.keys())
        w.writerow(data.values())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    # await state.finish()