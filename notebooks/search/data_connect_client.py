import requests
import sys
import getopt
import json
import time
from datetime import datetime
import os

import pandas as pd

class DataConnectClient:

    def __init__(self, hostURL, return_type=None, row_limit=10000, debug=False,
                query_log = None, passport = None):
        """Initialize a DataConnectClient

        Parameters:
        hostURL (str): base url of the Data Connect server to access
        return_type(str): default setting for how this client should return query results 'dataframe', 'json' or None.
        row_limit (int): limit the number of rows returned to the value given (default 10000)
        debug (boolean): whether to print debugging information during query runs (default False)
        query_log (str): file path for logging query statistics - use .json extension (default None)
        passport (str): file path for a file containing a passport or task specific token (default None)

        Returns:
        created client

        """  
        self.hostURL = self._url_format(hostURL)
        self.debug = debug
        self.return_type = return_type
        self.row_limit = row_limit
        self.query_log = query_log
        #self.passport = passport
        self.passport = self.__get_passport(passport)
        self.headers = {
            'content-type': 'application/json'
        }

    def __get_passport(self, passportFile=None):
        '''Adds Passport/TST to session header'''
        if passportFile != None:
            full_key_path = os.path.expanduser(passportFile)
            file_content = ""
            if self.debug: print(f"passport path {full_key_path}")
            try:
                with open(full_key_path) as f:
                    file_content = f.read()
                if self.debug: print(f"content of passport file {file_content}")
                return(file_content)
            except:
                print("Could not find passport file")
                return None
        else:
            return None
                
    def set_row_limit(self, row_limit):
        self.row_limit = row_limit

    def set_return_type(self, return_type):
        self.return_type = return_type

        # Look for registered search services
    @classmethod
    def getRegisteredSearchServices(cls):
        reg = GA4GHRegistryClient()
        services = reg.getRegisteredServices('org.ga4gh:search')
        for service in services:
            #serviceType=service['type']
            print(json.dumps(service, indent=3))
            #serviceURL = service['url']
            #hostname = serviceURL.split("/")[2]

        return None

    def _url_format(self, url):
        url = str(url)
        if url.endswith('/'):
            url = url[:-1]
        return url

    def list_tables(self, requestedCatalog=None, verbose=True):
        """List tables for a specified catalog

        Parameters:
        requestedCatalog (str): catalog to list or all tables if None (default None)
        verbose(boolean): Optionally print the list (default True)

        Returns:
        list of fully qualified table names as catalog.schema.table (list of str)

        """  

        tables = []

        if requestedCatalog == None:
            next_url = self.hostURL + "/tables"
        else:
            next_url = "{}{}{}".format(self.hostURL,'/tables/catalog/',requestedCatalog)

        pageCount = 0
        if verbose:
            print("Retrieving the table list")
        while next_url != None :
            pageCount += 1
            if verbose:
                print ("____Page{}_______________".format(pageCount))
            if self.debug:
                print(f'Retrieving {next_url}')
            response = requests.get(next_url, headers=self.headers)
            result = (response.json())
            if self.debug:
                print(json.dumps(result, indent=3))
            if requestedCatalog == None and 'pagination' in result and 'next_page_url' in result['pagination']:
                next_url = result['pagination']['next_page_url']
            else:
                next_url = None
            for t in result['tables']:
                if verbose:
                    print(t['name'])
                tables.append(t['name'])

        return tables

    def list_catalogs(self):
        """Prints list of catalogs available on the server"""
        url = self.hostURL + "/tables"

        print ("Retrieving the catalog list")
        response = requests.get(url, headers=self.headers)
        result = (response.json())
        for t in result['index']:
            print(t['description'])
        return


    def list_catalog(self, catalog):
        """List tables for a specified catalog

        Parameters:
        requestedCatalog (str): catalog to list or all tables if None (default None)

        Returns:
        list of fully qualified table names as catalog.schema.table (list of str)

        """  
        return self.list_tables(catalog)

    def list_table_info(self, table, verbose=False):
        """Obtain and optionally list the schema for a given table

        Parameters:
        table (str): table name
        verbose(boolean): Optionally print the list (default False)

        Returns:
        the table schema as a SearchSchema object

        """  
        url = "{}/table/{}/info".format(self.hostURL,table)
        response = requests.get(url, headers=self.headers)
        info = json.loads(response.text)
        if verbose:
            print ("_Schema for table{}_".format(table))
            print(json.dumps(info, indent=3))
        #return info
        return SearchSchema(info)

    def list_table_columns(self, table, descriptions=False, enums=False):
        """Print the columns in a table. More compact and practical for many purposes compared with list_table_info

        Parameters:
        table (str): table name
        descriptions(boolean): Include column descriptions (default False)
        enums(boolean): List the enumerated options/codes for categorical columns (default False)
        """  
        schema = self.list_table_info(table).schema
        if self.debug: print(json.dumps(schema, indent=3))
        for c, v in schema['data_model']['properties'].items():
            print (c)
            if descriptions:
                if 'description' in v: print (v['description'])
                if '$comment' in v: print (v['$comment'])
            if enums:
                if 'oneOf' in v:
                    for c in v['oneOf']:
                        print ('\t\t{}'.format(c['const']))
                if '$comment' in v: print (v['$comment'])
            print('_______________________________________')

    def list_column_info(self, table, verbose=False):
        """Obtain the table schema in JSON Schema format
        
        Parameters:
        table (str): table name
        verbose(boolean): Optionally print the schema (default False)

        Returns:
        the table schema as a JSON Schema

        """  
        url = "{}/table/{}/info".format(self.hostURL,table)
        response = requests.get(url, headers=self.headers)
        info = json.loads(response.text)
        if verbose:
            print ("_Schema for table{}_".format(table))
            print(json.dumps(info, indent=3))
        return info

    def get_mapping_template(self, table, propList=None):
        ''' Get an empty template in which to create  mappings for property values 
        :param table: table for which to generate a mapping template
        :param propList: optional list of properties to include in the map (default: all properties)
        
        :return the mapping template as a dictionary
        '''
        schema = self.list_table_info(table).schema
        template = {}
        for prop, details in schema['data_model']['properties'].items():
            if propList == None or prop in propList:
                if 'oneOf' in details:
                    vList = {}
                    for v in details['oneOf']:
                        vList[v['const']] = 'replaceThis'
                        #if titles:
                        #	vList[v['const']]['title'] = v['title']
                    template[prop] = vList
        return template


    def get_decode_template(self, table, propList=None, numericCodes=True):
        ''' Get a template which maps enumerated codes to their decoded values 
        :param table: table for which to generate a mapping template
        :param propList: optional list of properties to include in the map (default: all properties)
        :param numericCodes: return codes as integers - will fail if the codes are not (default True)
        
        :return the decoding template as a dictionary
        '''
        schema = self.list_table_info(table).schema
        template = {}
        for prop, details in schema['data_model']['properties'].items():
            if propList == None or prop in propList:
                if 'oneOf' in details:
                    vList = {}
                    for v in details['oneOf']:
                        if numericCodes:
                            vList[int(v['const'])] = v['title']
                        else:
                            vList[v['const']] = v['title']
                        #if titles:
                        #	vList[v['const']]['title'] = v['title']
                    template[prop] = vList
        return template


    def runOneTableQuery(self, column_list, table, limit):
        col_string = ", ".join(column_list)

        query = "select {columns} from {table} limit {results}".format(columns=col_string,
                                                                table=table, results=limit)
        res = self.run_query(query, return_type='dataframe')
        return res

    def getDataFrameFromTable(self, table, column_list=[], limit=1000):
        if isinstance(column_list, list):
            if len(column_list) == 0:
                column_list = '*'
            else:
                column_list.join(',')
        query = f"select {column_list} from {table} limit {limit}"
        print (query)
        res = self.run_query(query, return_type='dataframe')
        if res.shape[0] >= limit:
            print(f'The number of rows was limited to {limit}. Try setting limit=your_value if you need more data')
        return res

    def run_query(self, query, return_type=None, progessIndicator=None, query_tags=None):
        """Run an SQL query against tables available on the server and return all results. The function will 
        indicate progress as multiple pages of results are returned.
        

        Parameters:
        query (str): an SQL query
        return_type(str): 'dataframe', 'json' or None. (default - the return type specified at client initialization)
        progessIndicator(boolean): an optional IPython progress indicator widget (e.g. ipywidgets IntProgress see: https://ipywidgets.readthedocs.io/en/8.1.5/examples/Widget%20List.html#intprogress) (default None)
        query_tags(dict): A dictionary containing key/value pairs which will be included in the log for this query. Allows for tracking query performance according to user defined need. (default None)
        
        Returns: query results in the specified format.
        """  

        if return_type == None:
            return_type = self.return_type
        if query_tags != None and not isinstance(query_tags, dict):
            print("query_tags is not a dictionary")
            sys.exit(1)

        url = self.hostURL + "/search"
        query = query.replace("\n", " ").replace("\t", " ")
        query = query.strip()
        query_dict = {"query":query}        
        if self.passport != None:
            query_dict["passport"] = self.passport
        #query2 = "{\"query\":\"%s\", \"parameters\":[]}" % query
        query2 = json.dumps(query_dict)
        #query2 = f'\{\"query\":\{query}\", \"parameters\":[]\}'
        if self.debug:
            print(f"Query: {query2}")

        response = requests.request("POST", url,
            headers=self.headers, data = query2)
        
        self.t_start = time.perf_counter()
        stats_dict =    {
            "time": datetime.now().isoformat(),
            "server": self.hostURL,
            "method": "data_connect",
            "query": query
        }
        if query_tags != None:
            stats_dict.update(query_tags)

        return self.__handle_response(response, stats_dict, return_type, progessIndicator)


    def get_data(self, table, return_type=None, progessIndicator=None, query_tags=None):
        """Return all data from a specified table. The function will indicate progress as multiple pages of results are returned.
        

        Parameters:
        table (str): the table name to get
        return_type(str): 'dataframe', 'json' or None. (default - the return type specified at client initialization)
        progessIndicator(boolean): see run_query (default None)
        query_tags(dict):  see run_query  (default None)
        
        Returns: table data in the specified format.
        """  

        query = f"/table/{table}/data"
        
        self.t_start = time.perf_counter()
        stats_dict =    {
            "time": datetime.now().isoformat(),
            "server": self.hostURL,
            "method": "data_connect",
            "query": query
        }
        if query_tags != None:
            stats_dict.update(query_tags)

        if return_type == None:
            return_type = self.return_type

        url = self.hostURL + query
        if self.passport != None:
                headers = {"GA4GH-Search-Authorization": f"ga4gh-passport={self.passport}"}
                response = requests.request("GET", url, headers=headers)
        else:    
            response = requests.request("GET", url)
        return self.__handle_response(response, stats_dict, return_type, progessIndicator)


    def __handle_response(self, response, stats_dict, return_type, progessIndicator):
        total_pageCount = 0
        pageCount = 0
        resultRows = []
        column_list = []
        if not progessIndicator:
            print ("Retrieving the query")
        done = False
        bytes_retrieved = 0
        while not done :
            total_pageCount += 1
            if progessIndicator:
                progessIndicator.value += 1
            else:
                print ("____Page{}_______________".format(total_pageCount))

            if self.debug: print(response.content)
            result = (response.json())
            
            if self.debug:
                print(json.dumps(result, indent=3))
            if 'pagination' in result and 'next_page_url' in result['pagination']:
                next_url = result['pagination']['next_page_url']
            else:
                next_url = None
                done = True
            # only count pages with data
            if len(result['data']) > 0:
                pageCount += 1
                bytes_retrieved += len(response.content)
            resultRows += result['data']

            if 'data_model' in result:
                if self.debug: print('found data model')
                #column_list = result['data_model']['properties'].keys()

            if len(resultRows) >= self.row_limit:
                print(f"Client row limit of {self.row_limit} was reached. Reset limit with care!")
                done = True	

            # Get the next page
            if not done :
                response = requests.request("GET", next_url)

        if progessIndicator:
            progessIndicator.value = progessIndicator.max

        t_end = time.perf_counter()
        elapsed = t_end - self.t_start

        stats_dict.update( { "records" : len(resultRows),
                           "bytes" : bytes_retrieved,
                           "pages" : pageCount,
                           "elapsed_secs": float(f"{elapsed:0.4f}") } )
 
        if self.query_log != None:
            self.__write_log(stats_dict)
        
        # fix for dbGaP tables with non dictionary columns
        #deficit = len(resultRows[0]) - len(column_list)
        #if deficit == 1:
        #    column_list = ['dbgap_subject_id'] + list(column_list)
        #elif deficit == 2:
        #    column_list = ['dbgap_subject_id', 'dbgap_sample_id'] + list(column_list)
        if return_type == 'dataframe':
            #df = pd.DataFrame(resultRows, columns=column_list, index=None)
            df = pd.DataFrame.from_dict(resultRows)
            return df
        else:
            return resultRows

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

    def run_param_query(self, query, return_type=None, progessIndicator=None):

        if return_type == None:
            return_type = self.return_type

        url = self.hostURL + "/search"
        query_text = query['query'].replace("\n", " ").replace("\t", " ")
        query_text = query_text.strip()
        #query2 = "{\"query\":\"%s\"}" % query
        query2 = {"query":query_text, "parameters":query['parameters']}
        if self.debug:
            print("Query: {}".format(query2))
        #query2 = query

        #response = requests.request("POST", url,
        #	headers=self.headers, data = query2)
        response = requests.post(url, json = query2)
        return self.__handle_response(response, return_type, progessIndicator)



    def query2Frame(self, query):
        return self.run_query(query, return_type='dataframe')

