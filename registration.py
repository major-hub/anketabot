from datetime import datetime

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from language import TEXT, lang_txt, YUR_TEXT, ANKETA
from btn import BTN_TEXT, YUR_BTN_TEXT, ANKETA_BTN_TEXT
from config import *


def start(update: Update, _: CallbackContext):
    # telegram_id = update.effective_user.id
    keyboard = BTN_TEXT['til']
    update.message.reply_html(
        lang_txt,
        reply_markup=ReplyKeyboardMarkup.from_row(keyboard, True)
    )
    return TIL


def get_til(update: Update, context: CallbackContext):
    if update.message.text == "🇺🇿 Ўзбек тили":
        lang = 'uz'
    else:
        lang = 'ru'
    context.user_data['til'] = lang
    keyboard = BTN_TEXT[lang]['boshlash']
    update.message.reply_html(TEXT[lang]['boshlash'].format(update.effective_user.mention_html()))
    update.message.reply_html(
        TEXT[lang]['boshlash2'],
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return BOSHLASH


def get_boshlash(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    telegram_id = update.effective_user.id
    context.user_data['telegram_id'] = telegram_id
    print(datetime.now())
    now = str(datetime.now())
    context.user_data['begin_at'] = now
    conn = sqlite3.connect('data.sqlite3')
    conn.cursor().execute("INSERT INTO anketa (telegram_id, begin_at) VALUES (?, ?)", (telegram_id, now))
    conn.commit()
    conn.close()

    keyboard = BTN_TEXT[lang]['shaxs']
    text = TEXT[lang]['shaxs']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return SHAXS


def get_shaxs(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['shaxs'] = update.message.text
    keyboard = BTN_TEXT[lang]['hudud'].keys()
    text = TEXT[lang]['hudud']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return HUDUD


def get_hudud(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['hudud'] = update.message.text
    shaxs = context.user_data['shaxs']
    if shaxs == BTN_TEXT[lang]['shaxs'][0]:  # Jismoniy bolsa
        keyboard = BTN_TEXT[lang]['ish_karta']
        text = TEXT[lang]['ish_karta']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_row(keyboard, True)
        )
        return ISH_KARTA
    else:  # Yuridik bolsa
        keyboard = BTN_TEXT[lang]['hudud'].get(context.user_data['hudud'])
        text = TEXT[lang]['bank']['yuridik']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return BANK


def get_ish_karta(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    karta = update.message.text
    context.user_data['ish_karta'] = karta
    if karta == BTN_TEXT[lang]['ish_karta'][0]:  # ha
        text = TEXT[lang]['bank']['yes']
        keyboard = BTN_TEXT[lang]['hudud'].get(context.user_data['hudud'])
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return BANK
    else:  # yoq
        text = TEXT[lang]['bank']['no']
        keyboard = BTN_TEXT[lang]['hudud'].get(context.user_data['hudud'])
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return BANK


def get_bank(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['bank'] = update.message.text
    shaxs = context.user_data['shaxs']
    if shaxs == BTN_TEXT[lang]['shaxs'][0]:  # Jismoniy bolsa
        karta = context.user_data['ish_karta']
        if karta == BTN_TEXT[lang]['ish_karta'][0]:  # ha
            keyboard = BTN_TEXT[lang]['tashrif']
            text = TEXT[lang]['tashrif']['first']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return TASHRIF_MUDDAT
        else:
            keyboard = BTN_TEXT[lang]['sabab']
            text = TEXT[lang]['sabab']['first']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return SABAB
    else:
        keyboard = BTN_TEXT[lang]['sabab']
        text = TEXT[lang]['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SABAB


def get_sabab(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    sabab = update.message.text
    if sabab == BTN_TEXT[lang]['sabab'][-1]:  # boshqa
        text = TEXT[lang]['sabab']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SABAB_B
    elif sabab == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['sabab']
        text = TEXT[lang]['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SABAB
    else:
        context.user_data['sabab'] = sabab
        keyboard = BTN_TEXT[lang]['tashrif']
        text = TEXT[lang]['tashrif']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TASHRIF_MUDDAT


def get_tashrif(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    tashrif = update.message.text
    if tashrif == BTN_TEXT[lang]['tashrif'][-1]:  # boshqa
        text = TEXT[lang]['tashrif']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TASHRIF_MUDDAT_B
    elif tashrif == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['tashrif']
        text = TEXT[lang]['tashrif']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TASHRIF_MUDDAT
    else:
        context.user_data['tashrif'] = update.message.text
        shaxs = context.user_data['shaxs']
        if shaxs == BTN_TEXT[lang]['shaxs'][0]:  # Jismoniy bolsa
            keyboard = BTN_TEXT[lang]['mahsulot']
        else:  # yuridik
            keyboard = YUR_BTN_TEXT[lang]['mahsulot']
        text = TEXT[lang]['mahsulot']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return MAHSULOT


def get_mahsulot(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    mah = update.message.text

    shaxs = context.user_data['shaxs']
    if shaxs == BTN_TEXT[lang]['shaxs'][0]:  # Jismoniy bolsa
        if mah == BTN_TEXT[lang]['mahsulot'][-1]:  # boshqa
            text = TEXT[lang]['mahsulot']['other']
            keyboard = BTN_TEXT[lang]['back']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return MAHSULOT_B
        elif mah == BTN_TEXT[lang]['back'][0]:  # ortga
            # Bitta tepasidagi text + button
            keyboard = BTN_TEXT[lang]['mahsulot']
            text = TEXT[lang]['mahsulot']['first']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return MAHSULOT
        else:
            context.user_data['mahsulot'] = mah
            if mah == BTN_TEXT[lang]['mahsulot'][0]:  # kredit
                text = TEXT[lang]['kreditlar']['first']
                keyboard = BTN_TEXT[lang]['kreditlar']['first']
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return KREDITLAR
            elif mah == BTN_TEXT[lang]['mahsulot'][1]:  # omonat
                text = TEXT[lang]['omonatlar']['first']
                keyboard = BTN_TEXT[lang]['omonatlar']['first']
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return OMONATLAR
            elif mah == BTN_TEXT[lang]['mahsulot'][2]:  # tolovlar
                text = TEXT[lang]['tolovlar']['first']
                keyboard = BTN_TEXT[lang]['tolovlar']['first']
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return TOLOVLAR
            elif mah == BTN_TEXT[lang]['mahsulot'][3]:  # valyuta
                text = TEXT[lang]['valyuta']['first']
                keyboard = BTN_TEXT[lang]['valyuta']['first']
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return VALYUTA
            elif mah == BTN_TEXT[lang]['mahsulot'][4]:  # pul otkazma(transfer)
                text = TEXT[lang]['transfer']['first']
                keyboard = BTN_TEXT[lang]['transfer']['first']
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return PUL_OTKAZMALAR
            else:
                context.user_data['mahsulot'] = mah
                keyboard = ANKETA_BTN_TEXT[lang]['savol1']
                context.user_data['anketa'] = {}
                context.user_data['anketa']['params1'] = []
                if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
                    text = ANKETA[lang]['savol1'] + "\n\n" + \
                           f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
                else:
                    text = ANKETA[lang]['savol1'] + "\n\n" + \
                           f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return SAVOL1
    else:  # yuridik shaxs
        if mah == YUR_BTN_TEXT[lang]['mahsulot'][-1]:  # boshqa
            text = YUR_TEXT[lang]['mahsulot']['other']
            keyboard = YUR_BTN_TEXT[lang]['back']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return MAHSULOT_B
        elif mah == BTN_TEXT[lang]['back'][0]:  # ortga
            # Bitta tepasidagi text + button
            keyboard = YUR_BTN_TEXT[lang]['mahsulot']
            text = YUR_TEXT[lang]['mahsulot']['first']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return MAHSULOT
        else:
            if mah == YUR_BTN_TEXT[lang]['mahsulot'][0]:  # kredit
                text = YUR_TEXT[lang]['kreditlar']['first']
                keyboard = YUR_BTN_TEXT[lang]['kreditlar']['first']
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return YKREDITLAR
            elif mah == YUR_BTN_TEXT[lang]['mahsulot'][1]:  # depozit
                text = YUR_TEXT[lang]['omonatlar']['first']
                keyboard = YUR_BTN_TEXT[lang]['omonatlar']['first']
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return YOMONAT
            elif mah == YUR_BTN_TEXT[lang]['mahsulot'][2]:  # hisob
                text = YUR_TEXT[lang]['hisob']['first']
                keyboard = YUR_BTN_TEXT[lang]['hisob']['first']
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return YHISOB
            elif mah == YUR_BTN_TEXT[lang]['mahsulot'][3]:  # valyuta
                text = YUR_TEXT[lang]['valyuta']['first']
                keyboard = YUR_BTN_TEXT[lang]['valyuta']['first']
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return YVALYUTA
            elif mah == YUR_BTN_TEXT[lang]['mahsulot'][4]:  # boshqa
                # other ni qoshish
                keyboard = ANKETA_BTN_TEXT[lang]['savol1']
                context.user_data['anketa'] = {}
                context.user_data['anketa']['params1'] = []
                if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
                    text = ANKETA[lang]['savol1'] + "\n\n" + \
                           f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
                else:
                    text = ANKETA[lang]['savol1'] + "\n\n" + \
                           f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return SAVOL1
            else:
                keyboard = ANKETA_BTN_TEXT[lang]['savol1']
                context.user_data['anketa'] = {}
                context.user_data['anketa']['params1'] = []
                if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
                    text = ANKETA[lang]['savol1'] + "\n\n" + \
                           f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
                else:
                    text = ANKETA[lang]['savol1'] + "\n\n" + \
                           f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
                update.message.reply_html(
                    text,
                    reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
                )
                return SAVOL1


# YURIDIK KREDIT
def yur_kredit_first(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['kreditlar'] = {}
    context.user_data['kreditlar']['first'] = update.message.text
    keyboard = YUR_BTN_TEXT[lang]['kreditlar']['xizmat']
    text = YUR_TEXT[lang]['kreditlar']['xizmat']['first']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return YKR_XIZMAT


def yur_kredit_xizmat(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    xizmat = update.message.text
    if xizmat == YUR_BTN_TEXT[lang]['kreditlar']['xizmat'][-1]:  # boshqa
        text = YUR_TEXT[lang]['kreditlar']['xizmat']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YKR_XIZMAT_B
    elif xizmat == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = YUR_BTN_TEXT[lang]['kreditlar']['xizmat']
        text = YUR_TEXT[lang]['kreditlar']['xizmat']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YKR_XIZMAT
    else:
        context.user_data['kreditlar']['xizmat'] = update.message.text
        keyboard = YUR_BTN_TEXT[lang]['kreditlar']['sabab']
        text = YUR_TEXT[lang]['kreditlar']['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YKR_SABAB


def yur_kredit_sabab(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    sabab = update.message.text
    if sabab == YUR_BTN_TEXT[lang]['kreditlar']['sabab'][-1]:  # boshqa
        text = YUR_TEXT[lang]['kreditlar']['sabab']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YKR_SABAB_B
    elif sabab == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = YUR_BTN_TEXT[lang]['kreditlar']['sabab']
        text = YUR_TEXT[lang]['kreditlar']['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YKR_SABAB
    else:
        context.user_data['kreditlar']['sabab'] = update.message.text
        keyboard = YUR_BTN_TEXT[lang]['kreditlar']['xabar']
        text = YUR_TEXT[lang]['kreditlar']['xabar']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YKR_XABAR


def yur_kredit_xabar(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['kreditlar']['xabar'] = update.message.text
    keyboard = YUR_BTN_TEXT[lang]['kreditlar']['baholash']
    text = YUR_TEXT[lang]['kreditlar']['baholash']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return YKR_BAHOLASH


def yur_kredit_baholash(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['kreditlar']['baholash'] = update.message.text

    keyboard = ANKETA_BTN_TEXT[lang]['savol1']
    context.user_data['anketa'] = {}
    context.user_data['anketa']['params1'] = []
    if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
    else:
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return SAVOL1


# YURIDIK OMONATLAR
def yur_omonat_first(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['omonatlar'] = {}
    context.user_data['omonatlar']['first'] = update.message.text
    keyboard = YUR_BTN_TEXT[lang]['omonatlar']['sabab']
    text = YUR_TEXT[lang]['omonatlar']['sabab']['first']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return YO_SABAB


def yur_omonat_sabab(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    sabab = update.message.text
    if sabab == YUR_BTN_TEXT[lang]['omonatlar']['sabab'][-1]:  # boshqa
        text = YUR_TEXT[lang]['omonatlar']['sabab']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YO_SABAB_B
    elif sabab == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = YUR_BTN_TEXT[lang]['omonatlar']['sabab']
        text = YUR_TEXT[lang]['omonatlar']['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YO_SABAB
    else:
        context.user_data['omonatlar']['sabab'] = update.message.text

        keyboard = ANKETA_BTN_TEXT[lang]['savol1']
        context.user_data['anketa'] = {}
        context.user_data['anketa']['params1'] = []
        if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
        else:
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SAVOL1


# YURIDIK HISOB
def yur_hisob_first(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    hisob = update.message.text
    if hisob == YUR_BTN_TEXT[lang]['hisob']['first'][-1]:  # boshqa
        text = YUR_TEXT[lang]['hisob']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YHISOB_B
    elif hisob == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = YUR_BTN_TEXT[lang]['hisob']['first']
        text = YUR_TEXT[lang]['hisob']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YHISOB
    else:
        context.user_data['hisob'] = {}
        context.user_data['hisob']['first'] = update.message.text
        keyboard = YUR_BTN_TEXT[lang]['hisob']['vaqt']
        text = YUR_TEXT[lang]['hisob']['vaqt']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YHISOB_VAQT


def yur_hisob_vaqt(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['hisob']['vaqt'] = update.message.text
    keyboard = YUR_BTN_TEXT[lang]['hisob']['xato']
    text = YUR_TEXT[lang]['hisob']['xato']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return YHISOB_XATO


def yur_hisob_xato(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['hisob']['xato'] = update.message.text
    keyboard = ANKETA_BTN_TEXT[lang]['savol1']
    context.user_data['anketa'] = {}
    context.user_data['anketa']['params1'] = []
    if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
    else:
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return SAVOL1


# YURIDIK VALYUTA
def yur_valyuta_first(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    valyuta = update.message.text
    if valyuta == YUR_BTN_TEXT[lang]['valyuta']['first'][-1]:  # boshqa
        text = YUR_TEXT[lang]['valyuta']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YVALYUTA_B
    elif valyuta == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = YUR_BTN_TEXT[lang]['valyuta']['first']
        text = YUR_TEXT[lang]['valyuta']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return YVALYUTA
    else:
        context.user_data['valyuta'] = {}
        context.user_data['valyuta']['first'] = update.message.text
        keyboard = ANKETA_BTN_TEXT[lang]['savol1']
        context.user_data['anketa'] = {}
        context.user_data['anketa']['params1'] = []
        if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
        else:
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SAVOL1


# KREDITLAR JISMONIY
def get_kredit_first(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['kreditlar'] = {}
    kr = update.message.text
    context.user_data['kreditlar']['first'] = kr
    if kr == BTN_TEXT[lang]['kreditlar']['first'][0]:  # shu bank
        keyboard = BTN_TEXT[lang]['kreditlar']['xizmat']
        text = TEXT[lang]['kreditlar']['xizmat']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KR_XIZMAT
    elif kr == BTN_TEXT[lang]['kreditlar']['first'][1]:  # boshqa bank
        keyboard = BTN_TEXT[lang]['kreditlar']['xizmat']
        text = TEXT[lang]['kreditlar']['xizmat']['second']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KR_XIZMAT
    else:  # yoq desa sondirishga otib ketadi
        context.user_data['kreditlar']['sabab'] = update.message.text
        keyboard = BTN_TEXT[lang]['kreditlar']['sondirish']
        text = TEXT[lang]['kreditlar']['sondirish']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KR_SONDIRISH


def get_kredit_xizmat(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    xizmat = update.message.text
    if xizmat == BTN_TEXT[lang]['kreditlar']['xizmat'][-1]:  # boshqa
        text = TEXT[lang]['kreditlar']['xizmat']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KR_XIZMAT_B
    elif xizmat == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['kreditlar']['xizmat']
        text = TEXT[lang]['kreditlar']['xizmat']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KR_XIZMAT
    else:
        context.user_data['kreditlar']['xizmat'] = update.message.text
        if context.user_data['kreditlar']['first'] == BTN_TEXT[lang]['kreditlar']['first'][0]:  # shu bank
            text = TEXT[lang]['kreditlar']['sabab']['first']
        else:
            text = TEXT[lang]['kreditlar']['sabab']['second']  # boshqa bank
        keyboard = BTN_TEXT[lang]['kreditlar']['sabab']

        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KR_SABAB


def get_kredit_sabab(update: Update, context: CallbackContext):
    # kr sabab other
    lang = context.user_data['til']
    sabab = update.message.text
    if sabab == BTN_TEXT[lang]['kreditlar']['sabab'][-1]:  # boshqa
        text = TEXT[lang]['kreditlar']['sabab']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KR_SABAB_B
    elif sabab == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['kreditlar']['sabab']
        text = TEXT[lang]['kreditlar']['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KR_SABAB
    else:
        context.user_data['kreditlar']['sabab'] = update.message.text
        keyboard = BTN_TEXT[lang]['kreditlar']['sondirish']
        text = TEXT[lang]['kreditlar']['sondirish']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KR_SONDIRISH


def get_kredit_sondirish(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    son = update.message.text
    context.user_data['kreditlar']['sondirish'] = son
    if son == BTN_TEXT[lang]['kreditlar']['sondirish'][0]:  # bank orqali
        keyboard = BTN_TEXT[lang]['kreditlar']['bank']
        text = TEXT[lang]['kreditlar']['bank']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KRB
    else:
        keyboard = BTN_TEXT[lang]['kreditlar']['mobil']['first']
        text = TEXT[lang]['kreditlar']['mobil']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KRM


# KREDIT BANK
def get_kredit_bank(update: Update, context: CallbackContext):
    # kredit bank other
    lang = context.user_data['til']
    bank = update.message.text
    if bank == BTN_TEXT[lang]['kreditlar']['bank'][-1]:  # boshqa
        text = TEXT[lang]['kreditlar']['bank']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KRB_B
    elif bank == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['kreditlar']['bank']
        text = TEXT[lang]['kreditlar']['bank']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KRB
    else:
        context.user_data['kreditlar']['bank'] = {}
        context.user_data['kreditlar']['bank']['first'] = update.message.text
        keyboard = BTN_TEXT[lang]['kreditlar']['mobil']['xabar']
        text = TEXT[lang]['kreditlar']['mobil']['xabar']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KRM_XABAR


# KREDIT MOBIL
def get_kredit_mobil_first(update: Update, context: CallbackContext):
    # kredit mobil other
    lang = context.user_data['til']
    mobil = update.message.text
    if mobil == BTN_TEXT[lang]['kreditlar']['mobil']['first'][-1]:  # boshqa
        text = TEXT[lang]['kreditlar']['mobil']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KRM_B
    elif mobil == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['kreditlar']['mobil']['first']
        text = TEXT[lang]['kreditlar']['mobil']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KRM
    else:
        context.user_data['kreditlar']['mobil'] = {}
        context.user_data['kreditlar']['mobil']['first'] = update.message.text
        keyboard = BTN_TEXT[lang]['kreditlar']['mobil']['ilova']
        text = TEXT[lang]['kreditlar']['mobil']['ilova']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KRM_ILOVA


def get_kredit_mobil_ilova(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['kreditlar']['mobil']['ilova'] = update.message.text
    keyboard = BTN_TEXT[lang]['kreditlar']['mobil']['xabar']
    text = TEXT[lang]['kreditlar']['mobil']['xabar']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return KRM_XABAR


def get_kredit_mobil_xabar(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    sondirish = context.user_data['kreditlar']['sondirish']
    if sondirish == BTN_TEXT[lang]['kreditlar']['sondirish'][0]:  # bank
        context.user_data['kreditlar']['bank']['xabar'] = update.message.text

        keyboard = ANKETA_BTN_TEXT[lang]['savol1']
        context.user_data['anketa'] = {}
        context.user_data['anketa']['params1'] = []
        if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
        else:
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SAVOL1
    else:  # mobil ilova
        context.user_data['kreditlar']['mobil']['xabar'] = update.message.text
        keyboard = BTN_TEXT[lang]['kreditlar']['mobil']['baholash']
        text = TEXT[lang]['kreditlar']['mobil']['baholash']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return KRM_BAHOLASH


def get_kredit_mobil_baholash(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['kreditlar']['mobil']['baholash'] = update.message.text
    keyboard = ANKETA_BTN_TEXT[lang]['savol1']
    context.user_data['anketa'] = {}
    context.user_data['anketa']['params1'] = []
    if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
    else:
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return SAVOL1


# OMONATLAR
def get_omonat_first(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['omonatlar'] = {}
    om = update.message.text
    context.user_data['omonatlar']['first'] = om
    if om == BTN_TEXT[lang]['omonatlar']['first'][0]:  # ha shu bank
        keyboard = BTN_TEXT[lang]['omonatlar']['sabab']
        text = TEXT[lang]['omonatlar']['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return O_SABAB
    elif om == BTN_TEXT[lang]['omonatlar']['first'][1]:  # boshqa bank
        keyboard = BTN_TEXT[lang]['omonatlar']['sabab']
        text = TEXT[lang]['omonatlar']['sabab']['second']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return O_SABAB
    else:  # yoq desa shaklga otadi
        keyboard = BTN_TEXT[lang]['omonatlar']['shakl']
        text = TEXT[lang]['omonatlar']['shakl']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return O_SHAKL


def get_omonat_sabab(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    sabab = update.message.text
    if sabab == BTN_TEXT[lang]['omonatlar']['sabab'][-1]:  # boshqa
        text = TEXT[lang]['omonatlar']['sabab']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return O_SABAB_B
    elif sabab == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['omonatlar']['sabab']
        text = TEXT[lang]['omonatlar']['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return O_SABAB
    else:
        context.user_data['omonatlar']['sabab'] = update.message.text
        keyboard = BTN_TEXT[lang]['omonatlar']['shakl']
        text = TEXT[lang]['omonatlar']['shakl']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return O_SHAKL


def get_omonat_shakl(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    shakl = update.message.text
    context.user_data['omonatlar']['shakl'] = shakl

    if shakl == BTN_TEXT[lang]['omonatlar']['shakl'][0]:  # yani Bank
        keyboard = BTN_TEXT[lang]['omonatlar']['bank']['first']
        text = TEXT[lang]['omonatlar']['bank']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OB
    elif shakl == BTN_TEXT[lang]['omonatlar']['shakl'][1]:  # mobil
        keyboard = BTN_TEXT[lang]['omonatlar']['mobil']['first']
        text = TEXT[lang]['omonatlar']['mobil']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OM


# OMONATLAR BANK
def get_omonat_bank(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    bank = update.message.text
    if bank == BTN_TEXT[lang]['omonatlar']['bank']['first'][-1]:  # boshqa
        text = TEXT[lang]['omonatlar']['bank']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OB_B
    elif bank == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['omonatlar']['bank']
        text = TEXT[lang]['omonatlar']['bank']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OB
    else:
        context.user_data['omonatlar']['bank'] = {}
        context.user_data['omonatlar']['bank']['first'] = update.message.text
        keyboard = BTN_TEXT[lang]['omonatlar']['bank']['baholash']
        text = TEXT[lang]['omonatlar']['bank']['baholash']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OB_BAHOLASH


def get_omonat_baholash(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    baholash = update.message.text
    if baholash == BTN_TEXT[lang]['omonatlar']['bank']['baholash'][-1]:  # boshqa
        text = TEXT[lang]['omonatlar']['bank']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OB_BAHOLASH
    elif baholash == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['omonatlar']['bank']['baholash']
        text = TEXT[lang]['omonatlar']['bank']['baholash']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OB_BAHOLASH_B
    else:
        context.user_data['omonatlar']['bank']['baholash'] = update.message.text
        keyboard = BTN_TEXT[lang]['omonatlar']['mobil']['shartnoma']
        text = TEXT[lang]['omonatlar']['mobil']['shartnoma']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OM_SHARTNOMA


# OMONATLAR MOBIL
def get_omonat_mobil(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    mobil = update.message.text
    if mobil == BTN_TEXT[lang]['omonatlar']['mobil']['first'][-1]:  # boshqa
        text = TEXT[lang]['omonatlar']['mobil']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OM_B
    elif mobil == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['omonatlar']['mobil']['first']
        text = TEXT[lang]['omonatlar']['mobil']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OM
    else:
        context.user_data['omonatlar']['mobil'] = {}
        context.user_data['omonatlar']['mobil']['first'] = update.message.text
        keyboard = BTN_TEXT[lang]['omonatlar']['mobil']['boshqarish']
        text = TEXT[lang]['omonatlar']['mobil']['boshqarish']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OM_BOSHQARISH


def get_omonat_mobil_boshqarish(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['omonatlar']['mobil']['boshqarish'] = update.message.text
    keyboard = BTN_TEXT[lang]['omonatlar']['mobil']['shartnoma']
    text = TEXT[lang]['omonatlar']['mobil']['shartnoma']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return OM_SHARTNOMA


def get_omonat_mobil_shartnoma(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    shakl = context.user_data['omonatlar']['shakl']
    if shakl == BTN_TEXT[lang]['omonatlar']['shakl'][0]:  # bank
        context.user_data['omonatlar']['bank']['shartnoma'] = shakl
        keyboard = ANKETA_BTN_TEXT[lang]['savol1']
        context.user_data['anketa'] = {}
        context.user_data['anketa']['params1'] = []
        if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
        else:
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SAVOL1
    else:
        context.user_data['omonatlar']['mobil']['shartnoma'] = update.message.text
        keyboard = BTN_TEXT[lang]['omonatlar']['mobil']['baholash']
        text = TEXT[lang]['omonatlar']['mobil']['baholash']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return OM_BAHOLASH


def get_omonat_mobil_baholash(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['omonatlar']['mobil']['baholash'] = update.message.text

    keyboard = ANKETA_BTN_TEXT[lang]['savol1']
    context.user_data['anketa'] = {}
    context.user_data['anketa']['params1'] = []
    if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
    else:
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return SAVOL1


# TOLOVLAR
def get_tolovlar(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    tolov = update.message.text
    context.user_data['tolovlar'] = {}
    context.user_data['tolovlar']['first'] = tolov

    if tolov == BTN_TEXT[lang]['tolovlar']['first'][0]:  # naqd pul
        keyboard = BTN_TEXT[lang]['tolovlar']['naqd_pul']
        text = TEXT[lang]['tolovlar']['naqd_pul']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TNAQD_PUL
    elif tolov == BTN_TEXT[lang]['tolovlar']['first'][1]:  # naqd pulsiz (mobil)
        keyboard = BTN_TEXT[lang]['tolovlar']['naqd_pulsiz']
        text = TEXT[lang]['tolovlar']['naqd_pulsiz']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TNAQD_PULSIZ


def get_tolovlar_naqd_pul(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    naqd_pul = update.message.text
    if naqd_pul == BTN_TEXT[lang]['tolovlar']['naqd_pul'][-1]:  # boshqa
        text = TEXT[lang]['tolovlar']['naqd_pul']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TNAQD_PUL_B
    elif naqd_pul == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['tolovlar']['naqd_pul']
        text = TEXT[lang]['tolovlar']['naqd_pul']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TNAQD_PUL
    else:
        context.user_data['tolovlar']['naqd_pul'] = update.message.text
        context.user_data['tolovlar']['mobil'] = {}

        context.user_data['tolovlar']['mobil']['tur2'] = []
        keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['yulduzchathird']
        text = TEXT[lang]['tolovlar']['mobil']['tur2']['first'] + "\n\n" + \
               f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur2'][0]}</b>"  # yani tur2 ning birinchi savoli ketti
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TM_TUR2


def get_tolovlar_naqd_pulsiz(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    naqd_pulsiz = update.message.text
    if naqd_pulsiz == BTN_TEXT[lang]['tolovlar']['naqd_pulsiz'][-1]:  # boshqa
        text = TEXT[lang]['tolovlar']['naqd_pul']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TNAQD_PULSIZ_B
    elif naqd_pulsiz == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['tolovlar']['naqd_pulsiz']
        text = TEXT[lang]['tolovlar']['naqd_pulsiz']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TNAQD_PULSIZ
    else:
        context.user_data['tolovlar']['naqd_pulsiz'] = update.message.text

        keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['first']
        text = TEXT[lang]['tolovlar']['mobil']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TMOBIL


# def get_tolovlar_mobil_sabab(update: Update, context: CallbackContext):
#     lang = context.user_data['til']
#     sabab = update.message.text
#     if sabab == BTN_TEXT[lang]['tolovlar']['mobil']['sabab'][-1]:  # boshqa
#         text = TEXT[lang]['tolovlar']['mobil']['sabab']['other']
#         keyboard = BTN_TEXT[lang]['back']
#         update.message.reply_html(
#             text,
#             reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
#         )
#         return TM_SABAB_B
#     elif sabab == BTN_TEXT[lang]['back'][0]:  # ortga
#         # Bitta tepasidagi text + button
#         keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['sabab']
#         text = TEXT[lang]['tolovlar']['mobil']['sabab']['first']
#         update.message.reply_html(
#             text,
#             reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
#         )
#         return TM_SABAB
#     else:
#         context.user_data['tolovlar']['mobil']['sabab'] = update.message.text
#         keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['first']
#         text = TEXT[lang]['tolovlar']['mobil']['first']
#         update.message.reply_html(
#             text,
#             reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
#         )
#         return TMOBIL


def get_tolovlar_mobil(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['tolovlar']['mobil'] = {}
    mb = update.message.text
    context.user_data['tolovlar']['mobil']['first'] = mb

    if mb == BTN_TEXT[lang]['tolovlar']['mobil']['first'][0]:  # shu bank
        context.user_data['tolovlar']['mobil']['tur1'] = []

        keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['yulduzcha']
        text = TEXT[lang]['tolovlar']['mobil']['tur1']['first'] + "\n\n" + \
               f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur1'][0]}</b>"  # yani tur1 ning birinchi savoli ketti
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TM_TUR1
    elif mb == BTN_TEXT[lang]['tolovlar']['mobil']['first'][1]:  # boshqa bank
        context.user_data['tolovlar']['mobil']['tur1'] = []

        keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['yulduzcha']
        text = TEXT[lang]['tolovlar']['mobil']['tur1']['second'] + "\n\n" + \
               f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur1'][0]}</b>"  # yani tur1 ning birinchi savoli ketti
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TM_TUR1
    else:  # Payme, Click
        context.user_data['tolovlar']['mobil']['tur1'] = []

        keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['yulduzchathird']
        text = TEXT[lang]['tolovlar']['mobil']['tur1']['third'] + "\n\n" + \
               f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur1third'][0]}</b>"  # yani tur1 ning birinchi savoli ketti
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TM_TUR1THIRD


def get_tolovlar_mobil_tur1(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['tolovlar']['mobil']['tur1'].append(update.message.text)
    length = len(context.user_data['tolovlar']['mobil']['tur1'])
    if length < 5:
        if context.user_data['tolovlar']['mobil']['first'] == BTN_TEXT[lang]['tolovlar']['mobil']['first'][0]:  # shu
            text = TEXT[lang]['tolovlar']['mobil']['tur1']['first'] + "\n\n" + \
                   f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur1'][length]}</b>"
        else:
            text = TEXT[lang]['tolovlar']['mobil']['tur1']['second'] + "\n\n" + \
                   f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur1'][length]}</b>"
        update.message.reply_html(text)
        return TM_TUR1

    tolov = context.user_data['tolovlar']['first']
    if tolov == BTN_TEXT[lang]['tolovlar']['first'][0]:  # naqd pul
        keyboard = ANKETA_BTN_TEXT[lang]['savol1']
        context.user_data['anketa'] = {}
        context.user_data['anketa']['params1'] = []
        if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
        else:
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SAVOL1
    else:
        context.user_data['tolovlar']['mobil']['tur2'] = []
        keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['yulduzchathird']
        text = TEXT[lang]['tolovlar']['mobil']['tur2']['first'] + "\n\n" + \
               f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur2'][0]}</b>"  # yani tur2 ning birinchi savoli ketti
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TM_TUR2


def get_tolovlar_mobil_tur1_third(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['tolovlar']['mobil']['tur1'].append(update.message.text)
    length = len(context.user_data['tolovlar']['mobil']['tur1'])
    if length < 6:
        text = TEXT[lang]['tolovlar']['mobil']['tur1']['third'] + "\n\n" + \
               f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur1third'][length]}</b>"
        update.message.reply_html(text)
        return TM_TUR1THIRD

    tolov = context.user_data['tolovlar']['first']
    if tolov == BTN_TEXT[lang]['tolovlar']['first'][0]:  # naqd pul
        keyboard = ANKETA_BTN_TEXT[lang]['savol1']
        context.user_data['anketa'] = {}
        context.user_data['anketa']['params1'] = []
        if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
        else:
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SAVOL1
    else:
        context.user_data['tolovlar']['mobil']['tur2'] = []
        keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['yulduzchathird']
        text = TEXT[lang]['tolovlar']['mobil']['tur2']['first'] + "\n\n" + \
               f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur2'][0]}</b>"  # yani tur2 ning birinchi savoli ketti
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return TM_TUR2


def get_tolovlar_mobil_tur2(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['tolovlar']['mobil']['tur2'].append(update.message.text)
    length = len(context.user_data['tolovlar']['mobil']['tur2'])
    if length < 6:
        text = TEXT[lang]['tolovlar']['mobil']['tur2']['first'] + "\n\n" + \
               f"<b>{BTN_TEXT[lang]['tolovlar']['mobil']['tur2'][length]}</b>"
        update.message.reply_html(text)
        return TM_TUR2

    keyboard = BTN_TEXT[lang]['tolovlar']['mobil']['baholash']
    text = TEXT[lang]['tolovlar']['mobil']['baholash']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return TM_BAHOLASH


def get_tolovlar_mobil_baholash(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['tolovlar']['mobil']['baholash'] = update.message.text

    keyboard = ANKETA_BTN_TEXT[lang]['savol1']
    context.user_data['anketa'] = {}
    context.user_data['anketa']['params1'] = []
    if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
    else:
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return SAVOL1


# VALYUTA
def get_valyuta(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    first = update.message.text
    if first == BTN_TEXT[lang]['valyuta']['first'][-1]:  # boshqa
        text = TEXT[lang]['valyuta']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return VALYUTA_B
    elif first == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        text = TEXT[lang]['valyuta']['first']
        keyboard = BTN_TEXT[lang]['valyuta']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return VALYUTA
    else:
        tolov = update.message.text
        context.user_data['valyuta'] = {}
        context.user_data['valyuta']['first'] = tolov

        if tolov == BTN_TEXT[lang]['valyuta']['first'][0]:  # naqd pul
            keyboard = BTN_TEXT[lang]['valyuta']['naqd_pul']
            text = TEXT[lang]['valyuta']['naqd_pul']['first']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return VNAQD_PUL
        elif tolov == BTN_TEXT[lang]['valyuta']['first'][1]:  # naqd pulsiz (mobil)
            keyboard = BTN_TEXT[lang]['valyuta']['mobil']['first']
            text = TEXT[lang]['valyuta']['mobil']['first']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return VM
        else:
            keyboard = ANKETA_BTN_TEXT[lang]['savol1']
            context.user_data['anketa'] = {}
            context.user_data['anketa']['params1'] = []
            if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
                text = ANKETA[lang]['savol1'] + "\n\n" + \
                       f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
            else:
                text = ANKETA[lang]['savol1'] + "\n\n" + \
                       f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return SAVOL1


def get_valyuta_naqd_pul(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    naqd_pul = update.message.text
    print(naqd_pul)
    if naqd_pul == BTN_TEXT[lang]['valyuta']['naqd_pul'][-1]:  # boshqa
        text = TEXT[lang]['valyuta']['naqd_pul']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return VNAQD_PUL_B
    elif naqd_pul == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        text = TEXT[lang]['valyuta']['naqd_pul']['first']
        keyboard = BTN_TEXT[lang]['valyuta']['naqd_pul']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return VNAQD_PUL
    else:
        context.user_data['valyuta']['naqd_pul'] = update.message.text

        keyboard = ANKETA_BTN_TEXT[lang]['savol1']
        context.user_data['anketa'] = {}
        context.user_data['anketa']['params1'] = []
        if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
        else:
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SAVOL1


# valyuta mobil
def get_valyuta_mobil(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['valyuta']['mobil'] = {}
    context.user_data['valyuta']['mobil']['first'] = update.message.text
    keyboard = BTN_TEXT[lang]['valyuta']['mobil']['sabab']
    text = TEXT[lang]['valyuta']['mobil']['sabab']['first']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return VM_SABAB


def get_valyuta_mobil_sabab(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    sabab = update.message.text
    if sabab == BTN_TEXT[lang]['valyuta']['mobil']['sabab'][-1]:  # boshqa
        text = TEXT[lang]['valyuta']['mobil']['sabab']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return VM_SABAB_B
    elif sabab == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['valyuta']['mobil']['sabab']
        text = TEXT[lang]['valyuta']['mobil']['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return VM_SABAB
    else:
        context.user_data['valyuta']['mobil']['sabab'] = update.message.text
        keyboard = BTN_TEXT[lang]['valyuta']['mobil']['baholash']
        text = TEXT[lang]['valyuta']['mobil']['baholash']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return VM_BAHOLASH


def get_valyuta_mobil_baholash(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['valyuta']['mobil']['baholash'] = update.message.text

    keyboard = ANKETA_BTN_TEXT[lang]['savol1']
    context.user_data['anketa'] = {}
    context.user_data['anketa']['params1'] = []
    if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
    else:
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return SAVOL1


# PUL OTKAZMALARI
def get_transfer(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    first = update.message.text
    if first == BTN_TEXT[lang]['transfer']['first'][-1]:  # boshqa
        text = TEXT[lang]['transfer']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PUL_OTKAZMALAR_B
    elif first == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        text = TEXT[lang]['transfer']['first']
        keyboard = BTN_TEXT[lang]['transfer']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PUL_OTKAZMALAR
    else:
        tolov = update.message.text
        context.user_data['transfer'] = {}
        context.user_data['transfer']['first'] = tolov

        if tolov == BTN_TEXT[lang]['transfer']['first'][0]:  # naqd pul
            keyboard = BTN_TEXT[lang]['transfer']['naqd_pul']['first']
            text = TEXT[lang]['transfer']['naqd_pul']['first']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return PNAQD_PUL
        elif tolov == BTN_TEXT[lang]['transfer']['first'][1]:  # naqd pulsiz (mobil)
            keyboard = BTN_TEXT[lang]['transfer']['mobil']['first']
            text = TEXT[lang]['transfer']['mobil']['first']
            update.message.reply_html(
                text,
                reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
            )
            return PM


def get_transfer_naqd_pul(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    naqd_pul = update.message.text
    if naqd_pul == BTN_TEXT[lang]['transfer']['naqd_pul']['first'][-1]:  # boshqa
        text = TEXT[lang]['transfer']['naqd_pul']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PNAQD_PUL_B
    elif naqd_pul == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        text = TEXT[lang]['transfer']['naqd_pul']['first']
        keyboard = BTN_TEXT[lang]['transfer']['naqd_pul']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PNAQD_PUL
    else:
        context.user_data['transfer']['naqd_pul'] = {}
        context.user_data['transfer']['naqd_pul']['first'] = update.message.text
        keyboard = BTN_TEXT[lang]['transfer']['naqd_pul']['baholash']
        text = TEXT[lang]['transfer']['naqd_pul']['baholash']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PNAQD_PUL_BAHOLASH


def get_transfer_naqd_pul_baholash(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    naqd_pul = update.message.text
    if naqd_pul == BTN_TEXT[lang]['transfer']['naqd_pul']['baholash'][-1]:  # boshqa
        text = TEXT[lang]['transfer']['naqd_pul']['baholash']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PNAQD_PUL_BAHOLASH_B
    elif naqd_pul == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['transfer']['naqd_pul']['baholash']
        text = TEXT[lang]['transfer']['naqd_pul']['baholash']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PNAQD_PUL_BAHOLASH
    else:
        context.user_data['transfer']['naqd_pul']['baholash'] = update.message.text

        keyboard = ANKETA_BTN_TEXT[lang]['savol1']
        context.user_data['anketa'] = {}
        context.user_data['anketa']['params1'] = []
        if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
        else:
            text = ANKETA[lang]['savol1'] + "\n\n" + \
                   f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return SAVOL1


# TRANSFER MOBIL
def get_transfer_mobil(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['transfer']['mobil'] = {}
    context.user_data['transfer']['mobil']['first'] = update.message.text
    keyboard = BTN_TEXT[lang]['transfer']['mobil']['sabab']
    text = TEXT[lang]['transfer']['mobil']['sabab']['first']
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return PM_SABAB


def get_transfer_mobil_sabab(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    sabab = update.message.text
    if sabab == BTN_TEXT[lang]['transfer']['mobil']['sabab'][-1]:  # boshqa
        text = TEXT[lang]['transfer']['mobil']['sabab']['other']
        keyboard = BTN_TEXT[lang]['back']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PM_SABAB_B
    elif sabab == BTN_TEXT[lang]['back'][0]:  # ortga
        # Bitta tepasidagi text + button
        keyboard = BTN_TEXT[lang]['transfer']['mobil']['sabab']
        text = TEXT[lang]['transfer']['mobil']['sabab']['first']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PM_SABAB
    else:
        context.user_data['transfer']['mobil']['sabab'] = update.message.text
        keyboard = BTN_TEXT[lang]['transfer']['mobil']['baholash']
        text = TEXT[lang]['transfer']['mobil']['baholash']
        update.message.reply_html(
            text,
            reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
        )
        return PM_BAHOLASH


def get_transfer_mobil_baholash(update: Update, context: CallbackContext):
    lang = context.user_data['til']
    context.user_data['transfer']['mobil']['baholash'] = update.message.text

    keyboard = ANKETA_BTN_TEXT[lang]['savol1']
    context.user_data['anketa'] = {}
    context.user_data['anketa']['params1'] = []
    if context.user_data['shaxs'] == BTN_TEXT[lang]['shaxs'][0]:  # jismoniy
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['jismoniy'][0]}</b>"
    else:
        text = ANKETA[lang]['savol1'] + "\n\n" + \
               f"<b>{ANKETA[lang]['params1']['yuridik'][0]}</b>"
    update.message.reply_html(
        text,
        reply_markup=ReplyKeyboardMarkup.from_column(keyboard, True)
    )
    return SAVOL1
