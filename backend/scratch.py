from analysis import *
import numpy as np

view_addr = "http://admin:admin@172.26.134.68:5984/melbourne/_design/aggr/_view/zone/"

aurin_db_addr = "http://admin:admin@172.26.134.68:5984/sa2"

if __name__ == "__main__":
    # rst = get_zone_aggr_data(view_addr)
    # base_line = np.ones(25)
    # print(len(rst))
    # # print(rst[0])
    # print(get_zone_aggr_similarity(view_addr, base_line))
    # print(rst)
    # with open("./test_data.json", "w+") as fd:
    #     import json
    #     json.dump(rst, fd)
    rst = get_aurin_data(aurin_db_addr, "income")
    print(rst)
