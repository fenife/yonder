#!/usr/bin/env python3

"""
move data from old data to new db
"""


import os
import sys

project_path = os.path.abspath(os.path.join(os.path.dirname(__name__), '..'))
print(f"project_path: {project_path}")

sim_path = os.path.abspath(os.path.join(project_path, 'server_py3', 'sim'))
print(f"sim_path: {sim_path}")

app_path = os.path.abspath(os.path.join(project_path, 'server_py3', 'web'))
print(f"app_path: {app_path}")

sys.path.append(sim_path)
sys.path.append(app_path)

from web import db as new_db
from sim.norm import Database


old_db = Database()
old_db.init_config(
    host='127.0.0.1',
    port=3306,
    user='test',
    password='test',
    db_name='yonder'
)


def main():
    print(old_db, new_db)


if __name__ == "__main__":
    main()

