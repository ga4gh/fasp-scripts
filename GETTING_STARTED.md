# Getting Started

This guide walks through the step-by-step process of getting FASP newcomers 
prepared to successfully run the scripts within this repo.

## Initial setup

If you already have Python, Pip, and Virtualenv installed on your system, skip
ahead to "Repository setup."

`fasp-scripts` requires Python version 3.x or higher with `pip` and `virtualenv`
to be installed on your system. Download Python and Pip from the
[downloads page](https://www.python.org/downloads/) and install. Confirm
installation by running:
```
python3 -V
pip3 -V
```

With Python and Pip installed, install virtualenv:
```
python3 -m pip install virtualenv
```

Next, let's setup the `fasp-scripts` repository

## Repository setup

To begin, clone the `fasp-scripts` repository, and navigate to it.
```
git clone https://github.com/ga4gh/fasp-scripts.git
cd fasp-scripts
```

Let's create and activiate a virtual environment for `fasp-scripts` to avoid dependency conflicts with other projects.
```
virtualenv env
source env/bin/activate
```

Next, install dependencies and the core library:
```
python setup.py install
pip install .
```

## Create the FASP Settings file

The FASP settings file contains a number of configuration parameters for the 
scripts. Let's copy the [default FASP settings file](./fasp/examples/FASPSettings.json) to another directory, for example, our home directory:
```
cp ./fasp/examples/FASPSettings.json ~
```

Next, let's set the `FASP_SETTINGS` environment variable so the `fasp-scripts`
know where the setting files is located:
```
export FASP_SETTINGS="${HOME}/FASPSettings.json"
```

TODO instruct user to modify pipeline log

```
mkdir -p ~/.fasp-scripts/logs
```

We created our own FASP settings file outside the repository so we can modify
the behavior of certain scripts by changing the parameters. For now, the default
parameters are enough to get started.

## Google config

```
gcloud auth login
gcloud auth application-default login
gcloud projects create fasp-scripts
gcloud config set project fasp-scripts
```

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






