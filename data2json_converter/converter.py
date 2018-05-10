import json
import argparse
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('-f', "--raw-file", type=str, required=False)
parser.add_argument('-s', "--suffix", type=str, required=False)

def writeout(jsons, suffix):
    with open("{}.json".format(suffix), "a+") as j:
        json.dump(jsons, j, indent=4)

def generate_json(raw_file, suffix):
    bunchsize = 1000000
    new_jsons = []
    with open(raw_file) as f:
        for l in f.readlines():
            new_line = {}
            line_values = l.split("\t")

            new_line[suffix + "_id"] = line_values[0]
            new_line[suffix + "_enhancerID"] = line_values[1]
            new_line[suffix + "_pantherID"] = line_values[2]
            new_line[suffix + "_tissueID"] = line_values[3]
            new_line[suffix + "_assayID"] = line_values[4].rstrip()
            new_jsons.append(new_line)
            if len(new_jsons) == bunchsize:
                print("writing " + suffix)
                writeout(new_jsons, suffix)
                new_jsons = []
    writeout(new_jsons, suffix)

def check_file(file_path):
    if path.isfile(file_path):
        return True
    else:
        print("File path '" + file_path + "' does not exist.")
        return False

def parse_file(raw_file=None, suffix=None):
    if raw_file is None:
        for suffix in ["chia","eqtl","tad"]:
        # for suffix in ["tad"]:
            raw_file = "raw/linksDBtablePANTHER{}".format(suffix)
            if check_file(raw_file):
                generate_json(raw_file, suffix)

    else:
        generate_json(raw_file, suffix)


def main():
    args = parser.parse_args()
    parse_file(args.raw_file, args.suffix)

if __name__ == "__main__":
    main()

#### ./bin/solr delete -c enhancerenrichment
#### ./bin/solr create_core -c enhancerenrichment
#### python3 converter.py
#### ./bin/post -c enhancerenrichment enhancerenrichment/docs/*