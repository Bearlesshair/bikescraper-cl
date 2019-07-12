import json


def compare(newtotal, oldtotalfilename):
    try:
        with open(oldtotalfilename, 'r') as f:
            oldtotal = json.load(f)
    except json.decoder.JSONDecodeError as err:
        print("Problem parsing total.json, replacing file:", err)
        return newtotal
    except FileNotFoundError:
        return newtotal     # no total.json file exists yet, all listings are changed listings

    changed = {}

    for city in newtotal:
        if city not in oldtotal:
            changed[city] = newtotal[city]
        else:
            changed[city] = []
            for listing in newtotal[city]:
                if listing not in oldtotal[city]:
                    changed[city].append(listing)

    return changed