from fasp.workflow import ElixirWESClient, DNAStackWESClient

if __name__ == "__main__":
    # ELIXIR
    elixirClient = ElixirWESClient('https://wes.rahtiapp.fi/ga4gh/wes/v1')
    res = elixirClient.runWorkflow('http://62.217.82.57/test.txt', '/tmp/elixir-out')
    print(res)

    # DNAstack
    myClient = DNAStackWESClient('~/.keys/dnastack_wes_credentials.json')
    res = myClient.runWorkflow('gs://dnastack-public-bucket/thousand_genomes_meta.csv', '')
    print(res)
