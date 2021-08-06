import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
admin_ids = os.getenv('admin_ids')

# States
(TIL, BOSHLASH, SHAXS, HUDUD, ISH_KARTA, BANK, SABAB, SABAB_B, TASHRIF_MUDDAT, TASHRIF_MUDDAT_B, MAHSULOT, MAHSULOT_B,
 KREDITLAR, KR_XIZMAT, KR_XIZMAT_B, KR_SABAB, KR_SABAB_B, KR_SONDIRISH,
 KRB, KRB_B,
 KRM, KRM_B, KRM_ILOVA, KRM_XABAR, KRM_BAHOLASH,
 OMONATLAR, O_SABAB, O_SABAB_B, O_SHAKL,
 OB, OB_B, OB_BAHOLASH, OB_BAHOLASH_B,
 OM, OM_B, OM_BOSHQARISH, OM_SHARTNOMA, OM_BAHOLASH,
 TOLOVLAR,
 TNAQD_PUL, TNAQD_PUL_B,
 TNAQD_PULSIZ, TNAQD_PULSIZ_B, TMOBIL, TM_SABAB, TM_SABAB_B,
 TM_TUR1, TM_TUR1THIRD, TM_TUR2, TM_TUR2_B, TM_TUR2_NEXT, TM_BAHOLASH,
 VALYUTA, VALYUTA_B,
 VNAQD_PUL, VNAQD_PUL_B,
 VM, VM_SABAB, VM_SABAB_B, VM_BAHOLASH,
 PUL_OTKAZMALAR, PUL_OTKAZMALAR_B,
 PNAQD_PUL, PNAQD_PUL_B, PNAQD_PUL_BAHOLASH, PNAQD_PUL_BAHOLASH_B,
 PM, PM_SABAB, PM_SABAB_B, PM_BAHOLASH,
 YKREDITLAR, YKR_XIZMAT, YKR_XIZMAT_B, YKR_SABAB, YKR_SABAB_B, YKR_XABAR, YKR_BAHOLASH,
 YOMONAT, YO_SABAB, YO_SABAB_B,
 YHISOB, YHISOB_B, YHISOB_VAQT, YHISOB_XATO,
 YVALYUTA, YVALYUTA_B
 ) = map(chr, range(86))

# anketa states
(SAVOL1, SAVOL2, SAVOL3, SAVOL4, SAVOL5, FIKR) = map(chr, range(86, 92))


def init_db():
    conn = sqlite3.connect('data.sqlite3')

    conn.cursor().execute(""" CREATE TABLE IF NOT EXISTS anketa (
                                        id integer PRIMARY KEY autoincrement,
                                        telegram_id INTEGER,
                                        begin_at text,
                                        til varchar,
                                        shaxs varchar,
                                        hudud varchar,
                                        ish_karta varchar,
                                        bank varchar,
                                        sabab varchar,
                                        tashrif varchar,
                                        mahsulot varchar,
                                        kreditlar varchar,
                                        kreditlar_first varchar,
                                        kreditlar_xizmat varchar,
                                        kreditlar_xabar varchar,
                                        kreditlar_baholash varchar,
                                        kreditlar_sabab varchar,
                                        kreditlar_sondirish varchar,
                                        kreditlar_bank varchar,
                                        kreditlar_bank_first varchar,
                                        kreditlar_bank_xabar varchar,
                                        kreditlar_mobil varchar,
                                        kreditlar_mobil_first varchar,
                                        kreditlar_mobil_ilova varchar,
                                        kreditlar_mobil_xabar varchar,
                                        kreditlar_mobil_baholash varchar,
                                        omonatlar varchar,
                                        omonatlar_first varchar,
                                        omonatlar_sabab varchar,
                                        omonatlar_shakl varchar,
                                        omonatlar_bank_first varchar,
                                        omonatlar_bank_baholash varchar,
                                        omonatlar_bank_shartnoma varchar,
                                        omonatlar_mobil varchar,
                                        omonatlar_mobil_first varchar,
                                        omonatlar_mobil_boshqarish varchar,
                                        omonatlar_mobil_shartnoma varchar,
                                        omonatlar_mobil_baholash varchar,
                                        tolovlar varchar,
                                        tolovlar_first varchar,
                                        tolovlar_naqd_pul varchar,
                                        tolovlar_naqd_pul_tur1 varchar,
                                        tolovlar_naqd_pulsiz varchar,
                                        tolovlar_mobil varchar,
                                        tolovlar_mobil_first varchar,
                                        tolovlar_mobil_sabab varchar,
                                        tolovlar_mobil_tur1 varchar,
                                        tolovlar_mobil_tur2 varchar,
                                        tolovlar_mobil_baholash varchar,
                                        valyuta varchar,
                                        valyuta_first varchar,
                                        valyuta_naqd_pul varchar,
                                        valyuta_mobil_first varchar,
                                        valyuta_mobil_sabab varchar,
                                        valyuta_mobil_baholash varchar,
                                        transfer varchar,
                                        transfer_first varchar,
                                        transfer_naqd_pul varchar,
                                        transfer_naqd_pul_first varchar,
                                        transfer_naqd_pul_baholash varchar,
                                        transfer_mobil varchar,
                                        transfer_mobil_first varchar,
                                        transfer_mobil_sabab varchar,
                                        transfer_mobil_baholash varchar,
                                        hisob_first varchar,
                                        hisob_vaqt varchar,
                                        hisob_xato varchar,
                                        hisob varchar,
                                        anketa_params1_1 varchar,
                                        anketa_params1_2 varchar,
                                        anketa_params1_3 varchar,
                                        anketa_params1_4 varchar,
                                        anketa_params1_5 varchar,
                                        anketa_params2_1 varchar,
                                        anketa_params2_2 varchar,
                                        anketa_params2_3 varchar,
                                        anketa_params2_4 varchar,
                                        anketa_params3_1 varchar,
                                        anketa_params3_2 varchar,
                                        anketa_params3_3 varchar,
                                        anketa_params3_4 varchar,
                                        anketa_params3_5 varchar,
                                        anketa_params4_1 varchar,
                                        anketa_params4_2 varchar,
                                        anketa_params4_3 varchar,
                                        anketa_params4_4 varchar,
                                        anketa_params4_5 varchar,
                                        anketa_params4_6 varchar,
                                        anketa_params4_7 varchar,
                                        anketa_params4_8 varchar,
                                        anketa_params4_9 varchar,
                                        anketa_params5 varchar,
                                        anketa_fikr varchar
                                    ); """)
    conn.commit()
    conn.close()


