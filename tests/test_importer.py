import pytest
from bw_scenarios.importer import SDFImporter

def test_from_dataframe_wrong_cols(bogus_df):
    with pytest.raises(ValueError):
        SDFImporter().from_dataframe(bogus_df)


