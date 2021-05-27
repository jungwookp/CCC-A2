import requests
import numpy as np


def get_zone_aggr_data(view_addr, limit=None):
    """
    get twitter aggregated on zone level
    """
    res = requests.get(view_addr, params={
        "group": True,
        "limit": limit,
    })
    rst = res.json()["rows"]
    return {row["key"]: {'count': row["value"][0], 'vector': row["value"][1:]} for row in rst}


def get_zone_aggr_similarity(view_addr, baseline, mean=True):
    aggr_data = get_zone_aggr_data(view_addr)
    baseline = np.array(baseline)
    if mean:
        return {k: np.array(v["vector"]).dot(baseline) / v["count"] for k, v in aggr_data.items()}
    else:
        return {k: np.array(v["vector"]).dot(baseline) for k, v in aggr_data.items()}


def get_aurin_data(aurin_db_addr, doc_id):
    features = {
        "income": "median_aud"
    }
    assert doc_id  in features
    doc = requests.get(f"{aurin_db_addr}/{doc_id}").json()
    fea = features[doc_id]
    rst = { 
        elem['properties']['sa2_code']: elem['properties'][fea]
         for elem in doc['data']['features'] if elem['properties'][fea] is not None
    }
    return rst
