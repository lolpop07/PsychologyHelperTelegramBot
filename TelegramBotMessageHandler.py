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
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_3_1 = State()
    question_3_2 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    name = State()
    phone = State()
    Insta = State()
    DOB = State()


@dp.message_handler(commands=['start'])
async def cmd_start_handler(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await Form.gender.set()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Мужской', callback_data='Мужской'))
    markup.add(types.InlineKeyboardButton(text='Женский', callback_data='Женский'))
    markup.add(types.InlineKeyboardButton(text='Другое', callback_data='Другое'))
    await bot.send_message(message.chat.id, 'Ваш пол?', reply_markup=markup)


@dp.message_handler(commands=['help'])
async def cmd_help_handler(message: types.Message):
    '''

    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    text = 'Привет, я бот - помошник Ксении. Для того, чтобы начать, отправьте /start.\nДля того, чтобы сбросить все варианты ответов, отправьте /cancel'
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


@dp.callback_query_handler(lambda call: call.data not in ['Мужской', 'Женский', 'Другое'], state=Form.gender)
async def process_gender_invalid(call: types.CallbackQuery, state: FSMContext):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Мужской'))
    markup.add(types.InlineKeyboardButton('Женский'))
    markup.add(types.InlineKeyboardButton('Другое'))
    await bot.send_message(call.message.chat.id, 'Неправельный пол. Выбирите вариант один из предложенных вариантов.',
                           reply_markup=markup)


@dp.callback_query_handler(state=Form.gender)
async def process_gender(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = call.data
        await Form.next()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Да', callback_data='Да'))
        markup.add(types.InlineKeyboardButton(text='Нет', callback_data='Нет'))
        await bot.send_message(call.message.chat.id, 'Вы хотите сейчас отношений?', reply_markup=markup)


@dp.callback_query_handler(state=Form.question_1)
async def process_question_1(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['state_1'] = call.data
        if Form.question_1 == 'Да':
            text = 'Это превосходно! Рекомендую проанализировать все допущенные ошибки в предыдущих отношениях. ' \
                   'Возможно, отношения начались с сексуального влечения. Или вы уже были приятелями на работе или в ' \
                   'другой сфере и вы оба были не против попробовать. И тд. В любом случае, за этим не было системного ' \
                   'подхода с чётким пониманием - какой тип семьи вы хотите и какая у вас идеальная картина семьи и ' \
                   'партнёра. Рекомендую начать с этого ДО того, как вы начнёте ходить на свидания. Привязаться к ' \
                   'потенциальному партнёру легко. И если окажется, что этот человек совсем не подходит под ваше ' \
                   'видение семьи и жизни - отказывать и прекращать общение может быть болезненно. '
        else:
            text = 'Если с таким настроем вы всё-таки начнёте отношения - скорее всего всё будет развиваться так: В ' \
                   'первое время вы закроете все потребности связанные с отношениями. Далее, когда все потребности (' \
                   'секс, общение, внимание, забота и тд.) будут удовлетворены - ваш интерес к партнёру будет ' \
                   'пропадать. Его изначально и не было. Эта увлеченность была скорее телесной, не более. Но так как вы ' \
                   'не искали себе партнёра на жизнь - через время в этом человеке пропадёт надобность. В лучшем ' \
                   'случае, вы останетесь приятелями. В худшем - закончите ссорой. Закончите вы отношения скорее всего ' \
                   'быстро и холодно. И желания заходить в новые это не прибавит. '

        await bot.send_message(call.message.chat.id, text)
        await Form.next()
        markup = types.InlineKeyboardMarkup(row_width=3)
        answer1='Сходится с вашим портретом идеального партнёра'
        answer2='Не сходится с вашим портретом идеального партнёра, потому что не продуман никакой портрет'
        answer3='Не сходится с вашим портретом идеального партнёра, но человек понравился вам внешне или по другим ' \
                'характеристикам и вы решаете его немного подкорректировать под своего идеальный партнёра '
        markup.add(types.InlineKeyboardButton(text='A', callback_data='answer1'),
                   types.InlineKeyboardButton(text='B', callback_data='answer2'),
                   types.InlineKeyboardButton(text='C', callback_data='answer3'))
        text='Первое свидание. Человек рассказывает вам о себе и это...\n\nA: {0}\n\nB: {1}\n\nC: {2}'.format(answer1,answer2,answer3)
        await bot.send_message(call.message.chat.id, text,
                                        reply_markup=markup)


@dp.callback_query_handler(state=Form.question_2)
async def process_question_2(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_2'] = call.data
        if call.data == 'answer1':
            text = 'Прекрасно, продолжайте общение дальше, чтобы убедиться, что человек вам подходит и в других ' \
                   'аспектах. Держите в голове все-все моменты того, какой вы видите свою идеальную семью. Любые ' \
                   'компромиссы на этом этапе могут в дальнейшем привести к разочарованию. '
        elif call.data == 'answer2':
            text = 'Большинство отношений начинаются потому, что уже хочется секса или потому, что среди всех ' \
                   'потенциальных партнёров этот был самый адекватный. Очень рекомендую сначала разобраться с этими ' \
                   'фундаментальными вопросами, от которых и зависит успех в выборе партнёра. Прописать их и не давать ' \
                   'слабину в моменты, когда партнёр кажется привлекательным или более подходящим, чем все остальные. ' \
                   'Это убережёт вас от траты сил, времени, нервов и денег. '
        else:
            text = 'Такие отношения обречены на провал. Они точно закончатся, причём обоюдной обидой. Один будет ' \
                   'обижаться на то, что другой не поменялся ради него. Второй будет в непонимании, чего тому надо? Он ' \
                   'же сам видел с кем он создаёт отношения. По началу вроде всё устраивало, а сейчас хочет чего-то?! ' \
                   'Не мучайте ни себя, ни другого. На планете ещё как минимум 1 000 000 000 потенциально подходящих ' \
                   'вам партнёров, есть из кого выбрать. Будьте бескомпромиссны в фундаментальных вопросах по поводу ' \
                   'семьи. Основные моменты должны сходиться на 100%. Интересы в кино, предпочтения в еде и тд - ' \
                   'вторичны. '

        await bot.send_message(call.message.chat.id, text)
        await Form.next()
        answer1='Об интересах потенциального партнёра'
        answer2='Оба имеете идеальную картину семьи и обсуждаете её'
        answer3='О любимом кино'
        answer4='Болтаете о чём-то отвлечённом, чтобы не спугнуть'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='A', callback_data='answer1'))
        markup.add(types.InlineKeyboardButton(text='B', callback_data='answer2'))
        markup.add(types.InlineKeyboardButton(text='C', callback_data='answer3'))
        markup.add(types.InlineKeyboardButton(text='D', callback_data='answer4'))

        await bot.send_message(call.message.chat.id, 'Вспомните свои прошлые (или нынешние отношения). Первое свидание, '
                                                 'вы говорите о...\n\nA: {0}\n\nB: {1}\n\nC: {2}\n\nD: {3}'.format(answer1,answer2,answer3,answer4), reply_markup=markup)



@dp.callback_query_handler(state=Form.question_3)
async def process_question_3(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    answer1 = 'Я делаю что-то не так'
    answer2 = 'Он сделал что-то нечестное по отношению ко мне'
    answer3 = 'Мы оба накосячили по отношению друг к другу'
    text_4 = 'Вы замечаете, что партнёр часто недоволен вами (в прошлых или в текущих отношениях), критикует.  Ваши мысли ' \
           'на этот счёт...\n\nA: {0}\n\nB: {1}\n\nC: {2}'.format(answer1, answer2, answer3)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='A', callback_data='answer1'),
               types.InlineKeyboardButton(text='B', callback_data='answer2'),
               types.InlineKeyboardButton(text='C', callback_data='answer3'))

    async with state.proxy() as data:
        data['question_3'] = call.data
    if call.data == 'answer2':
        await Form.question_4.set()
        text = 'Поздравляю! Это очень редко происходит. И это очень правильно. Главное, чтобы в идеальной картине ' \
               'были учтены все моменты, с которыми будущая семья обязательно столкнётся. По незнанию можно их ' \
               'пропустить. Подход абсолютно верный, продолжаем! '
        await bot.send_message(call.message.chat.id, text)
        await bot.send_message(call.message.chat.id, text_4, reply_markup=markup)
    elif call.data == 'answer3':
        await Form.question_4.set()
        text = 'Любимое кино - это простой и быстрый способ понять, как мы видим и чувствуем мир. К сожалению, ' \
               'наше любимое кино может нравится и тем, у кого совершенно противоположные взгляды на построение семьи ' \
               'и воспитание детей)) Это важный пункт, но рекомендую его обсудить уже после сверки на совпадение ' \
               'ваших идеальных картин семьи. '
        await bot.send_message(call.message.chat.id, text)
        await bot.send_message(call.message.chat.id, text_4, reply_markup=markup)
    elif call.data == 'answer4':
        await Form.question_4.set()
        text = 'Эта неловкость на свидании нормальна и понятна. К такому мероприятию нужно быть готовым ' \
               'психологически, потому что вершится ваша судьба. От того, с кем вы её свяжете - зависит ваша ' \
               'удовлетворённость собой и жизнью. Рекомендую не робеть, а обсуждать важные фундаментальные моменты, ' \
               'на которых будет строиться ваша будущая семья. Если такого представления ещё нет или не всё ' \
               'определено - рекомендую обучиться тому, как прописывать идеальную картину своей семьи и далее из неё ' \
               'уже будет следовать портрет идеального партнёра. '
        await bot.send_message(call.message.chat.id, text)
        await bot.send_message(call.message.chat.id, text_4, reply_markup=markup)
    else:
        answer1='Ваши интересы сходятся'
        answer2='Ваше интересы не сходятся'
        text = 'A: {0}\n\nB: {1}'.format(answer1,answer2)
        await Form.question_3_1.set()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='A',callback_data='answer1'),
                   types.InlineKeyboardButton(text='B',callback_data='answer2'))
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)


@dp.callback_query_handler(state=Form.question_3_1)
async def process_question_3_1(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_3_1'] = call.data
    if call.data == 'answer1':
        answer1='Это любовь!'
        answer2='Проверите совпадаете ли вы по видению семьи'
        answer3='Попытаетесь что-то уточнить, что это будет уже не так важно - у вас же так много общего!'
        text = 'A: {0}\n\nB: {1}\n\nC: {2}'.format(answer1,answer2,answer3)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='A',callback_data='answer1'),
                   types.InlineKeyboardButton(text='B',callback_data='answer2'),
                   types.InlineKeyboardButton(text='C',callback_data='answer3'))
        await Form.next()
    else:
        answer4 = 'Продолжите общаться на тему идеальной картины семьи'
        answer5 = 'Потеряете интерес, постараете сьзакончить свидание поскорее'
        text = 'A: {0}\n\nB: {1}'.format(answer4,answer5)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='A',callback_data='answer4'),
                   types.InlineKeyboardButton(text='B',callback_data='answer5'))
        await Form.next()

    await bot.send_message(call.message.chat.id, text, reply_markup=markup)


@dp.callback_query_handler(state=Form.question_3_2)
async def process_question_3_2(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_3_2'] = call.data
    if call.data == 'answer1':
        text = 'К сожалению, как правило такие отношения заканчиваются в ближайшие полгода - 2 года. В худшем случае ' \
               'тянутся ещё дольше. В редких случаях по другим вопросам люди тоже совпадают, хотя они это даже не ' \
               'обговаривали. Сойтись по интересам несложно. Семья складывается из того, как 2 человека видят свою ' \
               'жизнь. И из того, какого партнёра они видят рядом с собой в течение этой жизни. Рекомендую сначала ' \
               'разобраться с этими фундаментальными вопросами, от которых и зависит успех в выборе партнёра. '
    elif call.data == 'answer2':
        text = 'Это абсолютно правильное решение. Людей, которые совпадают с вами по интересам может быть 5000000 в ' \
               'мире, а тех, кто смотрит на жизнь и семью также, как и вы - 1000. Именно об этом и стоит говорить на ' \
               'первом свидании. Если понимание это есть, но эти фундаментальные моменты ещё не определены - ' \
               'рекомендую обучиться тому, как их определять и как исходя из этого прописывать портрет желаемого ' \
               'партнёра. '
    elif call.data == 'answer3':
        text = 'Вы пытались))) На самом деле это очень сложно - пытаться отсеивать людей для отношений. Многие могут ' \
               'быть очень обаятельными и действительно сходиться в различных интересах с вами. Но успех отношений ' \
               'зависит от совпадения в фундаментальных взглядах на жизнь и семью. Рекомендую сначала разобраться с ' \
               'этими фундаментальными вопросами, от которых и зависит успех в выборе партнёра. Прописать их и не ' \
               'давать слабину в моменты, когда партнёр кажется привлекательным. Нужно уточнить все-все моменты до ' \
               'конца! Это убережёт вас от траты сил, времени, нервов и денег. '
    elif call.data == 'answer4':
        text = 'Вы действительно можете продолжить обсуждать фундаментальные взгляды на жизнь и отношения. И они ' \
               'могут сходиться. Но именно на основе ваших интересов будет в будущем выбираться досуг, ' \
               'вид и тип отдыха, кино для семейного просмотра и занятие на вечер. И будет очень некомфортно, ' \
               'если ваши интересы будут совсем неинтересны вашему партнёру и наоборот. Но, возможно, вы сможете идти ' \
               'на компромиссы и это не будет для вас неудобством. Вам просто нужно понимать заранее на что вы идёте. '
    else:
        text = 'Не отчаивайтесь - вокруг действительно много-много других потенциально подходящих партнёров. Лучше ' \
               'сказать об этом потенциальному партнёру открыто и как есть, что эти увлечения и интересы для вас ' \
               'важны и принципиальны, лучше не тратить ни его, ни своё время. К сожалению, часто нам не хочется ' \
               'обидеть человека, а в итоге мы обижаем его гораздо сильнее тем, что тратим его время из-за своей ' \
               'нерешительности или ненужной никому "вежливости". Есть специальные упражнения на то, чтобы говорить ' \
               'открыто и прямо, но в то же время деликатно о том, что думаешь и чувствуешь. '

    await bot.send_message(call.message.chat.id, text)
    await Form.question_4.set()
    answer1 = 'Я делаю что-то не так'
    answer2 = 'Он сделал что-то нечестное по отношению ко мне'
    answer3 = 'Мы оба накосячили по отношению друг к другу'
    text='Вы замечаете, что партнёр часто недоволен вами (в прошлых или в текущих отношениях), критикует.  Ваши мысли ' \
         'на этот счёт...\n\nA: {0}\n\nB: {1}\n\nC: {2}'.format(answer1,answer2,answer3)
    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='A',callback_data='answer1'),
               types.InlineKeyboardButton(text='B',callback_data='answer2'),
               types.InlineKeyboardButton(text='C',callback_data='answer3'))
    await bot.send_message(call.message.chat.id,text,reply_markup=markup)


@dp.callback_query_handler(state=Form.question_4)
async def process_question_4(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_4'] = call.data
    if call.data == 'answer1':
        text = 'Возможно, но основная причина в том, что какие-то обещания или правила в ваших отношениях нарушил ' \
               'партнёр. От накосячившего всегда идёт критика и придирки в адрес другого. Так человек преуменьшает ' \
               'вашу важность и ему становится немного легче. Груз от содеянного не так давит. + если он своими ' \
               'придирками вас спровоцирует на конфликт - будет оправдание, что он накосячил потому, что вы такой ' \
               'ужасный. '
    elif call.data == 'answer2':
        text = 'Да, как правило это из-за этого. От накосячившего всегда идёт критика и придирки в адрес другого. Так ' \
               'человек преуменьшает вашу важность и ему становится немного легче. Груз от содеянного не так давит. + ' \
               'если он своими придирками вас спровоцирует на конфликт - будет оправдание, что он накосячил потому, ' \
               'что вы такой ужасный. '
    else:
        text = 'Да, скорее всего. Если мы переживаем, что мы в чём-то накосячили - значит мы точно что-то натворили. ' \
               'Но есть момент. От накосячившего всегда идёт критика и придирки в адрес другого. Так человек ' \
               'преуменьшает вашу важность и ему становится немного легче. Груз от содеянного не так давит. + если он ' \
               'своими придирками вас спровоцирует на конфликт - будет оправдание, что он накосячил потому, ' \
               'что вы такой ужасный. '

    await bot.send_message(call.message.chat.id, text)
    await Form.question_5.set()
    answer1 = 'Хочу. Жду программу.'
    answer2 = 'Хочу, но позже.'
    answer3 = 'Подарю/ расскажу другу.'
    text = 'В следующем месяце я планирую онлайн-курс на тему отношений "Как найти себе подходящего партнёра?" Я ещё ' \
           'в продолжаю дополнять и дописывать программу. Хотели бы узнать о курсе подробнее?\n\nA: {0}\n\nB: {' \
           '1}\n\nC: {2}'.format(answer1, answer2, answer3)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='A', callback_data='answer1'),
               types.InlineKeyboardButton(text='B', callback_data='answer2'),
               types.InlineKeyboardButton(text='C', callback_data='answer3'))
    await bot.send_message(call.message.chat.id, text, reply_markup=markup)


@dp.callback_query_handler(state=Form.question_5)
async def process_question_5(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        data['question_5'] = call.data
    answer1 = 'Про отношения и любовь'
    answer2 = 'Про свободное общение с другими людьми'
    answer3 = 'Про триггеры и негативный опыт (ограничивающие убеждения)'
    answer4 = 'Про Эмоции (как управлять своими/ чужими, как читать эмоции других)'
    answer5 = 'Про то, как сделать саморезентацию для эффективного нетворкинга'
    answer6 = 'Про лучшее понимание себя и своей жизни'
    text='Я обещала добавить в список тех, кому к дню рождения я буду присылать полезные материалы. На какую тему ты ' \
         'хочешь получать от меня полезности к дню рождения? (чтобы новый год жить прошёл ещё круче, ' \
         'чем предыдущий)\nДля выбора нескольких вариантов, нажимайте на них поочередно' \
         '\n\nA: {0}\n\nB: {1}\n\nC: {2}\n\nD: {3}\n\nE: {4}\n\nF: {5}'.format(answer1, answer2, answer3,
                                                                                    answer4,answer5,answer6)

    await Form.next()
    async with state.proxy() as data:
        data['question_6'] = [['A', False] ,['B', False], ['C', False], ['D', False], ['E', False], ['F', False]]
        markup = generate_keyboard(data['question_6'])
    await bot.send_message(call.message.chat.id, text, reply_markup=markup)

@dp.callback_query_handler(state=Form.question_6, text='A')
@dp.callback_query_handler(state=Form.question_6, text='B')
@dp.callback_query_handler(state=Form.question_6, text='C')
@dp.callback_query_handler(state=Form.question_6, text='D')
@dp.callback_query_handler(state=Form.question_6, text='E')
@dp.callback_query_handler(state=Form.question_6, text='F')
async def choice_selection_deselection(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    async with state.proxy() as data:
        for item in data['question_6']:
            if call.data==item[0]:
                item[1]=not item[1]
    markup=generate_keyboard(data['question_6'])
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)


def generate_keyboard(choices):
    '''

    :param data: list of choices: bool,
    :return: Inline keyboard markup telegram.object
    '''
    T=':check_mark:'
    F=':cross_mark:'
    markup=types.InlineKeyboardMarkup(row_width=3)
    for item in choices:
        if item[1] == True:
            button_text=emoji.emojize(item[0] + ': ' +T)
            markup.add(types.InlineKeyboardButton(text=button_text, callback_data=item[0]))
        else:
            button_text = emoji.emojize(item[0] + ': ' + F)
            markup.add(types.InlineKeyboardButton(text=button_text, callback_data=item[0]))
    markup.add(types.InlineKeyboardButton(text='Готово', callback_data='accept'))
    return markup



@dp.callback_query_handler(state=Form.question_6, text='accept')
async def process_question_6(call: types.CallbackQuery, state: FSMContext):
    '''

    '''
    await Form.next()
    text='Оставь здесь, пожалуйста, свои контакты. Не волнуйся, я не буду засылать тебя тоннами спама. Только ' \
         'полезности раз в год на день рождения и в другое время по твоему запросу. '
    await bot.send_message(call.message.chat.id, text)
    await bot.send_message(call.message.chat.id, 'Твоё имя?')


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await bot.send_message(message.chat.id, 'Твой номер телефона?')

@dp.message_handler(state=Form.phone)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['phone'] = message.text

    await Form.next()
    await bot.send_message(message.chat.id, 'Твой Instagram?')

@dp.message_handler(state=Form.Insta)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['Insta'] = message.text

    await Form.next()
    await bot.send_message(message.chat.id, 'Твой день рождения?')


@dp.message_handler(state=Form.DOB)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['DOB'] = message.text

    await state.finish()
    await bot.send_message(message.chat.id, 'Cпасибо!')




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    # await state.finish()
'''
    
'''
