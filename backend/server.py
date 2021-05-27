from threading import RLock, Thread
import time
import datetime
from copy import deepcopy
import requests
from flask import request, Flask, g
from flask_cors import CORS
import word2vec as w2v
import polygon
import analysis
from util import log

# ERROR CODES
DB_ERROR_CODE = 100
CONFIG_ERROR_CODE = 200

# CONFIG GLOBAL PARAMs
LOCK = RLock()

WORD2VEC_MODEL_NAME = ""
WORD2VEC_MODEL = None
POLYGON_METHOD = "box"

DB_ADDR = ""
CONFIG_DB_ADDR = ""
CONFIG_FILE_ADDR: str = ""
TWITTER_DB_ADDR = ""
AURIN_DB_ADDR = ""
ANALYSIS_VIEW_ADDR = ""

# MANUALLY SET GLOBAL PARAMs
CONFIG_FILE_ID = ""


def make_new_config_doc(server_type):
    return {
        "id": None,
        "database": {
            "addr": "__something_do_not_exist__",
            "port": "__something_do_not_exist__",
            "user": "__something_do_not_exist__",
            "password": "__something_do_not_exist__",
            "twitter_db": "__something_do_not_exist__",
            "config_db": "__something_do_not_exist__",
            "aurin_db": "__something_do_not_exist__",
        },
        "server": {
            "addr": "__something_do_not_exist__",
            "port": -1,
            "running": False,
            "type": server_type,
            "last_sync": str(datetime.datetime.now()),
            "heartbeat_period": 30,
            "request_num": 0,
            "w2v_model": "glove-twitter-25",
            "view": '',
        }
    }


CONFIG_DOC = make_new_config_doc(None)


# ===============   helper functions ================


def add_request_static():
    with LOCK:
        CONFIG_DOC["server"]["request_num"] += 1


def push_config_file(new_doc):
    global CONFIG_DOC
    with LOCK:
        if new_doc is None:
            new_doc = CONFIG_DOC
        new_doc["server"]["last_sync"] = str(datetime.datetime.now())
        while True:
            log(
                f"update config at: {CONFIG_FILE_ADDR}?rev={CONFIG_DOC['_rev']}")
            res = requests.put(
                f"{CONFIG_FILE_ADDR}?rev={CONFIG_DOC['_rev']}", json=new_doc)
            if res.status_code != 201:
                log("update config file failed: " +
                    res.text + f" {res.status_code} ")
                exit(CONFIG_ERROR_CODE)
            # succ
            res_obj = res.json()
            CONFIG_DOC = new_doc
            CONFIG_DOC["_rev"] = res_obj["rev"]  # update revision
            return True


HEARTBEAT_CONTROL = {
    "heartbeat": True
}

HEARTBEAT_DAEMON = None


def create_and_run_heartbeat(period_in_sec: int=None):
    global HEARTBEAT_DAEMON
    if HEARTBEAT_DAEMON:
        return
    if period_in_sec is None:
        period_in_sec = int(CONFIG_DOC["server"]["heartbeat_period"])

    def task(sec):
        while "heartbeat" in HEARTBEAT_CONTROL and HEARTBEAT_CONTROL["heartbeat"]:
            time.sleep(sec)
            with LOCK:
                new_doc = deepcopy(CONFIG_DOC)
                new_doc["server"]["last_sync"] = str(datetime.datetime.now())
                push_config_file(new_doc)

    HEARTBEAT_DAEMON = Thread(target=task, args=[period_in_sec])
    HEARTBEAT_DAEMON.start()


def get_config_doc():
    config_response = requests.get(CONFIG_FILE_ADDR)
    if config_response.status_code == 200:
        return config_response.json()
    log(f"config doc does not exist: {CONFIG_FILE_ADDR} {config_response.status_code}")
    exit(DB_ERROR_CODE)


def reset_global():
    """ reset global parameters """
    global CONFIG_FILE_ADDR, CONFIG_DOC, WORD2VEC_MODEL_NAME, ANALYSIS_VIEW_ADDR,\
        DB_ADDR, TWITTER_DB_ADDR, CONFIG_DB_ADDR, AURIN_DB_ADDR, CONFIG_FILE_ID
    CONFIG_DOC = get_config_doc()
    db_config = CONFIG_DOC['database']
    CONFIG_FILE_ID = CONFIG_DOC["_id"]
    DB_ADDR = f"http://{db_config['user']}:{db_config['password']}@" \
              f"{db_config['addr']}:{db_config['port']}"
    TWITTER_DB_ADDR = f"{DB_ADDR}/{db_config['twitter_db']}"
    AURIN_DB_ADDR = f"{DB_ADDR}/{db_config['aurin_db']}"
    CONFIG_DB_ADDR = f"{DB_ADDR}/{db_config['config_db']}"
    CONFIG_FILE_ADDR = f"{CONFIG_DB_ADDR}/{CONFIG_FILE_ID}"
    ANALYSIS_VIEW_ADDR = f"{DB_ADDR}/{CONFIG_DOC['server']['view']}"
    modelname = CONFIG_DOC["server"]["w2v_model"]
    if modelname != WORD2VEC_MODEL_NAME:
        WORD2VEC_MODEL_NAME = modelname
        reload_word2vec()


