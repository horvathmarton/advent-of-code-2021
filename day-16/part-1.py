from __future__ import annotations
from os import path

# Code


class Packet:
    def __init__(self, content: str):
        self.version = int(content[:3], 2)
        self.type_id = int(content[3:6], 2)

        # Number 4 is the literal type.
        if self.type_id == 4:
            self.content, parsed_bits = self.__parse_literal(content[6:])
            self.length = 6 + parsed_bits
        else:
            self.content, parsed_bits = self.__parse_operator(content[6:])
            self.length = 6 + parsed_bits

    def __repr__(self) -> str:
        return f"Version: {self.version}, Type ID: {self.type_id}"

    @property
    def version_sum(self):
        if self.type_id == 4:
            return self.version
        else:
            return self.version + sum((packet.version_sum for packet in self.content))

    def __parse_literal(self, content: str) -> tuple[int, int]:
        stream = content
        values = []

        has_next = True
        while has_next:
            has_next = int(stream[0], 2)
            values.append(stream[1:5])
            stream = stream[5:]

        return int("".join(values), 2), len(content) - len(stream)

    def __parse_operator(self, content: str) -> tuple[list[Packet], int]:
        self.length_type_id = int(content[0], 2)
        if self.length_type_id:
            return self.__parse_type_one_operator(content[1:])

        else:
            return self.__parse_type_zero_operator(content[1:])

    def __parse_type_zero_operator(self, content: str) -> tuple[list[Packet], int]:
        payload_length = int(content[:15], 2)
        stream = content[15:]

        parsed_bits = 0
        payload = []
        while parsed_bits < payload_length:
            sub_packet = Packet(stream)
            payload.append(sub_packet)

            parsed_bits += sub_packet.length
            stream = stream[sub_packet.length :]

        return payload, 1 + 15 + parsed_bits

    def __parse_type_one_operator(self, content: str) -> tuple[list[Packet], int]:
        payload_count = int(content[:11], 2)
        stream = content[11:]

        parsed_bits = 0
        payload = []
        while len(payload) < payload_count:
            sub_packet = Packet(stream)
            payload.append(sub_packet)

            parsed_bits += sub_packet.length
            stream = stream[sub_packet.length :]

        return payload, 1 + 11 + parsed_bits


def hex_to_bytes(h: str) -> str:
    return "".join([bin(int(digit, 16))[2:].zfill(4) for digit in list(h)])


def read_file(name: str) -> str:
    with open(name) as f:
        return hex_to_bytes(f.read())


# Tests

input1 = "D2FE28"
bts1 = hex_to_bytes(input1)
assert bts1 == "110100101111111000101000"

packet1 = Packet(bts1)
assert packet1.version == 6
assert packet1.type_id == 4
assert packet1.content == 2021
assert packet1.length == 21

input2 = "38006F45291200"
bts2 = hex_to_bytes(input2)
assert bts2 == "00111000000000000110111101000101001010010001001000000000"

packet2 = Packet(bts2)
assert packet2.version == 1
assert packet2.type_id == 6
assert packet2.length_type_id == 0

assert len(packet2.content) == 2
assert packet2.content[0].length == 11
assert packet2.content[0].content == 10
assert packet2.content[1].length == 16
assert packet2.content[1].content == 20

input3 = "EE00D40C823060"
bts3 = hex_to_bytes(input3)
assert bts3 == "11101110000000001101010000001100100000100011000001100000"

packet3 = Packet(bts3)
assert packet3.version == 7
assert packet3.type_id == 3
assert packet3.length_type_id == 1

assert len(packet3.content) == 3
assert packet3.content[0].length == 11
assert packet3.content[0].content == 1
assert packet3.content[1].length == 11
assert packet3.content[1].content == 2
assert packet3.content[2].length == 11
assert packet3.content[2].content == 3

packet4 = Packet(hex_to_bytes("8A004A801A8002F478"))
assert packet4.version_sum == 16

packet5 = Packet(hex_to_bytes("620080001611562C8802118E34"))
assert packet5.version_sum == 12

packet6 = Packet(hex_to_bytes("C0015000016115A2E0802F182340"))
assert packet6.version_sum == 23

packet7 = Packet(hex_to_bytes("A0016C880162017C3686B18A3D4780"))
assert packet7.version_sum == 31

# Result

bts = read_file(path.join(path.dirname(__file__), "./input.txt"))
packet = Packet(bts)
print(packet.version_sum)
