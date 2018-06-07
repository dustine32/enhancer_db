import json
import argparse
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('-f', "--raw-file", type=str, required=False)
parser.add_argument('-s', "--suffix", type=str, required=False)
parser.add_argument('-c', "--col-map", type=str, required=False)
parser.add_argument('-d', "--delimiter", type=str, required=False)
parser.add_argument("--parse-col", action="store_true")

column_mapping = [
    'id',
    'enhancerID',
    'pantherID',
    'tissue',
    'assay'
]
ASSAY_LOOKUP = {
"1": "ChIA-PET",
"2": "single-tissue eQTL",
"3": "Topologically Associated Domain",
"4": "DNAse Hyersensitivity Region, histone acetylation marks"
}
TISSUE_LOOKUP = {}
with open("resources/tissuetable") as tf:
    for tline in tf.readlines():
        tnum, tname = tline.split("\t")
        TISSUE_LOOKUP[str(tnum)] = tname.rstrip()

def writeout(jsons, suffix):
    with open("{}.json".format(suffix), "a+") as j:
        json.dump(jsons, j, indent=4)

def generate_json(raw_file, suffix, col_map=column_mapping, parse_col=False, delimiter=None):
    bunchsize = 1000000
    new_jsons = []
    if delimiter is None:
        delimiter = "\t"
    with open(raw_file) as f:
        if parse_col:
            # print("hey")
            col_map = f.readline().rstrip().split(delimiter)
        elif col_map is None:
            col_map = column_mapping
        elif col_map.__class__ is str:
            col_map = col_map.split(",")
        # print(col_map)
        for l in f.readlines():
            new_line = {}
            line_values = l.split(delimiter)
            for idx, val in enumerate(line_values):
                val = val.rstrip()
                if col_map[idx] == "assay":
                    val = ASSAY_LOOKUP[str(val)]
                if col_map[idx] == "tissue":
                    val = TISSUE_LOOKUP[str(val)]
                new_line["{}_{}".format(suffix, col_map[idx])] = val
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

def parse_file(raw_file=None, suffix=None, col_map=None, parse_col=False, delimiter=None):
    # print(col_map.__class__.__name__)
    if raw_file is None:
        for suffix in ["chia","eqtl","tad"]:
            raw_file = "raw/linksDB{}".format(suffix)
            if check_file(raw_file):
                generate_json(raw_file, suffix, col_map, parse_col, delimiter)

    else:
        generate_json(raw_file, suffix, col_map, parse_col, delimiter)


def main():
    args = parser.parse_args()
    parse_file(args.raw_file, args.suffix, args.col_map, args.parse_col, args.delimiter)

if __name__ == "__main__":
    main()

#### (from solr-7.3.0/enhancer_db directory)
#### python3 data2json_converter/converter.py -f raw/linksDBnumeqtl -s eqtl --parse-col
#### python3 data2json_converter/converter.py -f raw/linksDBtad -s tad --parse-col
#### python3 data2json_converter/converter.py -f raw/linksDBchia -s chia --parse-col
#### python3 data2json_converter/converter.py -f raw/enhancerDBtable052618 -s enhancer -c ID,chromosome,start,end,build,source

#### (from solr-7.3.0 directory)
#### ./bin/solr delete -c enhancer
#### ./bin/solr create_core -c enhancer
#### ./bin/post -c enhancer enhancer_db/docs/*