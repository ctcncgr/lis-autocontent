#!/usr/bin/env python3

import os
import click
from .genus_species_collections import ProcessCollections


@click.command()
@click.option('--taxa_list', help='''Taxa.yml file. (Default: ../_data/taxon_list.yml)''')
@click.option('--jbrowse_out', help='''Output directory for Jbrowse2''')
def collections(taxa_list):
    '''CLI entry for populate-jekyll'''
    click.echo("Populating Collections...")
    parser = ProcessCollections()  # initialize class
    parser.parse_collections(taxa_list)  # parse_collections
    parser.deploy_jbrowse2(target_dir)
    pass
