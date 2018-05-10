import json

def writeout(jsons, suffix):
    with open("~/enhancerenrichment/docs/{}.json".format(suffix), "a+") as j:
        json.dump(new_jsons, j, indent=4)

bunchsize = 1000000
# for suffix in ["chia","eqtl","tad"]:
for suffix in ["tad"]:
    new_jsons = []
    with open("/auto/rcf-proj3/hm/caitlimm/enhancerenrichment/significant/finalfiles/dbtables/linksDBtablePANTHER{}".format(suffix)) as f:
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


#### ./bin/solr delete -c enhancerenrichment
#### ./bin/solr create_core -c enhancerenrichment
#### python3 converter.py
#### ./bin/post -c enhancerenrichment enhancerenrichment/docs/*