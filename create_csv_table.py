#!/usr/bin/python3
"""
This will take in data and produce a table definition to accomodate it in sql
"""
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import CreateTable
from sqlalchemy import Table, Column, String, MetaData

import datetime
import fileinput
import sys

from field_length import read_input

def main():
    table_name = 'import_' + str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M"))

    if len(sys.argv) == 1:
        input_, output_ = fileinput.input(), sys.stdout
    elif len(sys.argv) == 2:
        table_name = sys.argv[1]
        input_, output_ = open(sys.argv[1]), sys.stdout
    elif len(sys.argv) == 3:
        table_name = sys.argv[2]
        input_, output_ = open(sys.argv[1]), open(sys.argv[2], 'w+')
    else:
        print("Usage: ./create_csv_table.py [input] [output]")
        sys.exit(1)

    matrix = read_input(input_).counts
    for row in matrix:
        if not row[1]:
            row[1] = 1

    columns = [Column(n, String(l)) for n, l in matrix]
    table = CreateTable(Table(table_name, MetaData(),
        *columns
    ))

    output_.write(str(table.compile(dialect=mysql.dialect())))

if __name__ == '__main__':
    main()
