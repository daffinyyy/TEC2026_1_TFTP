import socket

from tftp.protocol import (
    RRQ,
    DATA,
    BLOCK_SIZE,
    create_data,
    parse_opcode,
)


class TFTPServer:

    def __init__(self, host: str = "0.0.0.0", port: int = 6969):
        self.host = host
        self.port = port

    def start(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))

        print(f"Servidor TFTP escutando em {self.host}:{self.port}")

        while True:
            data, addr = sock.recvfrom(1024)

            opcode = parse_opcode(data)

            if opcode == RRQ:
                self.handle_rrq(sock, data, addr)

    def handle_rrq(self, sock, data, addr):

        filename = data[2:].split(b"\0")[0].decode()

        print(f"Arquivo solicitado pelo cliente: {filename}")

        try:
            with open(filename, "rb") as f:

                block = 1

                while True:
                    chunk = f.read(BLOCK_SIZE)

                    packet = create_data(block, chunk)

                    sock.sendto(packet, addr)

                    ack, _ = sock.recvfrom(1024)

                    if len(chunk) < BLOCK_SIZE:
                        break

                    block += 1

        except FileNotFoundError:
            print("Arquivo não encontrado")