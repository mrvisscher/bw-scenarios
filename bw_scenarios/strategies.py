import pandas as pd


def separate_code_from_key(data: pd.DataFrame) -> pd.DataFrame:
    data["from code"] = data["from key"].apply(lambda key: eval(key)[1])
    data["to code"] = data["to key"].apply(lambda key: eval(key)[1])
    return data


def link_scenario_on_keys(data):
    """Link scenario entries based on the database, code tuple"""
    return data


def link_scenario_on_fields(data):
    """"Link scenario entries based on the fields"""
    return data


def replace_field(data, field: str, value, filter_fn=lambda old_value: True):
    """Replace a specific field, value combination"""
    return data


def check_exchange_number(data, except_on_mismatch=True):
    """Check whether the number of Scenario Exchanges matches the number of exchanges in the linked activity"""
    return data
