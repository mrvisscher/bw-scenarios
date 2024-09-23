from typing import Union, Iterable

import pandas as pd

def separate_code_from_key(data: pd.DataFrame) -> pd.DataFrame:
    data["from code"] = data["from key"].apply(lambda key: eval(key)[1])
    data["to code"] = data["to key"].apply(lambda key: eval(key)[1])
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


def link_scenario_on_keys(data: pd.DataFrame) -> pd.DataFrame:
    """Link scenario entries based on the database, code tuple"""
    return data


def link_scenario_on_fields(data: pd.DataFrame) -> pd.DataFrame:
    """"Link scenario entries based on the fields"""
    return data


def check_exchange_number(data: pd.DataFrame, except_on_mismatch=True) -> pd.DataFrame:
    """Check whether the number of Scenario Exchanges matches the number of exchanges in the linked activity"""
    return data
