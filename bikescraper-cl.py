#!/bin/env python3
import argparse
import config, query, excel, sender

parser = argparse.ArgumentParser(prog='bikescraper-cl', description='Craigslist bicycle finder')
parser.add_argument('--config', help='Config file location (default .bikescraper-cl/config.yaml)')
args = parser.parse_args()

# get configuration
configDict = config.get(args.config)

# run query
storage = query.do(configDict)

# export to excel file if new relevant listings
excelfile = excel.export(storage)

# if excelfile is not empty and gmail option enabled, send spreadsheet
if configDict['sendemail'] is True and excelfile is not None:
    print("Emailing spreadsheet to %s" % configDict['toemail'])
    sender.send(excelfile, configDict['botuser'], configDict['botpassword'], configDict['toemail'])