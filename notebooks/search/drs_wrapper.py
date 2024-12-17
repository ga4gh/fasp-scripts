import requests
import os
import time
from datetime import datetime
import json
from fasp.loc import sbcgcDRSClient
import pandas as pd

class DRSWrapper:

    def __init__(self,  api_key_path='~/.keys/sbcgc_key.json', 
                query_log = None):

        self.query_log = query_log
        self.drs_client = sbcgcDRSClient(api_key_path='~/.keys/sbcgc_key.json', access_id='s3')
        
        with open("data/dataset_drs_ids.json") as f:
            self.dataset_drs_ids = json.load(f)


    def drs_download(self, dataset, file_path):
        t_start = time.perf_counter()
        drs_id = self.dataset_drs_ids[dataset]
        fileDetails = self.drs_client.get_object(drs_id)
        url = self.drs_client.get_access_url(drs_id)
        #file_path = './data/' + fileDetails['name']
        with open(os.path.expanduser(file_path), "wb") as file:
            response = requests.get(url)
            file.write(response.content)
        t_end = time.perf_counter()
        elapsed = t_end - t_start
        stats =   {
          "time": datetime.now().isoformat(),
          "server": self.drs_client.api_url_base,
          "method": "drs",
          "query": f"/object/{drs_id}/access/{'s3'}",
          "dataset": dataset,
          "bytes": fileDetails['size'],
          "elapsed_secs": float(f"{elapsed:0.4f}")
        }
        self.__write_log(stats)

        print(f"Bytes downloaded: {stats['bytes']}")
        print(f"Time elapsed: {stats['elapsed_secs']} seconds")
        #df = pd.read_csv(file_path, sep='\t')
        return

    def __write_log(self, stats_dict):
        print ("writing log")
        try:
            with open(self.query_log) as f:
                query_stats = json.load(f)
        except FileNotFoundError:
            query_stats = []
        query_stats.append(stats_dict)
        with open(self.query_log, "w") as f:
            json.dump(query_stats, f, indent=3)