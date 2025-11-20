import random

def generar_isbn13() -> str:
    prefijo = "978"
    grupo = str(random.randint(0, 9))
    editorial = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    titulo = ''.join([str(random.randint(0, 9)) for _ in range(3)])
    
    isbn_sin_digito = prefijo + grupo + editorial + titulo
    
    suma = 0
    for i, digito in enumerate(isbn_sin_digito):
        if i % 2 == 0:
            suma += int(digito)
        else:
            suma += int(digito) * 3
    
    digito_control = (10 - (suma % 10)) % 10
    
    isbn = f"{prefijo}-{grupo}-{editorial}-{titulo}-{digito_control}"
    return isbn

def generar_isbn10() -> str:
    grupo = str(random.randint(0, 9))
    editorial = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    titulo = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    
    isbn_sin_digito = grupo + editorial + titulo
    
    suma = 0
    for i, digito in enumerate(isbn_sin_digito):
        suma += int(digito) * (10 - i)
    
    digito_control = (11 - (suma % 11)) % 11
    digito_control_str = 'X' if digito_control == 10 else str(digito_control)
    
    isbn = f"{grupo}-{editorial}-{titulo}-{digito_control_str}"
    return isbn