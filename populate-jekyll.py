#!/usr/bin/env python3

import os
import click
import cli.lis_cli as lis_cli

@click.group()
def cli():
    '''CLI entry for populate-jekyll'''
    pass


cli.add_command(lis_cli.collections)
cli()  # invoke cli
