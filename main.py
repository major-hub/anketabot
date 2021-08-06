import logging
import sqlite3
import time
import pandas as pd

from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

from config import *
from language import TEXT
from btn import BTN_TEXT
from registration import *
from annketa import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def create_excel():
    conn = sqlite3.connect('data.sqlite3', uri=True)
    pd.read_sql("SELECT * FROM anketa", conn).to_excel('data.xlsx')
    conn.close()
    time.sleep(1)


def send_excel(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id

    if str(telegram_id) in admin_ids:

        create_excel()
        with open('data.xlsx', 'rb') as f:
            update.message.reply_chat_action('upload_document')
            update.message.reply_document(f, filename='anketa.xlsx')


def main():
    updater = Updater(token=TOKEN, workers=100)
    logger.info(f"{updater.bot.get_me().full_name} is started!")
    dp = updater.dispatcher
    init_db()
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', callback=start, run_async=True)],
        states={
            TIL: [MessageHandler(Filters.text(BTN_TEXT['til']), callback=get_til, run_async=True)],
            BOSHLASH: [MessageHandler((Filters.text(BTN_TEXT['uz']['boshlash']) | Filters.text(BTN_TEXT['ru']['boshlash'])), callback=get_boshlash, run_async=True)],
            SHAXS: [MessageHandler((Filters.text(BTN_TEXT['uz']['shaxs']) | Filters.text(BTN_TEXT['ru']['shaxs'])), callback=get_shaxs, run_async=True)],
            HUDUD: [MessageHandler((Filters.text(BTN_TEXT['uz']['hudud']) | Filters.text(BTN_TEXT['ru']['hudud'])), callback=get_hudud, run_async=True)],
            ISH_KARTA: [MessageHandler((Filters.text(BTN_TEXT['uz']['ish_karta']) | Filters.text(BTN_TEXT['ru']['ish_karta'])), callback=get_ish_karta, run_async=True)],
            BANK: [MessageHandler(Filters.text, callback=get_bank, run_async=True)],
            SABAB: [MessageHandler((Filters.text(BTN_TEXT['uz']['sabab']) | Filters.text(BTN_TEXT['ru']['sabab'])), callback=get_sabab, run_async=True)],
            SABAB_B: [MessageHandler(Filters.text, callback=get_sabab, run_async=True)],  # sabab boshqada Filters.text
            TASHRIF_MUDDAT: [MessageHandler((Filters.text(BTN_TEXT['uz']['tashrif']) | Filters.text(BTN_TEXT['ru']['tashrif'])), callback=get_tashrif, run_async=True)],
            TASHRIF_MUDDAT_B: [MessageHandler(Filters.text, callback=get_tashrif, run_async=True)],
            MAHSULOT: [MessageHandler((Filters.text(BTN_TEXT['uz']['mahsulot']) | Filters.text(BTN_TEXT['ru']['mahsulot']) | Filters.text(YUR_BTN_TEXT['uz']['mahsulot']) | Filters.text(YUR_BTN_TEXT['ru']['mahsulot'])), callback=get_mahsulot, run_async=True)],
            MAHSULOT_B: [MessageHandler(Filters.text, callback=get_mahsulot, run_async=True)],
            # KREDITLAR
            KREDITLAR: [MessageHandler((Filters.text(BTN_TEXT['uz']['kreditlar']['first']) | Filters.text(BTN_TEXT['ru']['kreditlar']['first'])), callback=get_kredit_first, run_async=True)],
            KR_XIZMAT: [MessageHandler((Filters.text(BTN_TEXT['uz']['kreditlar']['xizmat']) | Filters.text(BTN_TEXT['ru']['kreditlar']['xizmat'])), callback=get_kredit_xizmat, run_async=True)],
            KR_XIZMAT_B: [MessageHandler(Filters.text, callback=get_kredit_xizmat, run_async=True)],
            KR_SABAB: [MessageHandler((Filters.text(BTN_TEXT['uz']['kreditlar']['sabab']) | Filters.text(BTN_TEXT['ru']['kreditlar']['sabab'])), callback=get_kredit_sabab, run_async=True)],
            KR_SABAB_B: [MessageHandler(Filters.text, callback=get_kredit_sabab, run_async=True)],
            KR_SONDIRISH: [MessageHandler((Filters.text(BTN_TEXT['uz']['kreditlar']['sondirish']) | Filters.text(BTN_TEXT['ru']['kreditlar']['sondirish'])), callback=get_kredit_sondirish, run_async=True)],
            KRB: [MessageHandler((Filters.text(BTN_TEXT['uz']['kreditlar']['bank']) | Filters.text(BTN_TEXT['ru']['kreditlar']['bank'])), callback=get_kredit_bank, run_async=True)],
            KRB_B: [MessageHandler(Filters.text, callback=get_kredit_bank, run_async=True)],
            KRM: [MessageHandler((Filters.text(BTN_TEXT['uz']['kreditlar']['mobil']['first']) | Filters.text(BTN_TEXT['ru']['kreditlar']['mobil']['first'])), callback=get_kredit_mobil_first, run_async=True)],
            KRM_B: [MessageHandler(Filters.text, callback=get_kredit_mobil_first, run_async=True)],
            KRM_ILOVA: [MessageHandler((Filters.text(BTN_TEXT['uz']['kreditlar']['mobil']['ilova']) | Filters.text(BTN_TEXT['ru']['kreditlar']['mobil']['ilova'])), callback=get_kredit_mobil_ilova, run_async=True)],
            KRM_XABAR: [MessageHandler((Filters.text(BTN_TEXT['uz']['kreditlar']['mobil']['xabar']) | Filters.text(BTN_TEXT['ru']['kreditlar']['mobil']['xabar'])), callback=get_kredit_mobil_xabar, run_async=True)],
            KRM_BAHOLASH: [MessageHandler((Filters.text(BTN_TEXT['uz']['kreditlar']['mobil']['baholash']) | Filters.text(BTN_TEXT['ru']['kreditlar']['mobil']['baholash'])), callback=get_kredit_mobil_baholash, run_async=True)],
            # OMONATLAR
            OMONATLAR: [MessageHandler((Filters.text(BTN_TEXT['uz']['omonatlar']['first']) | Filters.text(BTN_TEXT['ru']['omonatlar']['first'])), callback=get_omonat_first, run_async=True)],
            O_SABAB: [MessageHandler((Filters.text(BTN_TEXT['uz']['omonatlar']['sabab']) | Filters.text(BTN_TEXT['ru']['omonatlar']['sabab'])), callback=get_omonat_sabab, run_async=True)],
            O_SABAB_B: [MessageHandler(Filters.text, callback=get_omonat_sabab, run_async=True)],
            O_SHAKL: [MessageHandler((Filters.text(BTN_TEXT['uz']['omonatlar']['shakl']) | Filters.text(BTN_TEXT['ru']['omonatlar']['shakl'])), callback=get_omonat_shakl, run_async=True)],
            OB: [MessageHandler((Filters.text(BTN_TEXT['uz']['omonatlar']['bank']['first']) | Filters.text(BTN_TEXT['ru']['omonatlar']['bank']['first'])), callback=get_omonat_bank, run_async=True)],
            OB_B: [MessageHandler(Filters.text, callback=get_omonat_bank, run_async=True)],
            OB_BAHOLASH: [MessageHandler((Filters.text(BTN_TEXT['uz']['omonatlar']['bank']['baholash']) | Filters.text(BTN_TEXT['ru']['omonatlar']['bank']['baholash'])), callback=get_omonat_baholash, run_async=True)],
            OB_BAHOLASH_B: [MessageHandler(Filters.text, callback=get_omonat_baholash, run_async=True)],
            OM: [MessageHandler((Filters.text(BTN_TEXT['uz']['omonatlar']['mobil']['first']) | Filters.text(BTN_TEXT['ru']['omonatlar']['mobil']['first'])), callback=get_omonat_mobil, run_async=True)],
            OM_B: [MessageHandler(Filters.text, callback=get_omonat_mobil, run_async=True)],
            OM_BOSHQARISH: [MessageHandler((Filters.text(BTN_TEXT['uz']['omonatlar']['mobil']['boshqarish']) | Filters.text(BTN_TEXT['ru']['omonatlar']['mobil']['boshqarish'])), callback=get_omonat_mobil_boshqarish, run_async=True)],
            OM_SHARTNOMA: [MessageHandler((Filters.text(BTN_TEXT['uz']['omonatlar']['mobil']['shartnoma']) | Filters.text(BTN_TEXT['ru']['omonatlar']['mobil']['shartnoma'])), callback=get_omonat_mobil_shartnoma, run_async=True)],
            OM_BAHOLASH: [MessageHandler((Filters.text(BTN_TEXT['uz']['omonatlar']['mobil']['baholash']) | Filters.text(BTN_TEXT['ru']['omonatlar']['mobil']['baholash'])), callback=get_omonat_mobil_baholash, run_async=True)],
            # TOLOVLAR
            TOLOVLAR: [MessageHandler((Filters.text(BTN_TEXT['uz']['tolovlar']['first']) | Filters.text(BTN_TEXT['ru']['tolovlar']['first'])), callback=get_tolovlar, run_async=True)],
            TNAQD_PUL: [MessageHandler((Filters.text(BTN_TEXT['uz']['tolovlar']['naqd_pul']) | Filters.text(BTN_TEXT['ru']['tolovlar']['naqd_pul'])), callback=get_tolovlar_naqd_pul, run_async=True)],
            TNAQD_PUL_B: [MessageHandler(Filters.text, callback=get_tolovlar_naqd_pul, run_async=True)],
            TNAQD_PULSIZ: [MessageHandler((Filters.text(BTN_TEXT['uz']['tolovlar']['naqd_pulsiz']) | Filters.text(BTN_TEXT['ru']['tolovlar']['naqd_pulsiz'])), callback=get_tolovlar_naqd_pulsiz, run_async=True)],
            TNAQD_PULSIZ_B: [MessageHandler(Filters.text, callback=get_tolovlar_naqd_pulsiz, run_async=True)],
            TMOBIL: [MessageHandler((Filters.text(BTN_TEXT['uz']['tolovlar']['mobil']['first']) | Filters.text(BTN_TEXT['ru']['tolovlar']['mobil']['first'])), callback=get_tolovlar_mobil, run_async=True)],
            # TM_SABAB: [MessageHandler((Filters.text(BTN_TEXT['uz']['tolovlar']['mobil']['sabab']) | Filters.text(BTN_TEXT['ru']['tolovlar']['mobil']['sabab'])), callback=get_tolovlar_mobil_sabab, run_async=True)],
            # TM_SABAB_B: [MessageHandler(Filters.text, callback=get_tolovlar_mobil_sabab, run_async=True)],
            TM_TUR1: [MessageHandler((Filters.text(BTN_TEXT['uz']['tolovlar']['mobil']['yulduzcha']) | Filters.text(BTN_TEXT['ru']['tolovlar']['mobil']['yulduzcha'])), callback=get_tolovlar_mobil_tur1, run_async=True)],
            TM_TUR1THIRD: [MessageHandler((Filters.text(BTN_TEXT['uz']['tolovlar']['mobil']['yulduzchathird']) | Filters.text(BTN_TEXT['ru']['tolovlar']['mobil']['yulduzchathird'])), callback=get_tolovlar_mobil_tur1_third, run_async=True)],
            TM_TUR2: [MessageHandler((Filters.text(BTN_TEXT['uz']['tolovlar']['mobil']['yulduzchathird']) | Filters.text(BTN_TEXT['ru']['tolovlar']['mobil']['yulduzchathird'])), callback=get_tolovlar_mobil_tur2, run_async=True)],
            # TM_TUR2_B: [MessageHandler(Filters.text, callback=get_tolovlar_mobil_tur2, run_async=True)],
            # TM_TUR2_NEXT: [MessageHandler(Filters.text, callback=get_tolovlar_mobil_tur2, run_async=True)],
            TM_BAHOLASH: [MessageHandler((Filters.text(BTN_TEXT['uz']['tolovlar']['mobil']['baholash']) | Filters.text(BTN_TEXT['ru']['tolovlar']['mobil']['baholash'])), callback=get_tolovlar_mobil_baholash, run_async=True)],
            # VALYUTA
            VALYUTA: [MessageHandler((Filters.text(BTN_TEXT['uz']['valyuta']['first']) | Filters.text(BTN_TEXT['ru']['valyuta']['first'])), callback=get_valyuta, run_async=True)],
            VALYUTA_B: [MessageHandler(Filters.text, callback=get_valyuta, run_async=True)],
            VNAQD_PUL: [MessageHandler((Filters.text(BTN_TEXT['uz']['valyuta']['naqd_pul']) | Filters.text(BTN_TEXT['ru']['valyuta']['naqd_pul'])), callback=get_valyuta_naqd_pul, run_async=True)],
            VNAQD_PUL_B: [MessageHandler(Filters.text, callback=get_valyuta_naqd_pul, run_async=True)],
            VM: [MessageHandler((Filters.text(BTN_TEXT['uz']['valyuta']['mobil']['first']) | Filters.text(BTN_TEXT['ru']['valyuta']['mobil']['first'])), callback=get_valyuta_mobil, run_async=True)],
            VM_SABAB: [MessageHandler((Filters.text(BTN_TEXT['uz']['valyuta']['mobil']['sabab']) | Filters.text(BTN_TEXT['ru']['valyuta']['mobil']['sabab'])), callback=get_valyuta_mobil_sabab, run_async=True)],
            VM_SABAB_B: [MessageHandler(Filters.text, callback=get_valyuta_mobil_sabab, run_async=True)],
            VM_BAHOLASH: [MessageHandler((Filters.text(BTN_TEXT['uz']['valyuta']['mobil']['baholash']) | Filters.text(BTN_TEXT['ru']['valyuta']['mobil']['baholash'])), callback=get_valyuta_mobil_baholash, run_async=True)],
            # TRANSFER
            PUL_OTKAZMALAR: [MessageHandler((Filters.text(BTN_TEXT['uz']['transfer']['first']) | Filters.text(BTN_TEXT['ru']['transfer']['first'])), callback=get_transfer, run_async=True)],
            PUL_OTKAZMALAR_B: [MessageHandler(Filters.text, callback=get_transfer, run_async=True)],
            PNAQD_PUL: [MessageHandler((Filters.text(BTN_TEXT['uz']['transfer']['naqd_pul']['first']) | Filters.text(BTN_TEXT['ru']['transfer']['naqd_pul']['first'])), callback=get_transfer_naqd_pul, run_async=True)],
            PNAQD_PUL_B: [MessageHandler(Filters.text, callback=get_transfer_naqd_pul, run_async=True)],
            PNAQD_PUL_BAHOLASH: [MessageHandler((Filters.text(BTN_TEXT['uz']['transfer']['naqd_pul']['baholash']) | Filters.text(BTN_TEXT['ru']['transfer']['naqd_pul']['baholash'])), callback=get_transfer_naqd_pul_baholash, run_async=True)],
            PNAQD_PUL_BAHOLASH_B: [MessageHandler(Filters.text, callback=get_transfer_naqd_pul_baholash, run_async=True)],
            PM: [MessageHandler((Filters.text(BTN_TEXT['uz']['transfer']['mobil']['first']) | Filters.text(BTN_TEXT['ru']['transfer']['mobil']['first'])), callback=get_transfer_mobil, run_async=True)],
            PM_SABAB: [MessageHandler((Filters.text(BTN_TEXT['uz']['transfer']['mobil']['sabab']) | Filters.text(BTN_TEXT['ru']['transfer']['mobil']['sabab'])), callback=get_transfer_mobil_sabab, run_async=True)],
            PM_SABAB_B: [MessageHandler(Filters.text, callback=get_transfer_mobil_sabab, run_async=True)],
            PM_BAHOLASH: [MessageHandler((Filters.text(BTN_TEXT['uz']['transfer']['mobil']['baholash']) | Filters.text(BTN_TEXT['ru']['transfer']['mobil']['baholash'])), callback=get_transfer_mobil_baholash, run_async=True)],
            # YURIDIK
            YKREDITLAR: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['kreditlar']['first']) | Filters.text(YUR_BTN_TEXT['ru']['kreditlar']['first'])), callback=yur_kredit_first, run_async=True)],
            YKR_XIZMAT: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['kreditlar']['xizmat']) | Filters.text(YUR_BTN_TEXT['ru']['kreditlar']['xizmat'])), callback=yur_kredit_xizmat, run_async=True)],
            YKR_XIZMAT_B: [MessageHandler(Filters.text, callback=yur_kredit_xizmat, run_async=True)],
            YKR_SABAB: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['kreditlar']['sabab']) | Filters.text(YUR_BTN_TEXT['ru']['kreditlar']['sabab'])), callback=yur_kredit_sabab, run_async=True)],
            YKR_SABAB_B: [MessageHandler(Filters.text, callback=yur_kredit_sabab, run_async=True)],
            YKR_XABAR: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['kreditlar']['xabar']) | Filters.text(YUR_BTN_TEXT['ru']['kreditlar']['xabar'])), callback=yur_kredit_xabar, run_async=True)],
            YKR_BAHOLASH: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['kreditlar']['baholash']) | Filters.text(YUR_BTN_TEXT['ru']['kreditlar']['baholash'])), callback=yur_kredit_baholash, run_async=True)],
            YOMONAT: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['omonatlar']['first']) | Filters.text(YUR_BTN_TEXT['ru']['omonatlar']['first'])), callback=yur_omonat_first, run_async=True)],
            YO_SABAB: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['omonatlar']['sabab']) | Filters.text(YUR_BTN_TEXT['ru']['omonatlar']['sabab'])), callback=yur_omonat_sabab, run_async=True)],
            YO_SABAB_B: [MessageHandler(Filters.text, callback=yur_omonat_sabab, run_async=True)],
            YHISOB: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['hisob']['first']) | Filters.text(YUR_BTN_TEXT['ru']['hisob']['first'])), callback=yur_hisob_first, run_async=True)],
            YHISOB_B: [MessageHandler(Filters.text, callback=yur_hisob_first, run_async=True)],
            YHISOB_VAQT: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['hisob']['vaqt']) | Filters.text(YUR_BTN_TEXT['ru']['hisob']['vaqt'])), callback=yur_hisob_vaqt, run_async=True)],
            YHISOB_XATO: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['hisob']['xato']) | Filters.text(YUR_BTN_TEXT['ru']['hisob']['xato'])), callback=yur_hisob_xato, run_async=True)],
            YVALYUTA: [MessageHandler((Filters.text(YUR_BTN_TEXT['uz']['valyuta']['first']) | Filters.text(YUR_BTN_TEXT['ru']['valyuta']['first'])), callback=yur_valyuta_first, run_async=True)],
            YVALYUTA_B: [MessageHandler(Filters.text, callback=yur_valyuta_first, run_async=True)],
            # ANKETA
            SAVOL1: [MessageHandler((Filters.text(ANKETA_BTN_TEXT['uz']['savol1']) | Filters.text(ANKETA_BTN_TEXT['ru']['savol1'])), callback=savol1, run_async=True)],
            SAVOL2: [MessageHandler((Filters.text(ANKETA_BTN_TEXT['uz']['savol2']) | Filters.text(ANKETA_BTN_TEXT['ru']['savol2'])), callback=savol2, run_async=True)],
            SAVOL3: [MessageHandler((Filters.text(ANKETA_BTN_TEXT['uz']['savol3']) | Filters.text(ANKETA_BTN_TEXT['ru']['savol3'])), callback=savol3, run_async=True)],
            SAVOL4: [MessageHandler((Filters.text(ANKETA_BTN_TEXT['uz']['savol4']) | Filters.text(ANKETA_BTN_TEXT['ru']['savol4'])), callback=savol4, run_async=True)],
            SAVOL5: [MessageHandler((Filters.text(ANKETA_BTN_TEXT['uz']['savol5']) | Filters.text(ANKETA_BTN_TEXT['ru']['savol5'])), callback=savol5, run_async=True)],
            FIKR: [MessageHandler(Filters.text, callback=fikr, run_async=True)],
        },
        fallbacks=[CommandHandler('start', callback=start)]
    ))
    dp.add_handler(CommandHandler('data', callback=send_excel))
    updater.start_polling(drop_pending_updates=True)
    updater.idle()


if __name__ == '__main__':
    main()
