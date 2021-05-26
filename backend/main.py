import argparse
import sys
import server


def createParser():
    parser = argparse.ArgumentParser(
        description="Integerated twitter processing and UI backend for CCC project"
    )
    parser.add_argument(
        "-d"
        "--database",
        dest="database",
        required=True,
        help="address of the database, user:password@ip_addr:port")
    parser.add_argument(
        "--twitter_database",
        dest="twitter_database",
        required=False,
        default="melbourne",
        help="database name of preprocessed twitters"
    )
    parser.add_argument(
        "--word2vec",
        dest="word2vec",
        required=False,
        default="glove-twitter-25",
        help="name of pretrained word2vec model used for calc vector of tweets,"   
             "@see https://radimrehurek.com/gensim/auto_examples/howtos/run_downloader_api.html#sphx-glr-auto-examples-howtos-run-downloader-api-py"
    )
    parser.add_argument(
        "--port",
        required=False,
        default="7701",
        help="inbound port for connection from frontend"
    )
    return parser


def main():
    args = sys.argv[1:]
    config_db_addr = args[0]
    config_file_id = args[1]


if __name__ == "__main__":
    parser = createParser()