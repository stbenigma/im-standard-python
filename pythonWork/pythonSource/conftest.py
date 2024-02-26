import os.path
import sys

def pytest_addoption(parser):
    parser.addoption('--scan-repos', action='store_true', dest="nocoverage",
                     default=False, help="dont inside coverage runs")

def pytest_configure(config):
    if not config.option.nocoverage:
        setattr(config.option, 'markexpr', 'not nocoverage')

current = os.path.abspath(os.path.split(__file__)[0])
print(f"Appending {current} to library path")
sys.path.append(current)
