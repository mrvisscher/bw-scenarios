from bw2data.data_store import ProcessedDataStore

from .meta import scenarios


class Scenario(ProcessedDataStore):
    """
    {
        act.id: [
            (act.id, type, amount),
        ]
    }

    """
    _metadata = scenarios
    pass
