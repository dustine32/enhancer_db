import requests

def get_results(key, term):
    response = requests.get(url="http://68.181.125.171:8983/solr/enhancer/select?q={}:{}".format(key, term))
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
        for k in r:
            row_cols.append("{} : {}".format(k, r[k]))
            # row_cols.append("{}".format(k))
        print_str += ", ".join(row_cols)
        # print(print_str)
        ret.append(r)
    return ret

# print(response.json())
# print(get_results())