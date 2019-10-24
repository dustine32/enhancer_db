import requests
import os
import yaml

ASSAY_LOOKUP = {
"1": "ChIA-PET",
"2": "single-tissue eQTL",
"3": "Topologically Associated Domain",
"4": "DNAse Hyersensitivity Region, histone acetylation marks"
}

CONFIG_PROPERTIES = {}
CONFIG_YAML = "config/config.yaml"
if not os.path.isfile(CONFIG_YAML):
    print("No config file found: {} - Please create config".format(CONFIG_YAML))
    exit()
else:
    with open(CONFIG_YAML) as f:
        CONFIG_PROPERTIES = yaml.safe_load(f)

def get_results(q):
    solr_base_url = CONFIG_PROPERTIES["SOLR_BASE_URL"]
    response = requests.get(url="{}/solr/enhancer/select?q={}&rows=100000".format(solr_base_url, q))
    data = response.json()
    try:
        results = data["response"]["docs"]
    except KeyError:
        print(data)
        return []
    ret = []
    for r in results:
        print_str = "#1 - "
        row_cols = []
        # for k in r:
        #     row_cols.append("{} : {}".format(k, r[k]))
            # row_cols.append("{}".format(k))
        # print_str += ", ".join(row_cols)
        # print(print_str)
        ret.append(r)
    return ret

def get_query(type, params):
    if type == "gene2enhancers":
        results = []
        for ev in ["chia","eqtl","tad"]:
            col_name = ev + "_gene"
            q_str = "{}:{}".format(col_name, params["gene"])
            results = results + get_results(q_str)
        joined_results = []
        for er in results:
            enhancer_key, enhancer_id = item_with_key_suffix(er, "_enhancer")
            # for k, v in er.items():
            #     if k.endswith("_enhancer"):
            if enhancer_id is not None:
                # print("got here")
                q_str = "{}:{}".format("enhancer_ID", enhancer_id[0])
                enhancer = get_results(q_str)[0]
                enhancer["coordinates"] = enhancer_coordinates(enhancer)
                er["gene"] = item_with_key_suffix(er, "_gene")[1][0]
                er["assay"] = item_with_key_suffix(er, "_assay")[1][0]
                er["tissue"] = item_with_key_suffix(er, "tissue")[1][0]
                joined_results.append({**er, **enhancer})
        # final_results = []
        # for r in results:
    return joined_results

def item_with_key_suffix(dictionary, suffix):
    for k, v in dictionary.items():
        if k.endswith(suffix):
            return k, v

def enhancer_coordinates(enhancer_doc):
    return "{}:{}-{}".format(enhancer_doc["enhancer_chromosome"][0], enhancer_doc["enhancer_start"][0], enhancer_doc["enhancer_end"][0])

# print(response.json())
# print(get_results())