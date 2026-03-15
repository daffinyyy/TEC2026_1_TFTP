import socket

from tftp.protocol import (
    DATA,
    BLOCK_SIZE,
    create_rrq,
    create_ack,
    parse_opcode,
)


class TFTPClient:

    def __init__(self, server_ip: str, port: int = 6969):
        self.server_ip = server_ip
        self.port = port

    def download(self, filename: str) -> None:
        
        print(f"Downloading {filename} from {self.server_ip}")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        rrq = create_rrq(filename)

        sock.sendto(rrq, (self.server_ip, self.port))

        with open(filename, "wb") as f:

            while True:

                data, addr = sock.recvfrom(1024)

                opcode = parse_opcode(data)

                if opcode == DATA:

                    block = int.from_bytes(data[2:4], "big")
                    
                    print(f"Received block {block}")

                    chunk = data[4:]

                    f.write(chunk)

                    ack = create_ack(block)

                    sock.sendto(ack, addr)

                    if len(chunk) < BLOCK_SIZE:
                        break