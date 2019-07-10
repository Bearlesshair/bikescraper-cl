#!/bin/env python3
import argparse
import query

parser = argparse.ArgumentParser(prog='bikescraper-cl', description='Craigslist bicycle finder')
parser.add_argument('--config', help='Config file location (default .bikescraper-cl/config.yaml)')
args = parser.parse_args()

query.do(args.config)