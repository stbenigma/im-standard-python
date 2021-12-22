import os.path
import sys

current = os.path.abspath(os.path.split(__file__)[0])
print(f"Appending {current} to library path")
sys.path.append(current)

IM_DB_path = os.path.join(current, 'IM_db')
print(f"Appending {IM_DB_path} to library path")
sys.path.append(IM_DB_path)
