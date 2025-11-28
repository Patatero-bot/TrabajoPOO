import hashlib

def generar_hash(texto):
    return hashlib.sha256(texto.encode()).hexdigest()