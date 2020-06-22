"""Test module `test_analyze`."""

import pandas as pd
from psa_prizes.analyze import _str_comp_ann_g


def test_str_comp_ann_g() -> None:
    """Test a pd.DataFrame with 100% CAGR, missing and multiple entries per year."""
    data = {
        "date": ["10/06/2010", "10/06/2011", "10/06/2011", "10/06/2013", "10/06/2015"],
        "prize": [1, 2, 2, 2 ** 3, 2 ** 5],
    }
    df = pd.DataFrame(data, columns=["date", "prize"])
    df["year"] = pd.DatetimeIndex(df["date"]).year
    msg = (
        f"– The compound annual growth rate from {min(df.year)} "
        f"to {max(df.year)} is 100.0%."
    )
    assert msg == _str_comp_ann_g(df)
