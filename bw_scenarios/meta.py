from bw2data.serialization import SerializedDict
from bw2data.configuration import config

class Scenarios(SerializedDict):
    filename = "scenarios.json"

    def serialize(self, filepath=None):
        super().serialize(filepath)


scenarios = Scenarios()

config.metadata.extend([scenarios])
