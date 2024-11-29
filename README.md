
Example usage: <br />
````python 
import secp256k1

privateKey = 0x636678001c32339343b4ffadf02d1818e8a545926eebfdcf01f2b0f8573575c4

pub_key_coordinate = secp256k1.public_key_coordinate(privateKey)
print('public key  coordinate :', pub_key_coordinate)

uncompressed_pub_key = secp256k1.uncompressed_public_key(privateKey)
print('uncompressed public key:', uncompressed_pub_key)

compressed_pub_key = secp256k1.compressed_public_key(privateKey)
print('compressed  public  key:', compressed_pub_key)

print('\nReverse calculation', '-'*10)
de_compressed_pub_key = secp256k1.de_compressed(compressed_pub_key)
print('de compressed public key:', de_compressed_pub_key)
print(uncompressed_pub_key == de_compressed_pub_key)

recovered_coordinate = secp256k1.recover_public_key_coordinate(compressed_pub_key)
print('recovered public key coordinate:', recovered_coordinate)
print(pub_key_coordinate == recovered_coordinate)
````

Result: <br />
````text
public key  coordinate : (44866585412763965536104885134689245299327962125733546419544817742211528769243, 45871094679987590155060384166131592370080350379912042250811875565206608731444)
uncompressed public key: 0463319661bbd18fa0d40a35b3a81db3b360ea9e4482dc8b28e06f6def7263bedb656a1e9941fbeb3fa87d83748edd0032f967f5887be03678b00023b8f9a6dd34
compressed  public  key: 0263319661bbd18fa0d40a35b3a81db3b360ea9e4482dc8b28e06f6def7263bedb

Reverse calculation ----------
de compressed public key: 0463319661bbd18fa0d40a35b3a81db3b360ea9e4482dc8b28e06f6def7263bedb656a1e9941fbeb3fa87d83748edd0032f967f5887be03678b00023b8f9a6dd34
True
recovered public key coordinate: (44866585412763965536104885134689245299327962125733546419544817742211528769243, 45871094679987590155060384166131592370080350379912042250811875565206608731444)
True

Process finished with exit code 0
````



