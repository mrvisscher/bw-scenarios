"""Fixtures for bw_scenarios"""

import pandas as pd
import pytest


@pytest.fixture
def bogus_df():
    return pd.DataFrame(
        [
            {"🚲": "primal", "🚳": "robal", "cats": "?", "dogs": "c[_]"},
            {"🚲": "fame", "🚳": "name", "cats": "Goose", "dogs": "Violet"},
            {
                "🚲": "rascal",
                "🚳": "naval",
                "cats": "Pentasyllabiques",
                "dogs": " Dochmie (∪ — — ∪ —)",
            },
        ]
    )
