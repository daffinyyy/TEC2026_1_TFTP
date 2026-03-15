import struct

RRQ = 1
WRQ = 2
DATA = 3
ACK = 4
ERROR = 5

BLOCK_SIZE = 512


def create_rrq(filename: str, mode: str = "octet") -> bytes:
    return (
        struct.pack("!H", RRQ)
        + filename.encode()
        + b"\0"
        + mode.encode()
        + b"\0"
    )


def create_data(block: int, data: bytes) -> bytes:
    return struct.pack("!HH", DATA, block) + data


def create_ack(block: int) -> bytes:
    return struct.pack("!HH", ACK, block)


def parse_opcode(packet: bytes) -> int:
    return struct.unpack("!H", packet[:2])[0]