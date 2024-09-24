from bw2data.data_store import ProcessedDataStore
from bw2calc.lca import prepare_lca_inputs
import bw_processing as bwp
import numpy as np
from bw2data.errors import UnknownObject

from .meta import scenarios


class Scenario(ProcessedDataStore):
    """
    Scenario Datastore containing all the exchanges modified for the scenario

    ...

    Attributes
    ----------
    exchanges: dict
        Dictionary of exchanges modified for the scenario in the following format:
        {
            to_activity_id: [
                (from_activity_id, type, amount),
            ]
        }
    dp_static: bw_processing.DataPackage
    """
    _metadata = scenarios

    def __init__(self, name: str):
        super().__init__(name)

        self.dp_static = bwp.create_datapackage()  # tdb if static is correct

        try:
            self.exchanges = self.load()
        except UnknownObject:
            self.exchanges = {}

    def get_arrays_for_datapackage(self, matrix_name):
        """
        prepare the input to the datapackges (indices, data and flip array)

        matrix_name: str
            name of the matrix (technosphere or biosphere)

        """
        t_indices = []
        t_data = []
        t_flip = []

        if matrix_name == "technosphere":
            for to_act_id, exchanges_info in self.exchanges.items():
                for from_act_id, exc_type, amount in exchanges_info:
                    if (
                        exc_type == "biosphere"
                    ):  # skip biosphere exchanges, but keep going for technosphere and production exchanges
                        continue

                    t_indices.append((from_act_id, to_act_id))
                    t_data.append(amount)
                    if exc_type == "technosphere":
                        t_flip.append(True)
                    else:
                        t_flip.append(False)

        if matrix_name == "biosphere":
            for to_act_id, exchanges_info in self.exchanges.items():
                for from_act_id, exc_type, amount in exchanges_info:
                    if (
                        exc_type == "biosphere"
                    ):  # there is only one type of biosphere exchanges

                        t_indices.append((from_act_id, to_act_id))
                        t_data.append(amount)
            t_flip = None  # no sign flipping needed for biosphere exchanges

        return (
            np.array(t_indices, dtype=bwp.INDICES_DTYPE),
            np.array(t_data),
            np.array(t_flip),
        )

    def add_datapackage(self):
        """
        build biosphere and technosphere datapackages for the scenario
        """

        t_indices, t_data, t_flip = self.get_arrays_for_datapackage("technosphere")
        b_indices, b_data, _ = self.get_arrays_for_datapackage("biosphere")

        self.dp_static.add_persistent_vector(
            matrix="technosphere_matrix",
            indices_array=t_indices,
            data_array=t_data,
            flip_array=t_flip,
        )

        self.dp_static.add_persistent_vector(
            matrix="biosphere_matrix",
            indices_array=b_indices,
            data_array=b_data,
        )

    def add_exchange(self, from_id: int, to_id: int, exchange_type: str, amount: float):
        """
        Adds an exchange to the scenario

        Parameters
        ----------
        from_id: int
            Activity id of the activity the exchange originates from
        to_id: int
            Activity id of the activity the exchanges flows to
        exchange_type: str
            Type of the exchange, e.g. "biosphere" or "technosphere"
        amount: float
            Amount value of the exchange
        """
        from_act = self.exchanges.get(to_id, [])
        from_act.append((from_id, exchange_type, amount))
        self.exchanges[to_id] = from_act

    def save(self):
        """
        Save the scenario by writing all it's exchanges to disk
        """
        self.write(self.exchanges)

    def process(self, **extra_metadata):
        return
