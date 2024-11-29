
# Elliptic Curve Cryptography
### ECC

ECC is widely used for cryptology purposes. </br>
It focuses on asymmetric cryptography using pairs of public and private keys. </br>
This type of cryptography is used for encryption and decryption of data, authentication, and digital signatures. <br />
Bitcoin and other cryptocurrencies use the private key and public key for digital signatures and validating transactions.<br />
 </br>
**Private key:**  </br>
The private key is just a big and random number. </br>
To generate a secure private key, you can use this [random entropy creator](https://github.com/tokimay/random_entropy).
 </br>
 </br>
**Public key:**  </br>
The public key is a coordinate calculated on the curve algorithm based on the private key.  </br>
There are 3 types of public key that are used:
+ Public key coordinate: a tuple containing x and y of coordinate
+ Un compressed public key: '04' + hex(x) + hex(y)
+ Compressed public key: '02' for even or '03' for odd x + hex(x)

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



