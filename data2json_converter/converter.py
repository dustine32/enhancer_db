import csv
import json
import argparse
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('-f', "--raw-file", type=str, required=False)
parser.add_argument('-e', "--enhancer_file")
parser.add_argument('-a', "--assay_file")
parser.add_argument('-t', "--tissue_file")
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

def parse_lookup_file(filepath):
    lookup = {}
    with open(filepath) as f:
        reader = csv.reader(f, delimiter="\t")
        for r in reader:
            # Ex: ['1', 'Adipose Subcutaneous']
            lookup[r[0]] = r[1]
    return lookup


def parse_enhancer_file(filepath):
    lookup = {}
    with open(filepath) as f:
        reader = csv.reader(f, delimiter="\t")
        for r in reader:
            # Ex: ['chr1', '99534632', '99534837', '1']
            lookup[r[3]] = {
                "chrNum": r[0],
                "start": r[1],
                "end": r[2],
            }
    return lookup


ASSAY_LOOKUP = None
TISSUE_LOOKUP = None
COORDINATES_LOOKUP = None  # TODO: Enhancer coordinates files

def writeout(jsons):
    # with open("out.json", "a+") as j:
    with open("out.json", "w+") as j:
        json.dump(jsons, j, indent=4)

def generate_json(raw_file, col_map=column_mapping, parse_col=False, delimiter=None):
    # rows[0]
    # ['enhancer', 'gene', 'linkID', 'assay', 'tissue', 'p-value', 'eQTL_SNP_ID']
    # rows[3]
    # ['1', 'HUMAN|HGNC=15846|UniProtKB=Q9NP74', '1', '3', '66', '', '']
    # rows[20]
    # ['1', 'HUMAN|HGNC=15846|UniProtKB=Q9NP74', '1', '4', '53', '6e-08', '']

    bunchsize = 1000000
    new_jsons = []
    if delimiter is None:
        delimiter = "\t"
    with open(raw_file) as f:
        reader = csv.reader(f, delimiter="\t")
        if parse_col:
            col_map = next(reader)
        elif col_map is None:
            col_map = column_mapping
        elif col_map.__class__ is str:
            col_map = col_map.split(",")
        for r in reader:
            new_line = {}
            for idx, val in enumerate(r):
                if len(val) > 0:
                    if col_map[idx] == "enhancer":
                        # fancy way to merge coord info to new_line
                        new_line = {**new_line, **COORDINATES_LOOKUP[val]}
                    if col_map[idx] == "assay":
                        val = ASSAY_LOOKUP[str(val)]
                    if col_map[idx] == "tissue":
                        val = TISSUE_LOOKUP[str(val)]
                    new_line[col_map[idx]] = val
            new_jsons.append(new_line)
            if len(new_jsons) == bunchsize:
                print("writing files out")
                writeout(new_jsons)
                new_jsons = []
    writeout(new_jsons)

def check_file(file_path):
    if path.isfile(file_path):
        return True
    else:
        print("File path '" + file_path + "' does not exist.")
        return False

def parse_file(raw_file=None, col_map=None, parse_col=False, delimiter=None):
    # print(col_map.__class__.__name__)
    if raw_file is None:
        for suffix in ["chia","eqtl","tad"]:
            raw_file = "raw/linksDB{}".format(suffix)
            if check_file(raw_file):
                generate_json(raw_file, col_map, parse_col, delimiter)

    else:
        generate_json(raw_file, col_map, parse_col, delimiter)


def main():
    args = parser.parse_args()

    global ASSAY_LOOKUP
    ASSAY_LOOKUP = parse_lookup_file(args.assay_file)
    global TISSUE_LOOKUP
    TISSUE_LOOKUP = parse_lookup_file(args.tissue_file)
    global COORDINATES_LOOKUP
    COORDINATES_LOOKUP = parse_enhancer_file(args.enhancer_file)

    parse_file(args.raw_file, args.col_map, args.parse_col, args.delimiter)
    # TODO: Add docs for unlinked enhancers

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