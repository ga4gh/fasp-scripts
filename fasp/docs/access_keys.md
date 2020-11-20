### Getting an access key to use with Gen3 DRS services

If you go to the gen3 user interface for the Commons whose DRS service you wish to use (see table below) you will be able to create an account using the same account you use for dbGaP. Within that Data Commons you should then be able to access projects for which you have been granted authorization through dbGaP. Only those dbGaP projects which that particular Commons manages will be visible. You can check that your Commons account has access by using Explore to find the files via facets. 

In the user interface  go to Profile and click on “create API Key”. You can then download the API Key as a json file. It will be needed by the FASP scripts. Rename the file according to the following table and place it in a subdirectory .keys of yout home directory.



| Data Commons                 | Gen3 user interface                                   | Rename access key file as |
| ---------------------------- | ----------------------------------------------------- | ------------------------- |
| Anvil                        | [https://gen3.theanvil.io](https://gen3.theanvil.io/) | anvil_credentials.json    |
| BioDataCatalyst              | https://gen3.biodatacatalyst.nhlbi.nih.gov            | bdc_credentials.json      |
| Cancer Research Data Commons | https://nci-crdc.datacommons.io                       | crdc_credentials.json     |
| Kids First                   | https://data.kidsfirstdrc.org                         | kf_credentials.json       |

