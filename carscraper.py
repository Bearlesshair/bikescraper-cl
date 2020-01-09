import config
import query


def get_results(searchterm, filename, configpath=None):
    # get configuration
    config_dict = config.get(configpath)
    config_dict['auto_make_model'] = searchterm  # THIS SEARCHES CAR MAKE/MODEL, NOT TITLE
    # run query
    result = query.do(config_dict, filename) # Multiple filenames to parse new entries
    return result
