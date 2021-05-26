from threading import RLock, Thread
import time
import datetime
from copy import deepcopy
import requests
from flask import request, Flask, g
from flask_cors import CORS
import word2vec as w2v
import polygon
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
            print(f"{CONFIG_FILE_ADDR}?rev={new_doc['_rev']}")
            res = requests.put(f"{CONFIG_FILE_ADDR}?rev={new_doc['_rev']}", json=new_doc)
            if res.status_code != 201:
                log("update config file failed: " + res.text + f" {res.status_code} ")
                exit(CONFIG_ERROR_CODE)
            # succ
            res_obj = res.json()
            CONFIG_DOC = new_doc
            CONFIG_DOC["_rev"] = res_obj["rev"]  # update revision
            return True


HEARTBEAT_CONTROL = {
    "heartbeat": True
}


def create_heartbeat_daemon(period_in_sec: int):
    def task(sec):
        while "heartbeat" in HEARTBEAT_CONTROL and HEARTBEAT_CONTROL["heartbeat"]:
            time.sleep(sec)
            with LOCK:
                new_doc = deepcopy(CONFIG_DOC)
                new_doc["server"]["last_sync"] = str(datetime.datetime.now())
                push_config_file(new_doc)
    return Thread(target=task, args=[period_in_sec])


def get_config_doc():
    config_response = requests.get(CONFIG_FILE_ADDR)
    if config_response.status_code == 200:
        return config_response.json()
    log(f"config doc does not exist: {CONFIG_FILE_ADDR} {config_response.status_code}")
    exit(DB_ERROR_CODE)


def reset_global():
    """ reset global parameters """
    global CONFIG_FILE_ADDR, CONFIG_DOC, WORD2VEC_MODEL_NAME,\
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


def reload_word2vec():
    global WORD2VEC_MODEL
    log("Starting download and load word2vec pretrained model.....")
    WORD2VEC_MODEL = w2v.load_model(WORD2VEC_MODEL_NAME)
    log("Finished word2vec loading.")


def create_and_run_app(config_rev):
    # global control variables
    # check config file
    reset_global()
    if CONFIG_DOC["server"]["running"] or CONFIG_DOC["_rev"] != config_rev:
        log("can't match existing config file.")
        exit(CONFIG_ERROR_CODE)

    # create app
    app = Flask(__name__)
    CORS(app)   # add CORS support
    heartbeat_daemon = create_heartbeat_daemon(int(CONFIG_DOC["server"]["heartbeat_period"]))

    @app.route("/word2vec", methods=["GET"])
    def word2vec():
        add_request_static()
        global WORD2VEC_MODEL
        obj = request.get_json()
        sentence = obj["data"]
        vec = w2v.sentence2vec(sentence, model=WORD2VEC_MODEL)
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

    # g["heartbeat"] = True
    heartbeat_daemon.run()  # run heartbeat
    app.run(host=f"{CONFIG_DOC['server']['addr']}:{CONFIG_DOC['server']['port']}", debug=True)


# MONITOR server
def create_monitor_daemon():
    def task():
        pass
    return Thread(target=task)


def create_and_run_monitor():
    app = Flask(__name__)
    CORS(app)  # add CORS support


if __name__ == "__main__":
    config_file_id = "backend0"
    db_addr = "http://admin:admin@172.26.134.68:5984/config"
    CONFIG_FILE_ADDR = f"{db_addr}/{config_file_id}"
    CONFIG_DOC = get_config_doc()
    print(CONFIG_DOC)
    create_and_run_app(CONFIG_DOC["_rev"])
