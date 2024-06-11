import bw_processing as bp
import bw2data as bd
import itertools
from fs.zipfs import ZipFS
from bw2data.data_store import ProcessedDataStore
from bw2data.serialization import PickledDict

from process import open_test_scenario, build_scenario_df, build_sibling_df, dataframe_flow_iterator
from sibling_mapping import get_joined_exchanges
from utils import time_it


class Scenarios(PickledDict):
    filename = "scenarios.pickle"


scenarios = Scenarios()


class Scenario(ProcessedDataStore):
    _metadata = scenarios
    _matrices = ["technosphere_matrix", "biosphere_matrix"]

    def get_dependents(self):
        excs = get_joined_exchanges()

    @time_it
    def process(self, **extra_metadata):
        data = self.load()

        scenario_df = build_scenario_df(data)
        sibling_df = build_sibling_df(data)

        dp = bp.create_datapackage(
            fs=ZipFS(str(self.filepath_processed()), write=True),
            name=self.filename_processed(),
            sum_intra_duplicates=True,
            sum_inter_duplicates=False,
        )

        dp.add_persistent_vector_from_iterator(
            matrix="biosphere_matrix",
            name=bp.clean_datapackage_name(self.name + " biosphere matrix"),
            dict_iterator=itertools.chain(
                dataframe_flow_iterator(scenario_df, types=["biosphere"]),
                dataframe_flow_iterator(sibling_df, types=["biosphere"]),
            ),
        )

        tech_types = ['production', 'substitution', 'generic production', 'technosphere', 'generic consumption']

        dp.add_persistent_vector_from_iterator(
            matrix="technosphere_matrix",
            name=bp.clean_datapackage_name(self.name + " technosphere matrix"),
            dict_iterator=itertools.chain(
                dataframe_flow_iterator(scenario_df, types=tech_types),
                dataframe_flow_iterator(sibling_df, types=tech_types),
            ),
        )

        dp.finalize_serialization()


if __name__ == "__main__":
    bd.projects.set_current("prospective")

    scenario_0 = Scenario("scenario_0")
    scenario_0.write(open_test_scenario())
    scenario_0.process()

print("test")