class SearchSchema():
    ''' A table schema '''	
    def __init__(self, table_info ):
        self.schema = table_info

    def getCol(self, colName):
        if colName not in self.schema['data_model']['properties']:
            print('No column named {}'.format(colName))
        print(json.dumps(self.schema['data_model']['properties'][colName], indent=3))

    def getcaDSRDefinition(self, ref):

        from urllib.request import urlopen
        from xml.etree.ElementTree import parse
        metaresolverURL = 'http://identifiers.org/{}'.format(ref)
        var_url = urlopen(metaresolverURL)
        xmldoc = parse(var_url)

        root = xmldoc.getroot()
        requiredFields=['publicID','version','dateCreated','dateModified','longName',
                'preferredDefinition','preferredName', 'registrationStatus']

        requiredLinks=['valueDomain','dataElementConcept']
        caDSRrep = {}
        for item in root.findall('./queryResponse/class/field'):
            fName = item.get('name')
            if fName in requiredFields:
                caDSRrep[fName]=item.text
            if fName in requiredLinks:
                caDSRrep[fName]=item.get('{http://www.w3.org/1999/xlink}href')

        return caDSRrep


def usage():
    print (sys.argv[0] +' -s service -l listTables -c listCatalog -t tableInfo -r registeredServices')

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "hls:c:t:ra", ["help", "listTables", "service", "tableInfo", "registeredServices","catalogs"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    searchClient = None
    for opt, arg in opts:
        if opt == '-s':
            searchClient = DataConnectClient(arg, debug=True)
    if searchClient == None:
        print("-s service must be provided")
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-l", "--listTables"):
            searchClient.list_tables(verbose=True)
        elif opt in ("-c", "--listCatalog"):
            searchClient.list_catalog(arg)
        elif opt in ("-t", "--table"):
            ti = searchClient.list_table_info(arg, verbose=True)
        elif opt in ("-a", "--catalogs"):
            searchClient.list_catalogs()
        elif opt in ("-r", "--registeredServices"):
            DataConnectClient.getRegisteredSearchServices()


if __name__ == "__main__":
    main(sys.argv[1:])

