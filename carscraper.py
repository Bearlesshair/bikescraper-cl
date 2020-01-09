import config
import query


def get_results(searchterm, filename, configpath=None):
    # get configuration
    config_dict = config.get(configpath)

    # run query
    result = query.do(config_dict, filename)
    return result
