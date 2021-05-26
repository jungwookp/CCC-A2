from http.client import NO_CONTENT
import pandas as pd
import numpy as np
import gensim.downloader as api
import json

__import__ = [
    "load_model",
    "sentence2vec",
    "similarity",
]

ZEROS = None

MODEL = None


def load_model(name):
    return api.load(name)


def sentence2vec(sentence, *, model=None):
    if model is None:
        model = MODEL
    rst = int(0)
    for word in sentence.split():
        try:
            rst += model.get_vector(word)
        except KeyError:
            pass
    if isinstance(rst, int):
        return ZEROS.tolist()
    return (rst/np.linalg.norm(rst)).tolist()


if __name__ == "__main__":
    MODEL_NAME = "glove-twitter-25"
    MODEL = api.load(MODEL_NAME)
    print(f"Model {MODEL_NAME} loaded")
    ZEROS = np.zeros_like(MODEL.get_vector("a"))

    def main():
        for bulk in range(32):
            in_file = f"./data/melb_{bulk}"
            out_file = f"./data/melb_vec_{bulk}"
            with open(in_file, 'r', encoding='utf8') as ifd:
                tweets = json.load(ifd)
            for tw in tweets:
                tw["vec"] = sentence2vec(tw["properties"]["text"])
            with open(out_file, 'w+') as ofd:
                json.dump(tweets, ofd)
            print(f"finished bulk {bulk}")

    main()
