usage:
````python
from secp256k1 import get_public_key_coordinate

public_key = get_public_key_coordinate(YOUR_PRIVATE_KEY)[0]
````

Example: <br />
````python 
from secp256k1 import get_public_key_coordinate

public_key_coordinate = get_public_key_coordinate(0x636678001c32339343b4ffadf02d1818e8a545926eebfdcf01f2b0f8573575c4)
public_key = public_key_coordinate[0]
print(public_key)
````

Result: <br />
````text
44866585412763965536104885134689245299327962125733546419544817742211528769243

Process finished with exit code 0
````



