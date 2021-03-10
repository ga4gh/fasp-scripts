# Getting Started

This guide walks through the step-by-step process of getting FASP newcomers 
prepared to successfully run the scripts within this repo.

## Repository setup

As a prerequsite, Python version 3.x or higher must be installed. You may 
consider setting up a virtual environment for `fasp-scripts` to avoid 
dependency issues with other projects.

To begin, clone this repository to your local machine, and install 
dependencies and the core library:
```
git clone https://github.com/ga4gh/fasp-scripts.git
cd fasp-scripts
python setup.py install
pip install .
```

## Create the Settings file

TODO explain settings file and provide example(s)

## Establish relationships with external services, manage API keys

The scripts require the user, acting as a researcher, to have API access
to web services owned by a number of real-world, genomic data sharing institutes.
These institutions include:
* BioDataCatalyst
* Cancer Research Data Commons
* AnVIL
* Seven Bridges Cancer Genomics Cloud (CGC) 
* Seven Bridges Cavatica

Before we register or get our API keys with any of the above platforms, let's 
set up our local directory to hold these keys in the place that the
`fasp-scripts` expect to find them. To do this, simply create the `.keys` folder under your home directory:
```
mkdir ~/.keys
```
OR
```
mkdir $HOME/.keys
```

We will place our API key files under this directory. Now, we need to register
accounts with the data platforms. Let's start with BioDataCatalyst.

### Register with BioDataCatalyst






