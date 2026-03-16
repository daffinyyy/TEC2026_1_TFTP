import socket

from tftp.protocol import (
    DATA,
    ACK,
    BLOCK_SIZE,
    create_wrq,
    create_rrq,
    create_data,
    create_ack,
    parse_opcode,
)


class TFTPClient:

    def __init__(self, server_ip: str, port: int = 69):
        self.server_ip = server_ip
        self.port = port

    def download(self, filename: str) -> None:
        
        print(f"Downloading {filename} from {self.server_ip}")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        rrq = create_rrq(filename)

        sock.sendto(rrq, (self.server_ip, self.port))

        save_filename = f"download_{filename}"

        with open(save_filename, "wb") as f:

            while True:

                data, addr = sock.recvfrom(1024)

                opcode = parse_opcode(data)

                if opcode == 5:
                    print("Erro recebido do servidor.")
                    return

                if opcode == DATA:

                    block = int.from_bytes(data[2:4], "big")
                    
                    print(f"Received block {block}")

                    chunk = data[4:]

                    f.write(chunk)

                    ack = create_ack(block)

                    sock.sendto(ack, addr)

                    if len(chunk) < BLOCK_SIZE:
                        print(f"Download do arquivo '{save_filename}' finalizado.")
                        break

    def upload(self, filename: str) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # 1. Envia requisição de escrita (WRQ)
        wrq = create_wrq(filename)
        sock.sendto(wrq, (self.server_ip, self.port))

        # 2. Aguarda o ACK 0 do servidor para começar a enviar
        data, server_addr = sock.recvfrom(1024)
        opcode = parse_opcode(data)

        if opcode == 5:
            print("Erro recebido do servidor: arquivo já existe.")
            return
        
        if opcode == ACK:
            block_ack = int.from_bytes(data[2:4], "big")
            if block_ack == 0:
                try:
                    with open(filename, "rb") as f:
                        block = 1
                        while True:
                            # Lê pedaços do arquivo do tamanho do BLOCK_SIZE (512 bytes)
                            chunk = f.read(BLOCK_SIZE)
                            
                            # 3. Cria e envia pacote de dados
                            packet = create_data(block, chunk)
                            sock.sendto(packet, server_addr)
                            
                            # 4. Aguarda ACK do servidor
                            ack_data, _ = sock.recvfrom(1024)
                            
                            # Condição de parada: último bloco menor que 512 bytes
                            if len(chunk) < BLOCK_SIZE:
                                print(f"Upload de '{filename}' concluído com sucesso.")
                                break
                            
                            block = (block + 1) % 65536
                            
                except FileNotFoundError:
                    print("Erro: Arquivo não encontrado para upload.") 