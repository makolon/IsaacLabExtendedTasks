import os
import argparse

# add argparse arguments
parser = argparse.ArgumentParser(
    description="Utility to convert a MJCF into USD format."
)
parser.add_argument("input", type=str, nargs="+", help="Paths to the input MJCF files.")
import xml.etree.ElementTree as ET

args_cli = parser.parse_args()


def main():
    # parse xml
    xml_paths = args_cli.input
    for xml_path in xml_paths:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # get 'body' tag in 'worldbody'
        worldbody = root.find("worldbody")
        for body in worldbody.findall('body'):
            for site in body.findall('site'):
                body.remove(site)

        for body in worldbody.findall('body'):
            inner_body = body.find('body[@name="object"]')
            if inner_body is not None:
                worldbody.append(inner_body)
                worldbody.remove(body)

        dirname = os.path.dirname(xml_path)
        basename = os.path.basename(xml_path).split('.')[0]
        output_path = os.path.join(dirname, f"{basename}_fixed.xml")

        # save fixed xml file
        tree.write(output_path)


if __name__ == "__main__":
    main()
