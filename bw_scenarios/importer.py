from .scenario import Scenario

import pandas as pd
from typing import Optional, Union
from os import PathLike
from pathlib import Path


class SDFImporter:
    data: pd.DataFrame
    strategies: list

    TO_FIELDS = [
        "to activity name",
        "to reference product",
        "to location",
        "to database",
        "to categories",
        "to key",
    ]

    FROM_FIELDS = [
        "from activity name",
        "from reference product",
        "from location",
        "from categories",
        "from database",
        "from key",
        "flow type",
    ]

    def __init__(self):
        pass

    @classmethod
    def from_excel(cls, path: Union[str, PathLike]) -> "SDFImporter":
        """
        Read scenarios from an SDF in excel format
        """
        # check if the path is given in the correct format
        if not isinstance(path, (str, PathLike)):
            raise f"Path must be string or PathLike, but type is {type(path)}"

        df_data = pd.read_excel(path)

        return cls.from_dataframe(df_data)

    @classmethod
    def from_csv(
        cls, path: Union[str, PathLike], delimiter: Optional[str] = None
    ) -> "SDFImporter":
        """
        Read scenarios from an SDF in csv format

        """
        # check if the path is given in the correct format
        if not isinstance(path, (str, PathLike)):
            raise f"Path must be string or PathLike, but type is {type(path)}"

        # make sure we have a valid path format
        if isinstance(path, str):
            path = Path(path)

        # try to identify a delimiter if one wasn't given
        if not delimiter:
            with open(path) as file:
                line = file.readline()
                comma = line.find(",")
                semicol = line.find(";")
            if comma == -1 and semicol == -1:
                # neither a comma or semicolon were found, raise error
                raise (
                    "Delimiter not given and delimiter ',' or ';' not found. "
                    "Supply delimiter or ensure delimiter is ',' or ';'."
                )
            elif comma != -1 and comma < semicol:
                # comma exists and appears before semicolon
                delimiter = ","
            elif semicol != -1 and semicol < comma:
                # semicolon exists and appears before comma
                delimiter = ","

        df_data = pd.read_csv(path, delimiter=delimiter)

        return cls.from_dataframe(df_data)

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "SDFImporter":
        """
        Parse the SDF input data from a dataframe that is read in either from a csv or excel file into a nested dictionary.
        Stores the nested dictionary in the data attribute of the class.
        """

        # check if the dataframe contains the expected columns
        expected_columns = [
            "from activity name",
            "from reference product",
            "from location",
            "from categories",
            "from database",
            "from key",
            "to activity name",
            "to reference product",
            "to location",
            "to categories",
            "to database",
            "to key",
            "flow type",
        ]

        if not all([col in df.columns for col in expected_columns]):
            print(
                "Warning: the dataframe does not contain the expected columns: {}".format(
                    expected_columns
                )
            )

        df["from id"] = None
        df["to id"] = None

        importer = cls()
        importer.data = df
        return importer

    @property
    def unlinked(self) -> list:


        return []

    def apply_strategies(self):
        """Apply all data mutation strategies to scenarios"""
        pass

    def apply_strategy(self, strategy):
        """Apply a data mutation strategy to scenarios"""
        pass

    def to_datapackage(self):
        """Process all data into a datapackage"""
        pass

    def write(self):
        if self.unlinked:
            raise Exception("Cannot write unlinked scenarios")

        scenarios = {}

        for to_act in self.data.values():
            for exc in to_act["exchanges"]:
                for scenario, value in exc["values"].items():

                    if scenario not in scenarios:
                        scenarios[scenario] = {}

                    if not scenarios[scenario][to_act["id"]]:
                        scenarios[scenario][to_act["id"]] = []

                    scenarios[scenario][to_act["id"]].append((to_act["id"], value, to_act["flow type"]))

