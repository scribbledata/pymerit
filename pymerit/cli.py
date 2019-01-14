"""
Merit Command Line 
------------------

"""
import os
import sys
from texttable import Texttable
import click

from .base import * 
from .contrib import * 
from .utils import *

@click.group()
def main():
    """ 
    CLI for merit metadata files
    """
    pass

@main.group("schema")
def schema():
    """
    Discovery and operation 
    """
    pass 

@schema.command("list")
def _schema_list():
    """
    List available schemas 
    """

    merit = MeritDefault() 
    summary = merit.schema_list()
    table = Texttable()
    # table.set_deco(Texttable.HEADER)
    table.add_rows(summary)

    print(table.draw())

@schema.command("show")
@click.argument("schema")
def _schema_show(schema):
    """
    Show details of a schema
    """

    merit = MeritDefault() 
    cls = merit.schema_get(schema)
    help(cls)

@main.group("metadata")
def metadata():
    """
    Metadata processing
    """
    pass

@metadata.command("show")
@click.argument("filename")
def _metadata_show(filename):
    """
    Show metadata content
    """

    merit = news(open(filename).read())
    print(merit.prettyprint())

