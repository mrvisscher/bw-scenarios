import pandas as pd
import brightway2 as bw
import pickle
from bw2data.backends.peewee import ExchangeDataset, ActivityDataset
from peewee import *

bw.projects.set_current("prospective")

with open('ids.pickle', 'rb') as file:
    # Read the serialized object and deserialize it
    ids = pickle.load(file)

print("IDS imported")


# q = ExchangeDataset.select().where(ExchangeDataset.id << ids)

# Alias for ActivityDataset to use in the joins
# ActivityDatasetAliasA = ActivityDataset.alias()
# ActivityDatasetAliasB = ActivityDataset.alias()
#
# # Perform the joins and select the required columns
# query = (ExchangeDataset
#          .select(ExchangeDataset.id.alias('exc_id'),
#                  ActivityDatasetAliasA.id.alias('in_id'),
#                  ActivityDatasetAliasB.id.alias('out_id'))
#          .join(ActivityDatasetAliasA,
#                join_type=JOIN.LEFT_OUTER,
#                on=((ActivityDatasetAliasA.code == ExchangeDataset.input_code) &
#                    (ActivityDatasetAliasA.database == ExchangeDataset.input_database)))
#          .switch(ExchangeDataset)
#          .join(ActivityDatasetAliasB,
#                join_type=JOIN.LEFT_OUTER,
#                on=((ActivityDatasetAliasB.code == ExchangeDataset.output_code) &
#                    (ActivityDatasetAliasB.database == ExchangeDataset.output_database))))
#
# df = pd.DataFrame(query.tuples())

for edge_id in ids:
    edge = ExchangeDataset.get_by_id(edge_id)
    q = ExchangeDataset.select().where(
        (ExchangeDataset.input_database == edge.input_database),
        (ExchangeDataset.input_code == edge.input_code),
        (ExchangeDataset.output_database == edge.output_database),
        (ExchangeDataset.output_code == edge.output_code)
    )
    if len(q) > 1: print("HIT")

print("check")


