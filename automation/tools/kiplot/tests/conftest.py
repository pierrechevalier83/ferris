"""
Test configuration
"""


def pytest_addoption(parser):
    parser.addoption("--plot_dir", action="store", default=None,
                     help="the plot dir to use (omit to use a temp dir). "
                     "If given, plots will _not_ be cleared after testing.")
