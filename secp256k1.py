
# This file is part of https://github.com/tokimay/secp256k1_BTC_curve
# Copyright (C) 2016 https://github.com/tokimay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# This software is licensed under GPLv3. If you use or modify this project,
# you must include a reference to the original repository: https://github.com/tokimay/secp256k1_BTC_curve

__A = 0
__B = 7
__P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
__G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
       0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
__N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


def __is_on_curve(point: tuple[int, int]) -> bool:
    # if y ** 2 mod p = x **3 + ax + b mod p
    if (point[1] ** 2) % __P == ((point[0] ** 3) + (__A * point[0]) + __B) % __P:
        return True
    else:
        print('Point:')
        print(point)
        print('is not on curve')
        return False


def __get_inverse(_n):
    return pow(_n, -1, __P)


def __get_points_inverse(_p: tuple[int, int]) -> tuple[int, int]:
    _y = (_p[1] * -1) % __P
    p_1 = (_p[0], _y)
    return p_1


def __add(point_a: tuple[int, int], point_b: tuple[int, int]) -> tuple[int, int]:
    if __is_equal_to(point_a, point_b):  # is multiple
        # a = 0
        slope = ((3 * point_a[0] ** 2) + __A) * __get_inverse(_n=(2 * point_a[1])) % __P
    else:  # A is base B is poit
        slope = (point_b[1] - point_a[1]) * __get_inverse(_n=point_b[0] - point_a[0]) % __P

    x = (slope ** 2 - point_a[0] - point_b[0]) % __P
    y = (slope * (point_a[0] - x) - point_a[1]) % __P
    new_point = (x, y)

    return new_point  # Point(x, y)


def __multiply(point_a: tuple[int, int], base: tuple[int, int], repeat: int) -> tuple[int, int]:
    point = __add(point_a, base)
    for i in range(repeat - 2):
        point = __add(point, base)
    return point


def __scalar_multiply(point: tuple[int, int], repeat: int) -> tuple[int, int]:
    point_double = point
    offset = 1
    previous_points = []
    while offset < repeat:
        previous_points.append((offset, point_double))
        if 2 * offset <= repeat:
            point_double = __add(point_double, point_double)
            offset = 2 * offset
        else:
            next_offset = 1
            next_point = None
            for (previous_offset, previous_point) in previous_points:
                if previous_offset + offset <= repeat:
                    if previous_point[0] != point_double[0]:
                        next_offset = previous_offset
                        next_point = previous_point
            point_double = __add(point_double, next_point)
            offset = offset + next_offset

    return point_double


def __is_equal_to(point_a: tuple[int, int], point_b: tuple[int, int]):
    return point_a[0] == point_b[0] and point_a[1] == point_b[1]


def __normalize(hex_val: str or int) -> int:
    if isinstance(hex_val, str):
        try:
            int_val = int(hex_val, 16)
            return int_val
        except TypeError:
            raise TypeError
    elif isinstance(hex_val, int):
        return hex_val
    else:
        raise TypeError


def __uncompressed(pub_key_coordinate: tuple[int, int]) -> str:
    x = hex(pub_key_coordinate[0])[2:]
    y = hex(pub_key_coordinate[1])[2:]
    uc_pk = '04' + x + y
    if len(uc_pk) != (65 * 2):
        print('Public key length is not math bitcoin standards.')
    return uc_pk


def __compressed(pub_key_coordinate: tuple[int, int]) -> str:
    x = hex(pub_key_coordinate[0])[2:]
    if pub_key_coordinate[1] % 2 == 0:
        y = '02'
    else:
        y = '03'
    uc_pk = y + x
    if len(uc_pk) != (33 * 2):
        print('Public key length is not math bitcoin standards.')
    return uc_pk