def add_todb(data: dict):
    conn = sqlite3.connect('data.sqlite3')
    telegram_id = data['telegram_id']
    begin_at = data['begin_at']
    c = conn.cursor()
    for d in data.keys():
        if isinstance(data.get(d), str):
            c.execute(f"UPDATE anketa SET '{d}'='{data.get(d)}' WHERE telegram_id=? AND begin_at=?",
                      (telegram_id, begin_at))
        elif isinstance(data.get(d), dict):
            for d_d in data.get(d).keys():
                if isinstance(data.get(d).get(d_d), str):
                    c.execute(f"UPDATE anketa SET '{d}_{d_d}'='{data.get(d).get(d_d)}' "
                              f"WHERE telegram_id=? AND begin_at=?",
                              (telegram_id, begin_at))
                elif isinstance(data.get(d).get(d_d), list):
                    if d == 'anketa':
                        for i, value in enumerate(data.get(d).get(d_d), start=1):
                            c.execute(f"UPDATE anketa SET '{d}_{d_d}_{i}'='{value}' "
                                      f"WHERE telegram_id=? AND begin_at=?",
                                      (telegram_id, begin_at))
                    else:
                        txt = " | ".join(data.get(d).get(d_d))
                        c.execute(f"UPDATE anketa SET '{d}_{d_d}'='{txt}' "
                                  f"WHERE telegram_id=? AND begin_at=?",
                                  (telegram_id, begin_at))
                elif isinstance(data.get(d).get(d_d), dict):
                    for d_d_d in data.get(d).get(d_d).keys():
                        if isinstance(data.get(d).get(d_d).get(d_d_d), str):
                            c.execute(f"UPDATE anketa SET '{d}_{d_d}_{d_d_d}'='{data.get(d).get(d_d).get(d_d_d)}' "
                                      f"WHERE telegram_id=? AND begin_at=?",
                                      (telegram_id, begin_at))
                        elif isinstance(data.get(d).get(d_d).get(d_d_d), list):
                            if d == 'anketa':
                                for i, value in enumerate(data.get(d).get(d_d).get(d_d_d), start=1):
                                    c.execute(f"UPDATE anketa SET '{d}_{d_d}_{d_d_d}_{i}'='{value}' "
                                              f"WHERE telegram_id=? AND begin_at=?",
                                              (telegram_id, begin_at))
                            else:
                                txt = " | ".join(data.get(d).get(d_d).get(d_d_d))
                                c.execute(f"UPDATE anketa SET '{d}_{d_d}_{d_d_d}'='{txt}' "
                                          f"WHERE telegram_id=? AND begin_at=?",
                                          (telegram_id, begin_at))
    conn.commit()
    conn.close()
