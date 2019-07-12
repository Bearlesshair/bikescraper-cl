#!/bin/env python3
import argparse
import query, excel

parser = argparse.ArgumentParser(prog='bikescraper-cl', description='Craigslist bicycle finder')
parser.add_argument('--config', help='Config file location (default .bikescraper-cl/config.yaml)')
args = parser.parse_args()

storage = query.do(args.config)

excel.export(storage)