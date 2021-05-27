import argparse


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
        "--config",
        "-c",
        dest="config_db",
        required=False,
        default="config",
        help="database name of config db"
    )
    
    parser.add_argument(
        "--config-file",
        "-f",
        dest="config_file",
        required=True,
        help="config file id usered to start the server"
    )
    
    parser.add_argument(
        "--config-rev",
        "-v",
        dest="config_rev",
        required=False,
        default=None,
        help="revision of the config file"
    )

    parser.add_argument(
        "--type",
        "-t",
        dest="type",
        default="ui",
        choices=["ui", "monitor"],
        help="type of server to run"
    )

    return parser


def main():
    parser = createParser()
    args = parser.parse_args()
    # args = vars(args)
    if args.type == 'ui':
        import server
        server.CONFIG_FILE_ADDR = f"{args.database}/{args.config_db}/{args.config_file}" 
        server.CONFIG_DOC = server.get_config_doc()
        rev = server.CONFIG_DOC['_rev'] if args.config_rev is None else args.config_rev
        server.init(rev)
        server.create_and_run_heartbeat()
        server.run()
    elif args.type == "monitor":
        import monitor
        pass
    else:
        raise ValueError(f"Unsupported server type {args.type}")

if __name__ == "__main__":
    """
    python main.py -d http://admin:admin@172.26.134.68:5984/ -f backend0
    """
    main()