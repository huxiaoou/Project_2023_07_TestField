import os
import datetime as dt
import numpy as np
import pandas as pd
from skyrim.whiterun import CCalendar
from skyrim.falkreath import CManagerLibReader


def get_dates(calendar_path: str, bgn_date: str, stp_date: str):
    calendar = CCalendar(calendar_path)
    return calendar.get_iter_list(bgn_date, stp_date, True)


def load_major_minor_data(instruments: list[str], major_minor_dir: str) -> dict[str, pd.DataFrame]:
    manager_major_minor = {}
    for instrument in instruments:
        major_minor_file = f"major_minor.{instrument}.csv.gz"
        major_minor_path = os.path.join(major_minor_dir, major_minor_file)
        major_minor_df = pd.read_csv(major_minor_path, dtype={"trade_date": str}).set_index("trade_date")
        manager_major_minor[instrument] = major_minor_df
    return manager_major_minor


def load_md(instruments: list[str], md_dir: str) -> dict[str, pd.DataFrame]:
    manager_md = {}
    for instrument in instruments:
        md_file = f"{instrument}.md.close.csv.gz"
        md_path = os.path.join(md_dir, md_file)
        md_df = pd.read_csv(md_path, dtype={"trade_date": str}).set_index("trade_date")
        manager_md[instrument] = md_df
    return manager_md


def get_reader(db_name: str, db_dir: str) -> CManagerLibReader:
    db_reader = CManagerLibReader(db_dir, db_name)
    db_reader.set_default("MD")
    return db_reader


def test_f3(pairs: list[tuple[str, str, str]], mgr_md: dict[str, pd.DataFrame]):
    res = []
    for trade_date, instrument, contract in pairs:
        prc = mgr_md[instrument].at[trade_date, contract]
        res.append(prc)
    return res


def test_f2(pairs: list[tuple[str, str]], db_reader: CManagerLibReader):
    res = []
    for trade_date, contract in pairs:
        df = db_reader.read_by_conditions(t_conditions=[
            ("trade_date", "=", trade_date),
            ("loc_id", "=", contract),
        ], t_value_columns=["close"])
        prc = df["close"].iloc[0]
        res.append(prc)
    return res


def get_trade_date_and_contract_pair(size: int, dates: list[str], instruments: list[str], manager_major_minor: dict[str, pd.DataFrame]) -> (list[tuple[str, str]], list[tuple[str, str, str]]):
    n, m = len(dates), len(instruments)
    idx_date = np.random.randint(0, n, size=size)
    idx_inst = np.random.randint(0, m, size=size)
    pairs2, pairs3 = [], []
    for i0, i1 in zip(idx_date, idx_inst):
        trade_date = dates[i0]
        instrument = instruments[i1]
        pairs2.append((
            trade_date,
            manager_major_minor[instrument].at[trade_date, "n_contract"]
        ))
        pairs3.append((
            trade_date,
            instrument,
            manager_major_minor[instrument].at[trade_date, "n_contract"]
        ))
    return pairs2, pairs3


if __name__ == "__main__":
    test_calendar_path = "E:\\Deploy\\Data\\Calendar\\cne_calendar.csv"
    test_major_minor_dir = "E:\\Deploy\\Data\\Futures\\by_instrument\\major_minor"
    test_bgn_date, test_stp_date = "20160101", "20230701"
    test_instruments = ["RB.SHF", "AU.SHF", "CU.SHF",
                        "Y.DCE", "I.DCE", "PP.DCE",
                        "MA.CZC", "TA.CZC",
                        "CF.CZC", "SR.CZC"]
    test_size = 1000

    test_dates = get_dates(test_calendar_path, test_bgn_date, test_stp_date)
    mgr_major_minor = load_major_minor_data(test_instruments, test_major_minor_dir)
    p2, p3 = get_trade_date_and_contract_pair(test_size, test_dates, test_instruments, mgr_major_minor)

    t0 = dt.datetime.now()
    test_md_reader = get_reader("md.db", "E:\\Deploy\\Data\\Futures\\md")
    res2 = test_f2(pairs=p2, db_reader=test_md_reader)

    t1 = dt.datetime.now()
    test_mgr_md = load_md(test_instruments, "E:\\Deploy\\Data\\Futures\\by_instrument\\md_by_instru")
    res3 = test_f3(pairs=p3, mgr_md=test_mgr_md)

    t2 = dt.datetime.now()

    print(pd.DataFrame({"SQL": res2, "CSV": res3}))
    print(f"SQL time consuming = {(t1 - t0).total_seconds():.2f} seconds")
    print(f"CSV time consuming = {(t2 - t1).total_seconds():.2f} seconds")
