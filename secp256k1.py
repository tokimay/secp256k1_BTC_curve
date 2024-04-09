# secp256k1
___a = 0
___b = 7
# p hex = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
___mod = 115792089237316195423570985008687907853269984665640564039457584007908834671663
# x hex = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
# y hex = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
___base = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
           32670510020758816978083085130507043184471273380659243275938904335757337482424)
# n hex = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
___n = 115792089237316195423570985008687907852837564279074904382605163141518161494337


def ___is_equal_to(pointA: tuple, pointB: tuple):
    return pointA[0] == pointB[0] and pointA[1] == pointB[1]


def ___isOnCurve(point: tuple) -> bool:
    # if y ** 2 mod p = x **3 + ax + b mod p
    if (point[1] ** 2) % ___mod == ((point[0] ** 3) + (___a * point[0]) + ___b) % ___mod:
        return True
    else:
        print('Point:')
        print(point)
        print('is not on curve')
        return False


def ___get_inverse(n):
    return pow(n, -1, ___mod)


def ___getPointsInverse(_p: tuple) -> tuple:
    _y = (_p[1] * -1) % ___mod
    p_1 = (_p[0], _y)
    return p_1


def ___add(pointA: tuple, pointB: tuple) -> tuple:
    if ___is_equal_to(pointA, pointB):  # is multiple
        # a = 0
        slope = ((3 * pointA[0] ** 2) + ___a) * ___get_inverse(n=(2 * pointA[1])) % ___mod
    else:  # A is base B is poit
        slope = (pointB[1] - pointA[1]) * ___get_inverse(n=pointB[0] - pointA[0]) % ___mod

    x = (slope ** 2 - pointA[0] - pointB[0]) % ___mod
    y = (slope * (pointA[0] - x) - pointA[1]) % ___mod
    newPoint = (x, y)

    return newPoint  # Point(x, y)


def __multiply(pointA: tuple, base: tuple, repeat: int) -> tuple:
    point = ___add(pointA, base)
    for i in range(repeat - 2):
        point = ___add(point, base)
    return point


def ___scalar_multiply(point: tuple, repeat: int) -> tuple:
    point_double = point
    offset = 1
    previous_points = []
    while offset < repeat:
        previous_points.append((offset, point_double))
        if 2 * offset <= repeat:
            point_double = ___add(point_double, point_double)
            offset = 2 * offset
        else:
            next_offset = 1
            next_point = None
            for (previous_offset, previous_point) in previous_points:
                if previous_offset + offset <= repeat:
                    if previous_point[0] != point_double[0]:
                        next_offset = previous_offset
                        next_point = previous_point
            point_double = ___add(point_double, next_point)
            offset = offset + next_offset

    return point_double


def getPublicKeyCoordinate(privateKey: int) -> tuple:
    pk = ___scalar_multiply(point=___base, repeat=privateKey)
    if ___isOnCurve(___base) and ___isOnCurve(pk):
        return pk
    else:
        return ()


def multipy(repeat: int, point: tuple) -> tuple:
    pk = ___scalar_multiply(point=point, repeat=repeat)
    if ___isOnCurve(___base) and ___isOnCurve(pk):
        return pk
    else:
        return ()


def add(pointA: tuple, pointB: tuple) -> tuple:
    return ___add(pointA, pointB)


def n() -> int:
    return ___n


def g() -> tuple:
    return ___base
