import os.path
import sys

current = os.path.abspath(os.path.split(__file__)[0])
print(f"Appending {current} to library path")
sys.path.append(current)
