import argparse

# add argparse arguments
parser = argparse.ArgumentParser(
    description="Utility to convert a MJCF into USD format."
)
parser.add_argument("input", type=str, help="The path to the input MJCF file.")
parser.add_argument("output", type=str, help="The path to store the USD file.")
import xml.etree.ElementTree as ET

args_cli = parser.parse_args()

# parse xml
tree = ET.parse(args_cli.input)
root = tree.getroot()

# get 'body' tag in 'worldbody'
worldbody = root.find("worldbody")
if worldbody is not None:
    # get 'body name="object"' tag
    body = worldbody.find("body")
    body_object = body.find('body[@name="object"]')

    # remove 'body' tag
    if body is not None:
        worldbody.remove(body)

    if body_object is None:
        raise ValueError("body object does not exist.")
    else:
        worldbody.append(body_object)

    # remove 'site' tag
    sites_to_remove = [
        worldbody.find("site"),
    ]

    for site in sites_to_remove:
        if site is not None:
            worldbody.remove(site)

# save fixed xml file
tree.write(args_cli.output)