def reload_word2vec():
    global WORD2VEC_MODEL
    log("Starting download and load word2vec pretrained model.....")
    WORD2VEC_MODEL = w2v.load_model(WORD2VEC_MODEL_NAME)
    log("Finished word2vec loading.")


# ========================== UI-BACKEND ========================================
# create app
app = Flask(__name__)
CORS(app)   # add CORS support


@app.route("/word2vec", methods=["POST"])
def run_word2vec():
    add_request_static()
    global WORD2VEC_MODEL
    obj = request.get_json()
    sentence = obj["data"]
    vec = w2v.sentence2vec(sentence, model=WORD2VEC_MODEL)
    log(f"Recv word2vec: {sentence} :: {vec}")
    return {"data": vec}

@app.route("/twitter", methods=["PUT"])
def twitter():
    """ process a new tweet and save to  """
    add_request_static()
    global WORD2VEC_MODEL, POLYGON_METHOD
    tw = request.get_json()
    coords = tw["geometry"]["coordinates"]
    sa_code = polygon.get_sa_code(coords, method=POLYGON_METHOD)
    sentence = tw["properties"]["text"]
    vector = w2v.sentence2vec(sentence, model=WORD2VEC_MODEL)
    if "id" in tw:
        response = requests.put(f"http://{TWITTER_DB_ADDR}/{tw['id']}", json={
            "_id": tw["id"],
            "sa_code": sa_code,
            "geometry": tw["geometry"],
            "properties": tw["properties"],
            "vec": vector,
        })
    else:
        response = requests.post(f"http://{TWITTER_DB_ADDR}", json={
            "sa_code": sa_code,
            "geometry": tw["geometry"],
            "properties": tw["properties"],
            "vec": vector,
        })
    return response

@app.route("/", methods=["DELETE"])
def shutdown():
    """ shutdown server """
    log("receive shut down request")
    global HEARTBEAT_CONTROL
    HEARTBEAT_CONTROL["heartbeat"] = False  # stop heartbeat
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    exit(0)

@app.route("/config_doc", methods=["GET"])
def config_doc():
    add_request_static()
    with LOCK:
        return deepcopy(CONFIG_DOC)

@app.route("/polygon")
def get_polygon():
    pass

@app.route("/analysis", methods=["POST"])
def do_analysis():
    add_request_static()
    data = request.get_json()
    baseline = data["baseline"]
    baseline_vec = w2v.sentence2vec(baseline, model=WORD2VEC_MODEL)
    rst = analysis.get_zone_aggr_similarity(ANALYSIS_VIEW_ADDR, baseline_vec)
    if 'NaZ' in rst:
        del rst['NaZ']
    return rst


@app.route("/aurin/<doc:str>", methods=["GET"])
def aurin(doc):
    log("Recv AURIN")
    add_request_static()
    data = analysis.get_aurin_data(AURIN_DB_ADDR, doc)
    return data


# MONITOR server

def init(config_rev):
    # global control variables
    # check config file
    reset_global()
    if CONFIG_DOC["server"]["running"] or CONFIG_DOC["_rev"] != config_rev:
        log("Can't match existing config file or these is a server still running with this configue file.")
        exit(CONFIG_ERROR_CODE)
    new_doc = deepcopy(CONFIG_DOC)
    new_doc["server"]["running"] = True
    push_config_file(new_doc)


    # heartbeat_daemon.start()  # run heartbeat
    # log(f"listen on {CONFIG_DOC['server']['addr']}:{CONFIG_DOC['server']['port']}")
    # return app, heartbeat_daemon
    # app.run(host=CONFIG_DOC['server']['addr'], port=CONFIG_DOC['server']['port'], debug=True)

def create_monitor_daemon():
    def task():
        pass
    return Thread(target=task)


def create_and_run_monitor():
    app = Flask(__name__)
    CORS(app)  # add CORS support


if __name__ == "__main__":
    # global CONFIG_DOC, CONFIG_FILE_ADDR
    config_file_id = "backend0"
    db_addr = "http://admin:admin@172.26.134.68:5984/config"
    CONFIG_FILE_ADDR = f"{db_addr}/{config_file_id}"
    CONFIG_DOC = get_config_doc()
    log(CONFIG_DOC)
    init(CONFIG_DOC["_rev"])
    # heartbeat = create_heartbeat_daemon()
    create_and_run_heartbeat()
    # heartbeat.start()
    app.run(host=CONFIG_DOC["server"]["addr"], port=int(
        CONFIG_DOC['server']['port']), debug=False)
