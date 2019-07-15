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

    changed = []

    for listing in newtotal:
        if listing not in oldtotal:
            changed.append(listing)

    return changed