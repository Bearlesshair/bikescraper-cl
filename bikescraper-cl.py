#!/bin/env python3
import argparse
import config, query, excel

parser = argparse.ArgumentParser(prog='bikescraper-cl', description='Craigslist bicycle finder')
parser.add_argument('--config', help='Config file location (default .bikescraper-cl/config.yaml)')
args = parser.parse_args()

# get configuration
configDict = config.get(args.config)

# run query
storage = query.do(configDict)

# export to excel file if new relevant listings
excelfile = excel.export(storage)
