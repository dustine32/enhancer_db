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
        ret.append(r)
    return ret

def get_query(type, params):
    if type == "gene2enhancers":
        results = []
        col_name = "gene"
        q_str = "{}:{}".format(col_name, params["gene"])
        results = get_results(q_str)
        joined_results = []
        for er in results:
            enhancer_id = er["enhancer"][0]
            if enhancer_id is not None:
                q_str = "{}:{}".format("enhancer_ID", enhancer_id)
                er["coordinates"] = enhancer_coordinates(er)
                er["gene"] = er["gene"][0]
                er["assay"] = er["assay"][0]
                er["tissue"] = er["tissue"][0]
                joined_results.append(er)
    return results

def item_with_key_suffix(dictionary, suffix):
    for k, v in dictionary.items():
        if k.endswith(suffix):
            return k, v

def enhancer_coordinates(enhancer_doc):
    return "{}:{}-{}".format(enhancer_doc["chrNum"][0], enhancer_doc["start"][0], enhancer_doc["end"][0])
