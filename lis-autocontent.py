#!/usr/bin/env python3

import os
import click
import cli.lis_cli as lis_cli

@click.group()
def cli():
    '''CLI entry for populate-jekyll'''
    pass


cli.add_command(lis_cli.populate_jekyll)
cli.add_command(lis_cli.populate_jbrowse2)
cli.add_command(lis_cli.populate_blast)
cli()  # invoke cli
