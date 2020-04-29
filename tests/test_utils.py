from web3 import Web3

from contracts_lib_py.utils import split_signature


def test_split_signature():
    signature = b'\x19\x15!\xecwnX1o/\xdeho\x9a9\xdd9^\xbb\x8c2z\x88!\x95\xdc=\xe6\xafc' \
                b'\x0f\xe9\x14\x12\xc6\xde\x0b\n\xa6\x11\xc0\x1cvv\x9f\x99O8\x15\xf6f' \
                b'\xe7\xab\xea\x982Ds\x0bX\xd9\x94\xa42\x01'
    _signature = split_signature(Web3, signature=signature)
    assert _signature.v == 28
    assert _signature.r == b'\x19\x15!\xecwnX1o/\xdeho\x9a9\xdd9^\xbb\x8c2z\x88!\x95' \
                                b'\xdc=\xe6\xafc\x0f\xe9'
    assert _signature.s == b'\x14\x12\xc6\xde\x0b\n\xa6\x11\xc0\x1cvv\x9f\x99O8\x15' \
                                b'\xf6f\xe7\xab\xea\x982Ds\x0bX\xd9\x94\xa42'


