import pickle
import random
import bw2data as bd
import pandas as pd
from typing import List

from sibling_mapping import get_sibling_mapping, get_joined_exchanges
from utils import time_it


@time_it
def dataframe_flow_iterator(df: pd.DataFrame, types: List[str] = None):
    for exc_id, row in df.iterrows():
        if types and row["exc_type"] not in types: continue
        yield {
            "amount": row["amount"],
            "row": row["in_id"],
            "col": row["out_id"],
            "flip": True if row["exc_type"] in ('technosphere', 'generic consumption') else False
        }


@time_it
def build_sibling_df(scenario_dict) -> pd.DataFrame:
    mapping = get_sibling_mapping()
    mapping = mapping.drop(mapping[(mapping.amount == 0) |
                                   (~mapping.sibling_id.isin(scenario_dict.keys())) |
                                   (mapping.exc_id.isin(scenario_dict.keys()))].index)

    mapping = mapping.drop(columns=['sibling_id'])
    mapping = mapping.drop_duplicates()
    mapping = mapping.set_index("exc_id")

    mapping = mapping.join(get_joined_exchanges(), how="left")

    return mapping


@time_it
def build_scenario_df(scenario_dict) -> pd.DataFrame:
    scenario_df = pd.DataFrame.from_dict(scenario_dict, "index", columns=["amount"])
    scenario_df = scenario_df.join(get_joined_exchanges(), how="left")

    return scenario_df


@time_it
def open_test_scenario() -> dict:
    with open('ids.pickle', 'rb') as file:
        return {exc_id: random.random() for exc_id in pickle.load(file)}


if __name__ == "__main__":
    bd.projects.set_current("prospective")
    scenarios_dict = open_test_scenario()

    scenario_df = build_scenario_df(scenarios_dict)
    sibling_df = build_sibling_df(scenarios_dict)

    list(dataframe_flow_iterator(scenario_df))
    list(dataframe_flow_iterator(sibling_df))


