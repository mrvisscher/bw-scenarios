import pandas as pd
from bw2data.backends import sqlite3_lci_db, ExchangeDataset
import bw2data as bd
import sqlite3
from utils import time_it

joined_exchanges = pd.DataFrame()


@time_it
def get_joined_exchanges() -> pd.DataFrame:
    # simulate a cache
    global joined_exchanges
    if not joined_exchanges.empty: return joined_exchanges

    sql_txt = """
    SELECT e.id AS exc_id, e.type AS exc_type, e.output_database as out_db, a.id AS in_id, b.id AS out_id
    FROM exchangedataset as e
    INNER JOIN activitydataset as a ON a.code = e.input_code AND a.database = e.input_database
    INNER JOIN activitydataset as b ON b.code = e.output_code AND b.database = e.output_database
    """
    connection = sqlite3.connect(sqlite3_lci_db._filepath)
    types = {"exc_id": int, "exc_type": str, "in_id": int, "out_id": int, "out_db": str}
    df = pd.read_sql_query(sql_txt, connection, index_col="exc_id", dtype=types)

    joined_exchanges = df

    return df

@time_it
def get_sibling_mapping() -> pd.DataFrame:
    df = get_joined_exchanges()

    df["combine"] = df["in_id"].astype(str) + "-" + df["out_id"].astype(str)

    cnts = df["combine"].value_counts()
    df["unique"] = df["combine"].map(cnts)
    df = df.drop(df[df.unique == 1].index)

    mapping = []
    exchange_data = pd.DataFrame(ExchangeDataset.select(ExchangeDataset.id, ExchangeDataset.data).where(ExchangeDataset.id << df.index.tolist()).dicts()).set_index("id")
    for exchange_id, row in df.iterrows():
        siblings = df.loc[(df["combine"] == row["combine"]) & (df.index != exchange_id)]

        for sibling_id, sibling_row in siblings.iterrows():
            data = exchange_data.loc[exchange_id, "data"]
            new_row = {
                "exc_id": exchange_id,
                "sibling_id": sibling_id,
                "amount": data["amount"]
            }
            mapping.append(new_row)

    mapping = pd.DataFrame(mapping)
    return mapping


if __name__ == "__main__":
    bd.projects.set_current("huge")
    print(get_sibling_mapping())
