
from fasp.search import DiscoverySearchClient

def main():

    searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com')
    query = """SELECT sample_submitter_id, fileid, filename 
    FROM dbgap_demo.scr_ega.scr_egapancreatic_sample_multi p 
    join dbgap_demo.scr_ega.scr_egapancreatic_files f on f.sample_primary_id = p.sample_primary_id 
    where phenotype = 'pancreatic adenocarcinoma' limit 3"""
    query_job = searchClient.runQuery(query)
    
    for row in query_job:

        print("sample={}, EGAFileID={}".format(row[0], row[1]))
                
    
if __name__ == "__main__":
    main()
    