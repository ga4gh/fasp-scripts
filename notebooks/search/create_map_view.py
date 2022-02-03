'''
Create a view with harmonized data from metadata stored in a map.
Additional data can be harmonized by creating a map.
The generated views can be queried via Data Connect.
'''

#  IMPORTS
from google.cloud import bigquery

client = bigquery.Client()


# Build the union query
query_job = client.query("""SELECT t.table_version_id tv,
  bq_dataset_name, t.table_name, v.column_name,
map_id
, from_scheme
, to_scheme
,map_type
,formula
FROM metadata.mapping m,
metadata.s_variable v,
metadata.s_table t,
metadata.s_study s
where map_id  between 1200 and 1299
and from_scheme = v.variable_id
and t.table_version_id = v.table_version_id
and s.study_version_id = t.study_version_id""")

results = query_job.result()
viewSQL = ""
firstSeLect = True
for row in results:
    print("{} : {} : {} : {} ".format(row.tv,row.bq_dataset_name,row.table_name, row.column_name))
    rSelect = "SELECT '"+row.bq_dataset_name+"' Source, dbGaP_Subject_ID, "+row.column_name
    rSelect  += "+5"
    rSelect  += " "+ row.to_scheme + " FROM isbcgc-216220."+row.bq_dataset_name+"."+row.table_name
    if firstSeLect:
    	firstSeLect = False
    else:
    	viewSQL += " union all "
    viewSQL += rSelect
    
print (viewSQL)

# Create the view
dataset_ref = client.dataset('mapped')
view_ref = dataset_ref.table("age_years")
view = bigquery.Table(view_ref)
view.view_query = viewSQL
view = client.create_table(view)  # API request

print("Successfully created view at {}".format(view.full_table_id))

    


	
	

	
	