def __legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def __tonelli(y2_modular):
    assert __legendre(y2_modular, __P) == 1, "not a square (mod p)"
    q = __P - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(y2_modular, (__P + 1) // 4, __P)
    for z in range(2, __P):
        if __P - 1 == __legendre(z, __P):
            break
    c = pow(z, q, __P)
    r = pow(y2_modular, (q + 1) // 2, __P)
    t = pow(y2_modular, q, __P)
    m = s
    # t2 = 0
    while (t - 1) % __P != 0:
        t2 = (t * t) % __P
        for i in range(1, m):
            if (t2 - 1) % __P == 0:
                break
            t2 = (t2 * t2) % __P
        b = pow(c, 1 << (m - i - 1), __P)
        r = (r * b) % __P
        c = (b * b) % __P
        t = (t * c) % __P
        m = i
    return r

def __get_y(x: int):
    y2_modular = ((x ** 3) + 7) % __P
    y = __tonelli(y2_modular)
    return y

def recover_public_key_coordinate(pub_key: str or int) -> tuple[int, int]:
    if isinstance(pub_key, str):
        pub_key = pub_key[2:] # remove prefix '02' or '03' or '04
    elif isinstance(pub_key, int):
        pub_key = hex(pub_key)[3:] # remove '0x' and prefix '2' or '3' or '4'
    else:
        raise ValueError

    pub_key = hex(__normalize(pub_key))[2:]
    x = None
    y = None
    if len(pub_key) == (32 * 2): # compressed
        x = int(pub_key, 16)
        y = __get_y(x)
    elif len(pub_key) == (64 * 2): # uncompressed
        x = int(pub_key[:64], 16)
        y = int(pub_key[64:], 16)
    else:
        print('public key length is not math bitcoin standards.')
    return x, y

def de_compressed(compressed_pk: str or int) -> str:
    if isinstance(compressed_pk, str):
        compressed_pk = compressed_pk[2:] # remove prefix '02' or '03'
    elif isinstance(compressed_pk, int):
        compressed_pk = hex(compressed_pk)[3:] # remove '0x' and prefix '2' or '3'
    else:
        raise ValueError
    if len(compressed_pk) != (32 * 2):
        print('Compressed public key length is not math bitcoin standards.')

    x = __normalize(compressed_pk)
    y = __get_y(x)
    uc_pk = '04' + hex(x)[2:] + hex(y)[2:]
    if len(uc_pk) != (65 * 2):
        print('Uncompressed public key length is not math bitcoin standards.')
    return uc_pk


def public_key_coordinate(private_key: str or int) -> tuple[int, int] or None:
    try:
        private_key = __normalize(private_key)
        if len(hex(private_key)[2:]) != 32 * 2:
            print('Private key length is not math bitcoin standards.')
        pk = __scalar_multiply(point=__G, repeat=private_key)
        if not __is_on_curve(pk):
            raise ValueError
        return pk
    except Exception as er:
        print(str(er))
        return None


def uncompressed_public_key(private_key: str or int) -> str or None:
    try:
        private_key = __normalize(private_key)
        if len(hex(private_key)[2:]) != 32 * 2:
            print('Private key length is not math bitcoin standards.')
        pk = __scalar_multiply(point=__G, repeat=private_key)
        if not __is_on_curve(pk):
            raise ValueError
        return __uncompressed(pk)
    except Exception as er:
        print(str(er))
        return None


def compressed_public_key(private_key: str or int) -> str or None:
    try:
        private_key = __normalize(private_key)
        if len(hex(private_key)[2:]) != 32 * 2:
            print('Private key length is not math bitcoin standards.')
        pk = __scalar_multiply(point=__G, repeat=private_key)
        if not __is_on_curve(pk):
            raise ValueError
        return __compressed(pk)
    except Exception as er:
        print(str(er))
        return None


def multipy(repeat: int, point: tuple[int, int]) -> tuple[int, int] or None:
    try:
        pk = __scalar_multiply(point=point, repeat=repeat)
        if __is_on_curve(pk):
            return pk
        else:
            raise ValueError
    except Exception as er:
        print(str(er))
        return None


def add(point_a: tuple[int, int], point_b: tuple[int, int]) -> tuple[int, int]:
    return __add(point_a, point_b)


def n() -> int:
    return __N


def g() -> tuple[int, int]:
    return __G
