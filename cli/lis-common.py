import os
import sys


def split_name(name):
    '''Split provided string into delimited parts, "." delimiter'''
    fields = name.split('.')  # split on delimiter
    return fields


def split_url(url):
    '''Splits URL into sub uri parts using "/"'''
    fields = url.split('/')  # split on delimiter
    return fields


def get_gensp(parts):
    '''Gets gensp and strain and from parts array and returns a tuple'''
    gensp = f'{parts[1].lower()[:3]}{parts[2][:2]}'  # make gensp from preparsed organismDir
    strain = parts[-2]  # get strain and key information
    return (gensp, strain)
