#!/usr/bin/env python3

import os
import click
from .genus_species_collections import ProcessCollections


@click.command()
@click.option('--taxa_list', default="../_data/taxon_list.yml", help='''Taxa.yml file. (Default: ../_data/taxon_list.yml)''')
@click.option('--jbrowse_out', default="/var/www/html/jbrowse2_autodeploy", help='''Output directory for Jbrowse2. (Default: /var/www/html/jbrowse2_autodeploy)''')
def collections(taxa_list, jbrowse_out):
    '''CLI entry for populate-jekyll'''
    click.echo("Populating Collections...")
    parser = ProcessCollections()  # initialize class
    click.echo("Generating Collections...")
    parser.parse_collections(taxa_list)  # parse_collections
    click.echo("Creating JBrowse Instance...")
    parser.deploy_jbrowse2(jbrowse_out)  # populate JBrowse2
