import json
import argparse
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('-f', "--raw-file", type=str, required=False)
parser.add_argument('-s', "--suffix", type=str, required=False)
parser.add_argument('-c', "--col-map", type=str, required=False)
parser.add_argument("--parse-col", action="store_true")

column_mapping = [
    'id',
    'enhancerID',
    'pantherID',
    'tissueID',
    'assayID'
]

def writeout(jsons, suffix):
    with open("{}.json".format(suffix), "a+") as j:
        json.dump(jsons, j, indent=4)

def generate_json(raw_file, suffix, col_map=column_mapping, parse_col=False):
    bunchsize = 1000000
    new_jsons = []
    with open(raw_file) as f:
        if parse_col:
            # print("hey")
            col_map = f.readline().rstrip().split("\t")
        elif col_map is None:
            col_map = column_mapping
        elif col_map.__class__ is str:
            col_map = col_map.split(",")
        # print(col_map)
        for l in f.readlines():
            new_line = {}
            line_values = l.split("\t")
            for idx, val in enumerate(line_values):
                new_line["{}_{}".format(suffix, col_map[idx])] = val.rstrip()
            new_jsons.append(new_line)
            if len(new_jsons) == bunchsize:
                print("writing " + suffix)
                writeout(new_jsons, suffix)
                new_jsons = []
    writeout(new_jsons, suffix)

def generate_assay_json(raw_file, suffix):
    return ''

def check_file(file_path):
    if path.isfile(file_path):
        return True
    else:
        print("File path '" + file_path + "' does not exist.")
        return False

def parse_file(raw_file=None, suffix=None, col_map=None, parse_col=False):
    # print(col_map.__class__.__name__)
    if raw_file is None:
        for suffix in ["chia","eqtl","tad"]:
            raw_file = "raw/linksDB{}".format(suffix)
            if check_file(raw_file):
                generate_json(raw_file, suffix, col_map, parse_col)

    else:
        generate_json(raw_file, suffix, col_map, parse_col)


def main():
    args = parser.parse_args()
    # print(args.parse_col)
    parse_file(args.raw_file, args.suffix, args.col_map, args.parse_col)

if __name__ == "__main__":
    main()

#### python3 data2json_converter/converter.py -f raw/linksDBnumeqtl -s eqtl -c enhancer,gene,tissue,number_of_eQTL,assay
#### python3 data2json_converter/converter.py -f raw/enhancerDBtable052618 -s enhancer -c ID,chromosome,start,end,build,source

#### ./bin/solr delete -c enhancerenrichment
#### ./bin/solr create_core -c enhancerenrichment
#### python3 converter.py
#### ./bin/post -c enhancerenrichment enhancerenrichment/docs/*