def get_new_hash():
    import hashlib
    import os
    # Генерируем случайные байты
    random_bytes = os.urandom(16)

    # Используем hashlib для генерации хэша, например, с помощью SHA-256
    hash_obj = hashlib.sha256(random_bytes)

    # Получаем хэш в виде шестнадцатеричной строки
    hex_dig = hash_obj.hexdigest()

    # Обрезаем хэш до 10 символов
    short_hash = hex_dig[:10]
    print(f"Хэш: {short_hash}")
    return short_hash
