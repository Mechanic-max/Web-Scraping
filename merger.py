
import pandas
csv1 = pandas.read_csv('Franklin_results_details_formatted (1).csv')
csv2 = pandas.read_csv('final_dataset_for_franklin.csv')
merged = csv1.merge(csv2, on='decedent address')
merged.to_csv("output.csv", index=False)