from typing import Union, Iterable

import pandas as pd
import numpy as np

import bw2data as bd
from bw2data.errors import UnknownObject


def separate_keys(data: pd.DataFrame) -> pd.DataFrame:
    """
    Splits the key fields up into database and code fields. Overwrites existing values. Removes the key fields.
    """

    def parse(key):
        try:
            return pd.Series(eval(key))
        except Exception as e:
            return pd.Series((None, None, ))

    data[["from database", "from code"]] = data["from key"].apply(parse)
    data[["to database", "to code"]] = data["to key"].apply(parse)

    data.drop(columns=["from key", "to key"], inplace=True)

    return data


def replace_field(data: pd.DataFrame, field: Union[str, Iterable[str]], replace: dict) -> pd.DataFrame:
    """Replace a specific values in a field or set of fields with a new value.

    field: a str or iterable of str that are the fields that values should be replaced in
    replace: a dict of items to replace with the values to replace them with
    """
    if isinstance(field, str):
        to_replace = {field: replace}
    else:
        to_replace = {f: replace for f in field}
    return data.replace(to_replace=to_replace)


def link_scenario_on_keys(data: pd.DataFrame, relink=False) -> pd.DataFrame:
    """Link scenario entries based on the database, code tuple"""
    from_set = set([tuple(x) for x in data[['from database', 'from code']].values])
    [from_set.add(tuple(x)) for x in data[['to database', 'to code']].values]

    id_mapping = {}
    for key in from_set:
        try:
            id_mapping[key] = bd.get_id(key)
        except UnknownObject:
            id_mapping[key] = None

    for index, from_db, from_code, to_db, to_code in data[["from database", "from code", "to database", "to code"]].itertuples():
        if pd.isna(data.loc[index, "from id"]) or relink:
            data.loc[index, "from id"] = id_mapping[(from_db, from_code)]

        if pd.isna(data.loc[index, "to id"]) or relink:
            data.loc[index, "to id"] = id_mapping[(to_db, to_code)]

    return data


def link_scenario_on_fields(data: pd.DataFrame) -> pd.DataFrame:
    """Link scenario entries based on the fields"""
    return data


def check_exchange_number(data: pd.DataFrame, except_on_mismatch=True) -> pd.DataFrame:
    """Check whether the number of Scenario Exchanges matches the number of exchanges in the linked activity"""
    raise NotImplementedError("We acknowledge that this is an issue and will deal with this later")
