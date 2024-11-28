
__A = 0
__B = 7
__MOD = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
__BASE = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
          0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
__N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


def __is_on_curve(point: tuple[int, int]) -> bool:
    # if y ** 2 mod p = x **3 + ax + b mod p
    if (point[1] ** 2) % __MOD == ((point[0] ** 3) + (__A * point[0]) + __B) % __MOD:
        return True
    else:
        print('Point:')
        print(point)
        print('is not on curve')
        return False


def __get_inverse(_n):
    return pow(_n, -1, __MOD)


def __get_points_inverse(_p: tuple[int, int]) -> tuple[int, int]:
    _y = (_p[1] * -1) % __MOD
    p_1 = (_p[0], _y)
    return p_1


def __add(point_a: tuple[int, int], point_b: tuple[int, int]) -> tuple[int, int]:
    if __is_equal_to(point_a, point_b):  # is multiple
        # a = 0
        slope = ((3 * point_a[0] ** 2) + __A) * __get_inverse(_n=(2 * point_a[1])) % __MOD
    else:  # A is base B is poit
        slope = (point_b[1] - point_a[1]) * __get_inverse(_n=point_b[0] - point_a[0]) % __MOD

    x = (slope ** 2 - point_a[0] - point_b[0]) % __MOD
    y = (slope * (point_a[0] - x) - point_a[1]) % __MOD
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

def __private_key(private_key: str or int) -> int:
    if isinstance(private_key, str):
        try:
            if private_key.startswith('0x') or private_key.startswith('0X'):
                private_key = private_key[2:]
            if len(private_key) != 32 * 2:
                print('Private_key key length is not math bitcoin standards.')
            __pk = int(private_key, 16)
            return __pk
        except TypeError:
            raise TypeError
    elif isinstance(private_key, int):
        if len(hex(private_key)[2:]) != 32 * 2:
            print('Private_key key length is not math bitcoin standards.')
        return private_key
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


def public_key_coordinate(private_key: str or int) -> tuple[int, int] or None:
    try:
        private_key = __private_key(private_key)
        pk = __scalar_multiply(point=__BASE, repeat=private_key)
        if not __is_on_curve(pk):
            raise ValueError
        return pk
    except Exception as er:
        print(str(er))
        return None

def uncompressed_public_key(private_key: str or int) -> str or None:
    try:
        private_key = __private_key(private_key)
        pk = __scalar_multiply(point=__BASE, repeat=private_key)
        if not __is_on_curve(pk):
            raise ValueError
        return __uncompressed(pk)
    except Exception as er:
        print(str(er))
        return None

def compressed_public_key(private_key: str or int) -> str or None:
    try:
        private_key = __private_key(private_key)
        pk = __scalar_multiply(point=__BASE, repeat=private_key)
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
    return __BASE
