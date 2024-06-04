import datetime as dt
import multiprocessing as mp
import numpy as np
import pandas as pd
from skyrim.falkreath import CManagerLibWriter, CTable, CManagerLibReader


def read_df(table_name: str, src_db_dir: str, src_db_name: str):
    db_reader = CManagerLibReader(t_db_save_dir=src_db_dir, t_db_name=src_db_name)
    df = db_reader.read(
        t_value_columns=["trade_date", "val"],
        t_table_name=table_name, t_using_default_table=False)
    db_reader.close()
    print(df)
    return df


def read_df_mp(proc_num: int, table_names: list[str], **kwargs):
    t0 = dt.datetime.now()
    pool = mp.Pool(processes=proc_num)
    for p in table_names:
        pool.apply_async(read_df, args=(p,), kwds=kwargs)
    pool.close()
    pool.join()
    t1 = dt.datetime.now()
    print("... total time consuming: {:.2f} seconds".format((t1 - t0).total_seconds()))
    return 0


if __name__ == "__main__":
    n = 24

    trade_dates = [f"T{_:03d}" for _ in range(n)]
    db_name = "test.db"
    db = CManagerLibWriter(t_db_save_dir=".", t_db_name=db_name)
    tables = [
        CTable(t_table_struct={"table_name": "ta", "primary_keys": {"trade_date": "TEXT"}, "value_columns": {"val": "REAL"}}),
        CTable(t_table_struct={"table_name": "tb", "primary_keys": {"trade_date": "TEXT"}, "value_columns": {"val": "REAL"}}),
        CTable(t_table_struct={"table_name": "tc", "primary_keys": {"trade_date": "TEXT"}, "value_columns": {"val": "REAL"}}),
    ]
    db.initialize_tables(
        t_tables=tables,
        t_remove_existence=True,
    )
    for tab_name in ["ta", "tb", "tc"]:
        db.update(
            t_update_df=pd.DataFrame({"trade_date": trade_dates, "value": np.random.random(n)}),
            t_using_index=False,
            t_using_default_table=False,
            t_table_name=tab_name,
        )
    db.close()

    read_df_mp(proc_num=3, table_names=["ta", "tb", "tc"], src_db_dir=".", src_db_name=db_name)
