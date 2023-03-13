import os
import json


file_path = os.path.join(
                    os.path.dirname(__file__), 
                    'seeds.json'
                    )
seeds_file = open(file_path, 'r')
SEEDS = json.load(seeds_file)
seeds_file.close()


def init_table(target, connection, **kw):
    tablename = str(target)
    print(f"Seeding {tablename} with data")
    if tablename in SEEDS and len(SEEDS[tablename]) > 0:
        for entry in SEEDS[tablename]:
            connection.execute(target.insert(), entry)