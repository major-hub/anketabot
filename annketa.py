from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from btn import ANKETA_BTN_TEXT, BTN_TEXT
from language import ANKETA
from config import *


def savol1(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['anketa']['params1'].append(update.message.text)
    length = len(context.user_data['anketa']['params1'])
    if length < 5:
        if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['jismoniy'][length]}</b>"
        else:
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['yuridik'][length]}</b>"
        update.message.reply_html(text)
        return SAVOL1
    else:
        keyboard = ANKETA_BTN_TEXT[lang]['savol2']
        context.user_data['anketa']['params2'] = []
        text = ANKETA[lang]['savol2'] + "\n\n" + f"<b>{ANKETA[lang]['params2'][0]}</b>"
        update.message.reply_html(text, reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True))
        return SAVOL2


def savol2(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['anketa']['params2'].append(update.message.text)
    length = len(context.user_data['anketa']['params2'])
    if length < 4:
        text = ANKETA[lang]['savol2'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params2'][length]}</b>"
        update.message.reply_html(text)
        return SAVOL2
    else:
        keyboard = ANKETA_BTN_TEXT[lang]['savol3']
        context.user_data['anketa']['params3'] = []
        text = ANKETA[lang]['savol3'] + "\n\n" + f"<b>{ANKETA[lang]['params3'][0]}</b>"
        update.message.reply_html(text, reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True))
        return SAVOL3


def savol3(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['anketa']['params3'].append(update.message.text)
    length = len(context.user_data['anketa']['params3'])
    if length < 5:
        text = ANKETA[lang]['savol3'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params3'][length]}</b>"
        update.message.reply_html(text)
        return SAVOL3
    else:
        keyboard = ANKETA_BTN_TEXT[lang]['savol4']
        context.user_data['anketa']['params4'] = []
        text = ANKETA[lang]['savol4'] + "\n\n" + f"<b>{ANKETA[lang]['params4'][0]}</b>"
        update.message.reply_html(text, reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True))
        return SAVOL4


def savol4(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['anketa']['params4'].append(update.message.text)
    length = len(context.user_data['anketa']['params4'])
    if length < 9:
        text = ANKETA[lang]['savol4'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params4'][length]}</b>"
        update.message.reply_html(text)
        return SAVOL4
    else:
        keyboard = ANKETA_BTN_TEXT[lang]['savol5']
        text = ANKETA[lang]['savol5']
        update.message.reply_html(text, reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True))
        return SAVOL5


def savol5(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['anketa']['params5'] = update.message.text
    text = ANKETA[lang]['fikr']
    keyboard = ANKETA_BTN_TEXT[lang]['fikr']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return FIKR


def fikr(update: Update, context: CallbackContext):
    komment_fikr = update.message.text
    context.user_data['anketa']['fikr'] = komment_fikr
    text = ANKETA[context.user_data['til']]['last']
    add_todb(context.user_data)
    update.message.reply_html(text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
