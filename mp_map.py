from multiprocessing import Pool
from skyrim.falkreath import CManagerLibReader


def add_one(number):
    return number + 1


def read_df(arg_comb):
    table_name, src_db_dir, src_db_name = arg_comb
    db_reader = CManagerLibReader(t_db_save_dir=src_db_dir, t_db_name=src_db_name)
    df = db_reader.read(
        t_value_columns=["trade_date", "val"],
        t_table_name=table_name, t_using_default_table=False)
    db_reader.close()
    print(df)
    return table_name


if __name__ == "__main__":
    process_pool = Pool(2)
    table_names = [(f"TAB{_:02d}", ".", "test.db") for _ in range(5)]
    res = process_pool.map(read_df, table_names)
    process_pool.close()
    process_pool.join()
    print(res)
