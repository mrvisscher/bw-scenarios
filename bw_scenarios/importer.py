from .scenario import Scenario

from pandas import pd
from typing import Optional, Union
from os import PathLike
import os


class SDFImporter:
    data: dict
    strategies: list

    def __init__(self):
        pass

    @classmethod
    def from_excel(cls, path: Union[str, PathLike]) -> "SDFImporter":
        """Read scenarios from an SDF in excel format"""
        # check if the path is given in the correct format
        if not isinstance(path, (str, PathLike)):
            raise f"Path must be string or PathLike, but type is {type(path)}"

        df_data = pd.read_excel(path)

    @classmethod
    def from_csv(cls, path: Union[str, PathLike], delimiter: Optional[str] = None) -> "SDFImporter":
        """Read scenarios from an SDF in csv format"""
        # check if the path is given in the correct format
        if not isinstance(path, (str, PathLike)):
            raise f"Path must be string or PathLike, but type is {type(path)}"

        # make sure we have a valid path format
        if isinstance(path, str):
            path = os.path(path)

        # try to identify a delimiter if one wasn't given
        if not delimiter:
            with open(path) as file:
                line = file.readline()
                comma = line.find(",")
                semicol = line.find(";")
            if comma == -1 and semicol == -1:
                # neither a comma or semicolon were found, raise error
                raise ("Delimiter not given and delimiter ',' or ';' not found. "
                       "Supply delimiter or ensure delimiter is ',' or ';'.")
            elif comma != -1 and comma < semicol:
                # comma exists and appears before semicolon
                delimiter = ","
            elif semicol != -1 and semicol < comma:
                # semicolon exists and appears before comma
                delimiter = ","

        df_data = pd.read_csv(path, delimiter=delimiter)


    @property
    def unlinked(self) -> list:
        return []

    @property
    def linked(self) -> [Scenario]:
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


