"""Day 16: Packet Decoder"""


import math
import operator
import os
from functools import reduce


INPUT = os.path.join(os.path.dirname(__file__), 'input')

# Type ID
SUM = 0
PRODUCT = 1
MINIMUM = 2
MAXIMUM = 3
LITERAL = 4
GREATER_THAN = 5
LESS_THAN = 6
EQUAL_TO = 7

# Length type ID
TOTAL_LENGTH_IN_BITS = 0
NUMBER_OF_SUB_PACKETS = 1


class Buffer:

    def __init__(self, data):
        self.data = data
        self.index = 0

    def __str__(self):
        return self.data[self.index:].__str__()

    def __bool__(self):
        return (
            self.index < len(self.data)
            and not all(n == '0' for n in self.data[self.index:])
        )

    def read(self, size):
        chunk = self.data[self.index:self.index + size]
        self.index += size
        return chunk

    def read_int(self, size):
        return int(self.read(size), 2)


class Packet:

    def __init__(self, packet):
        self.packet = packet

    def decode(self):
        buffer = Buffer(self._hex_to_bin(self.packet))
        return self._decode(buffer)[0]

    def _decode(self, buffer, num_packets=math.inf):
        packets = []
        while buffer and num_packets > 0:
            packet = {
                'version': buffer.read_int(3),
                'type_id': (type_id := buffer.read_int(3)),
            }
            if type_id == LITERAL:
                packet['value'] = self._decode_literal(buffer)
            else:
                packet['length_type_id'] = length_type_id = buffer.read_int(1)
                if length_type_id == TOTAL_LENGTH_IN_BITS:
                    packet['length'] = length = buffer.read_int(15)
                    packet['packets'] = self._decode(
                        Buffer(buffer.read(length))
                    )
                elif length_type_id == NUMBER_OF_SUB_PACKETS:
                    packet['num_packets'] = _num_packets = buffer.read_int(11)
                    packet['packets'] = self._decode(buffer, _num_packets)

            packets.append(packet)
            num_packets -= 1

        return packets

    @staticmethod
    def _decode_literal(buffer):
        number = []
        while True:
            data = buffer.read(5)
            number.append(data[1:])
            if data[0] == '0':
                break

        return int(''.join(number), 2)

    @staticmethod
    def _hex_to_bin(string):
        return bin(int(string, 16))[2:].zfill(len(string) * 4)


def sum_version(packet):
    def _sum(packets):
        if packets:
            return sum(
                packet['version'] + _sum(packet.get('packets'))
                for packet in packets
            )
        return 0

    return packet['version'] + _sum(packet.get('packets'))


def evaluate(packet):
    values = (
        sub_packet['value']
        if sub_packet['type_id'] == LITERAL else evaluate(sub_packet)
        for sub_packet in packet['packets']
    )

    if packet['type_id'] == SUM:
        return sum(values)

    if packet['type_id'] == PRODUCT:
        return reduce(operator.mul, values, 1)

    if packet['type_id'] == MINIMUM:
        return min(values)

    if packet['type_id'] == MAXIMUM:
        return max(values)

    if packet['type_id'] == LESS_THAN:
        first, second = values
        return 1 if first < second else 0

    if packet['type_id'] == GREATER_THAN:
        first, second = values
        return 1 if first > second else 0

    if packet['type_id'] == EQUAL_TO:
        first, second = values
        return 1 if first == second else 0


def parse(filename):
    with open(filename, encoding='utf-8') as input_file:
        return input_file.read().strip()


def test_sum_versions():
    examples = ('example4', 'example5', 'example6', 'example7')
    values = (16, 12, 23, 31)
    for example, expected in zip(examples, values):
        assert sum_version(Packet(parse(example)).decode()) == expected


def test_sum():
    assert evaluate(Packet(parse('example8')).decode()) == 3


def test_product():
    assert evaluate(Packet(parse('example9')).decode()) == 54


def test_minimum():
    assert evaluate(Packet(parse('example10')).decode()) == 7


def test_maximum():
    assert evaluate(Packet(parse('example11')).decode()) == 9


def test_less_than():
    assert evaluate(Packet(parse('example12')).decode()) == 1


def test_greater_than():
    assert evaluate(Packet(parse('example13')).decode()) == 0


def test_equal_to():
    assert evaluate(Packet(parse('example14')).decode()) == 0


def test_expression():
    assert evaluate(Packet(parse('example15')).decode()) == 1


def test_part1():
    assert sum_version(Packet(parse(INPUT)).decode()) == 860


def test_part2():
    assert evaluate(Packet(parse(INPUT)).decode()) == 470949537659
