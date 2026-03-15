import argparse

from tftp.client import TFTPClient


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("server")
    parser.add_argument("command", choices=["get", "put"])
    parser.add_argument("filename")

    args = parser.parse_args()

    client = TFTPClient(args.server)

    if args.command == "get":
        client.download(args.filename)
    elif args.command == "put":
        client.upload(args.filename)


if __name__ == "__main__":
    main()