# lis-autocontent
Generates content for jekyll collections and populates JBrowse2 instances from https://data.legumeinfo.org

## Reqiurements

1. JBrowse2. (https://jbrowse.org/jb2/docs/combined/)
2. Python3

## Install

1. Clone repository into _scripts directory for jekyll-legumeinfo. `git clone https://github.com/ctcncgr/lis-autocontent.git`
2. Create a virtual environment for python3 `/path/to/python3/bin/virtualenv autocontent_env`
3. Source virtual environment `. ./autocontent_env/bin/activate`
4. Install requirements. `pip install -r ./lis-autocontent/requirements.txt`
5. Create jbrowse-components instance. `sudo sh -c 'mkdir -p /var/www/html/jbrowse2_autodeploy;jbrowse create /var/www/html/jbrowse2_autodeploy'`
6. Change permissions for jbrowse2 if needed. `chown $USER:$USER /var/www/html/jbrowse2_autodeploy`

## Run

The pipeline will run with no options if run from the _scripts directory. `python3 ./lis-autocontent/populate-jekyll.py collections`

```
Usage: populate-jekyll.py [OPTIONS] COMMAND [ARGS]...

  CLI entry for populate-jekyll

Options:
  --help  Show this message and exit.

Commands:
  collections  CLI entry for populate-jekyll
```
```
Usage: populate-jekyll.py collections [OPTIONS]

  CLI entry for populate-jekyll

Options:
  --taxa_list TEXT    Taxa.yml file. (Default: ../_data/taxon_list.yml)
  --jbrowse_out TEXT  Output directory for Jbrowse2
  --help              Show this message and exit.
```

DOCKER COMING
