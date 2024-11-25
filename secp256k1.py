# secp256k1
__a = 0
__b = 7
# p hex = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
__mod = 115792089237316195423570985008687907853269984665640564039457584007908834671663
# x hex = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
# y hex = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
__base = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
          32670510020758816978083085130507043184471273380659243275938904335757337482424)
# n hex = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
__n = 115792089237316195423570985008687907852837564279074904382605163141518161494337


def __is_equal_to(point_a: tuple, point_b: tuple):
    return point_a[0] == point_b[0] and point_a[1] == point_b[1]


def __is_on_curve(point: tuple) -> bool:
    # if y ** 2 mod p = x **3 + ax + b mod p
    if (point[1] ** 2) % __mod == ((point[0] ** 3) + (__a * point[0]) + __b) % __mod:
        return True
    else:
        print('Point:')
        print(point)
        print('is not on curve')
        return False


def __get_inverse(_n):
    return pow(_n, -1, __mod)


def __get_points_inverse(_p: tuple) -> tuple:
    _y = (_p[1] * -1) % __mod
    p_1 = (_p[0], _y)
    return p_1


def __add(point_a: tuple, point_b: tuple) -> tuple:
    if __is_equal_to(point_a, point_b):  # is multiple
        # a = 0
        slope = ((3 * point_a[0] ** 2) + __a) * __get_inverse(_n=(2 * point_a[1])) % __mod
    else:  # A is base B is poit
        slope = (point_b[1] - point_a[1]) * __get_inverse(_n=point_b[0] - point_a[0]) % __mod

    x = (slope ** 2 - point_a[0] - point_b[0]) % __mod
    y = (slope * (point_a[0] - x) - point_a[1]) % __mod
    new_point = (x, y)

    return new_point  # Point(x, y)


def __multiply(point_a: tuple, base: tuple, repeat: int) -> tuple:
    point = __add(point_a, base)
    for i in range(repeat - 2):
        point = __add(point, base)
    return point


def __scalar_multiply(point: tuple, repeat: int) -> tuple:
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


def get_public_key_coordinate(private_key: int) -> tuple:
    pk = __scalar_multiply(point=__base, repeat=private_key)
    if __is_on_curve(__base) and __is_on_curve(pk):
        return pk
    else:
        return ()


def multipy(repeat: int, point: tuple) -> tuple:
    pk = __scalar_multiply(point=point, repeat=repeat)
    if __is_on_curve(__base) and __is_on_curve(pk):
        return pk
    else:
        return ()


def add(point_a: tuple, point_b: tuple) -> tuple:
    return __add(point_a, point_b)


def n() -> int:
    return __n


def g() -> tuple:
    return __base
