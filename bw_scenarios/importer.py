from .scenario import Scenario


class SDFImporter:
    data: dict
    strategies: list

    def __init__(self):
        pass

    @classmethod
    def from_excel(cls, path) -> "SDFImporter":
        """Read scenarios from an SDF in excel format"""
        pass

    @classmethod
    def from_csv(cls, path) -> "SDFImporter":
        """Read scenarios from an SDF in csv format"""
        pass

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


