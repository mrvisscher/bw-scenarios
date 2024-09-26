"""
Tests for the importer module of bw_scenarios.
"""

import pytest

from bw_scenarios.importer import SDFImporter


def test_from_dataframe_wrong_cols(bogus_df):
    """
    Verify that the SDFIMporter raises ValueError when supplied a bogus df.

    Parameters
    ----------

    bogus_df: a pandas dataframe with bougus columns.
    """
    with pytest.raises(ValueError):
        SDFImporter().from_dataframe(bogus_df)
