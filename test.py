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


