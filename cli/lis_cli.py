#!/usr/bin/env python3

import os
import click
from .genus_species_collections import ProcessCollections


@click.command()
@click.option('--taxa_list', default="../_data/taxon_list.yml", help='''Taxa.yml file. (Default: ../_data/taxon_list.yml)''')
@click.option('--collections_out', default="../_data/taxa/", help='''Output for collections.''')
def populate_jekyll(taxa_list, collections_out):
    '''CLI entry for populate-jekyll'''
    click.echo("Populating Collections...")
    parser = ProcessCollections()  # initialize class
    click.echo("Generating Collections...")
    parser.parse_collections(taxa_list, collections_out)  # parse_collections

@click.command()
@click.option('--taxa_list', default="../_data/taxon_list.yml", help='''Taxa.yml file. (Default: ../_data/taxon_list.yml)''')
@click.option('--jbrowse_out', default="/var/www/html/jbrowse2_autodeploy", help='''Output directory for Jbrowse2. (Default: /var/www/html/jbrowse2_autodeploy)''')
@click.option('--cmds_only', is_flag=True, help='''Output commands only. Do not run Jbrowse2 just output the commands that would be run.''')
def populate_jbrowse2(taxa_list, jbrowse_out, cmds_only):
    '''CLI entry for deploy-jbrowse2'''
    click.echo("Populating Collections...")
    parser = ProcessCollections()  # initialize class
    parser.parse_collections(taxa_list)  # parse_collections
    click.echo("Creating JBrowse Instance...")
    parser.populate_jbrowse2(jbrowse_out, cmds_only)  # populate JBrowse2

@click.command()
@click.option('--taxa_list', default="../_data/taxon_list.yml", help='''Taxa.yml file. (Default: ../_data/taxon_list.yml)''')
@click.option('--blast_out', default="/var/www/html/db/Genomic_Sequence_Collection", help='''Output directory for Jbrowse2. (Default: /var/www/html/db/Genomic_Sequence_Collection)''')
@click.option('--cmds_only', is_flag=True, help='''Output commands only. Do not run makeblastdb just output the commands that would be run.''')
def populate_blast(taxa_list, blast_out, cmds_only):
    '''CLI entry for populate-blast'''
    click.echo("Populating Collections...")
    parser = ProcessCollections()  # initialize class
    parser.parse_collections(taxa_list)  # parse_collections
    click.echo("Creating BLAST Instance...")
    parser.populate_blast(blast_out, cmds_only)  # populate BLAST
