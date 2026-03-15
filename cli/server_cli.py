from tftp.server import TFTPServer


def main():
    server = TFTPServer()
    server.start()


if __name__ == "__main__":
    main()