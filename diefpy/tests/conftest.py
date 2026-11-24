import matplotlib

matplotlib.use('Agg')  # never open windows while running the tests

import matplotlib.pyplot as plt  # noqa: E402
import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def close_figures():
    """Close all figures after each test to not leak memory between tests."""
    yield
    plt.close('all')
