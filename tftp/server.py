import socket
import os
from tftp.protocol import create_error

from tftp.protocol import (
    RRQ,
    WRQ,
    DATA,
    ACK,
    BLOCK_SIZE,
    create_data,
    create_ack,
    create_error,
    parse_opcode,
)


class TFTPServer:

    def __init__(self, host: str = "0.0.0.0", port: int = 69):
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
            elif opcode == WRQ:
                self.handle_wrq(sock, data, addr)

    def handle_rrq(self, sock, data, addr):

        filename = data[2:].split(b"\0")[0].decode()

        print(f"Arquivo solicitado pelo cliente: {filename}")

        try:
            with open(filename, "rb") as f:

                block = 1

                while True:
                    chunk = f.read(BLOCK_SIZE)

                    packet = create_data(block, chunk)
                    
                    print(f"Sending block {block}")

                    sock.sendto(packet, addr)

                    ack, _ = sock.recvfrom(1024)

                    if len(chunk) < BLOCK_SIZE:
                        print(f"Envio do arquivo '{filename}' para o cliente concluído.")
                        break

                    block = (block + 1) % 65536

        except FileNotFoundError:
            print("Arquivo não encontrado")
            error_packet = create_error(1, "File not found")
            sock.sendto(error_packet, addr)

    def handle_wrq(self, sock, data, addr):
        filename = data[2:].split(b"\0")[0].decode()
        print(f"Cliente iniciou o upload do arquivo: {filename}")

        save_filename = f"server_{filename}"
        if os.path.exists(save_filename):
            print("Erro: arquivo já existe no servidor.")
            error_packet = create_error(6, "File already exists")
            sock.sendto(error_packet, addr)
            return
        ack = create_ack(0)
        sock.sendto(ack, addr)

        with open(save_filename, "wb") as f:
            while True:
                packet, client_addr = sock.recvfrom(1024)
                opcode = parse_opcode(packet)

                if opcode == DATA:
                    block = int.from_bytes(packet[2:4], "big")
                    chunk = packet[4:]
                    
                    f.write(chunk)

                    ack = create_ack(block)
                    sock.sendto(ack, client_addr)

                    if len(chunk) < BLOCK_SIZE:
                        print(f"Upload do arquivo '{save_filename}' finalizado.")
                        break