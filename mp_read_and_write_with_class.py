import sys
import os
import datetime as dt
import multiprocessing as mp
import numpy as np
import pandas as pd
from skyrim.falkreath import CManagerLibWriter, CTable, CManagerLibReader


class CLib(object):
    def __init__(self, src_db_dir: str, src_db_name: str):
        self.src_db_dir = src_db_dir
        self.src_db_name = src_db_name

    def _read_df(self, table_name: str):
        db_reader = CManagerLibReader(t_db_save_dir=self.src_db_dir, t_db_name=self.src_db_name)
        df = db_reader.read(
            t_value_columns=["trade_date", "val"],
            t_table_name=table_name, t_using_default_table=False)
        # print(df.tail())
        return df

    def _write_df(self, table: CTable, b: int, s: int, task: int):
        i = 0
        while i < task:
            i += 1

        db_writer = CManagerLibWriter(t_db_save_dir=self.src_db_dir, t_db_name=self.src_db_name)
        db_writer.initialize_table(t_table=table, t_remove_existence=False, t_set_as_default=True)
        new_dates = [f"T{_:03d}" for _ in range(b, s)]
        new_df = pd.DataFrame({"trade_date": new_dates, "value": np.random.random(s - b)})
        db_writer.update(t_update_df=new_df, t_using_index=False)
        db_writer.close()
        return 0

    def read_df_mp(self, proc_num: int, table_names: list[str]):
        t0 = dt.datetime.now()
        pool = mp.Pool(processes=proc_num)
        for p in table_names:
            pool.apply_async(self._read_df, args=(p,))
        pool.close()
        pool.join()
        t1 = dt.datetime.now()
        print("... total time consuming: {:.2f} seconds for Reading".format((t1 - t0).total_seconds()))
        return 0

    def write_df_mp(self, proc_num: int, tables: list[CTable], b: int, s: int, task: int):
        t0 = dt.datetime.now()
        pool = mp.Pool(processes=proc_num)
        for p in tables:
            pool.apply_async(self._write_df, args=(p, b, s, task))
        pool.close()
        pool.join()
        t1 = dt.datetime.now()
        print("... total time consuming: {:.2f} seconds for Writing".format((t1 - t0).total_seconds()))
        return 0

    def write_df_linear(self, tables: list[CTable], b: int, s: int, task: int):
        t0 = dt.datetime.now()
        for p in tables:
            self._write_df(p, b, s, task)
        t1 = dt.datetime.now()
        print("... total time consuming: {:.2f} seconds for Writing".format((t1 - t0).total_seconds()))
        return 0


if __name__ == "__main__":
    n = 500
    m = 1000
    k = 50
    db_name = "test.db"
    task = int(sys.argv[1])

    trade_dates = [f"T{_:04d}" for _ in range(n)]
    test_tables = [
        CTable(t_table_struct={"table_name": f"TAB{_:02d}", "primary_keys": {"trade_date": "TEXT"}, "value_columns": {"val": "REAL"}})
        for _ in range(k)]
    test_table_names = [f"TAB{_:02d}" for _ in range(k)]

    # init lib
    os.remove(db_name)
    db = CManagerLibWriter(t_db_save_dir=".", t_db_name=db_name)
    db.initialize_tables(t_tables=test_tables, t_remove_existence=True)
    for tab_name in test_table_names:
        db.update(
            t_update_df=pd.DataFrame({"trade_date": trade_dates, "value": np.random.random(n)}),
            t_using_index=False,
            t_using_default_table=False,
            t_table_name=tab_name,
        )
    db.close()

    # main test
    test_lib = CLib(src_db_dir=".", src_db_name=db_name)
    test_lib.read_df_mp(proc_num=5, table_names=["ta", "tb", "tc"])
    test_lib.write_df_mp(proc_num=5, tables=test_tables, b=n, s=n + m, task=task)
    # test_lib.write_df_linear(tables=test_tables, b=n, s=n + m, task=task)
    test_lib.read_df_mp(proc_num=5, table_names=["ta", "tb", "tc"])
