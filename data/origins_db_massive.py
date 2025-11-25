# data/origins_db_massive.py

# 1. DESTINO (Prefijo): Define Stats Base y Suerte
ORIGIN_PREFIXES = {
    "Maldito":      {"luck": -20, "hp": -20, "desc": "El cielo te odia."},
    "Afortunado":   {"luck": 20, "gold": 100, "desc": "Encuentras dinero al caminar."},
    "Lisiado":      {"vel": -5, "def": -5, "comprension": 10, "desc": "Cuerpo débil, mente aguda."},
    "Genio":        {"comprension": 20, "qi": 50, "desc": "Aprendes x2 más rápido."},
    "Reencarnado":  {"comprension": 50, "luck": 10, "desc": "Recuerdos de otra vida."},
    "Exiliado":     {"atk": 10, "gold": 0, "desc": "Expulsado de tu hogar."},
    "Enfermizo":    {"hp": -30, "stamina": -20, "comprension": 15, "desc": "Tose sangre a menudo."},
    "Robusto":      {"hp": 50, "stamina": 50, "desc": "Nunca te enfermas."},
    "Hermoso":      {"luck": 10, "desc": "Tu rostro abre puertas."},
    "Feo":          {"luck": -5, "atk": 5, "desc": "Tu rostro asusta niños."},
    "Loco":         {"comprension": -10, "atk": 20, "desc": "Tu mente es un caos."},
    "Iluminado":    {"qi": 100, "comprension": 30, "desc": "Naciste rodeado de luz."},
    "Poseído":      {"qi": 50, "hp": -10, "desc": "Una voz habla en tu cabeza."},
    "Dormido":      {"stamina": 20, "desc": "Siempre tienes sueño."},
    "Borracho":     {"atk": 5, "comprension": -5, "desc": "Naciste entre barriles de vino."}
    # ... Puedes agregar cientos más
}

# 2. IDENTIDAD (Raíz): Define Inventario Inicial y Rol
ORIGIN_ROLES = {
    "Mendigo":      {"gold": 0, "inv": {"Cuenco": 1, "Palo": 1}, "stats": {"def": 5}},
    "Príncipe":     {"gold": 5000, "inv": {"Sello Real": 1, "Ropa de Seda": 1}, "stats": {"atk": 5}},
    "Esclavo":      {"gold": 0, "inv": {"Grilletes Rotos": 1}, "stats": {"hp": 20}},
    "Erudito":      {"gold": 50, "inv": {"Libro Clásico": 1, "Pincel": 1}, "stats": {"comprension": 10}},
    "Cazador":      {"gold": 20, "inv": {"Arco": 1, "Piel": 2}, "stats": {"atk": 10, "vel": 5}},
    "Comerciante":  {"gold": 500, "inv": {"Ábaco": 1}, "stats": {"luck": 5}},
    "Asesino":      {"gold": 100, "inv": {"Daga": 1, "Veneno": 1}, "stats": {"vel": 10, "atk": 10}},
    "Monje":        {"gold": 0, "inv": {"Rosario": 1}, "stats": {"def": 10, "qi": 20}},
    "Herrero":      {"gold": 100, "inv": {"Martillo": 1, "Hierro": 3}, "stats": {"atk": 15}},
    "Alquimista":   {"gold": 100, "inv": {"Caldero Pequeño": 1, "Hierba": 5}, "stats": {"qi": 10}},
    "Granjero":     {"gold": 10, "inv": {"Azada": 1, "Arroz": 10}, "stats": {"hp": 30}},
    "Vagabundo":    {"gold": 5, "inv": {"Mapa": 1, "Sombrero de Paja": 1}, "stats": {"stamina": 20}},
    "Huérfano":     {"gold": 2, "inv": {"Retrato de Padres": 1}, "stats": {"luck": -5}},
    "Bastardo":     {"gold": 50, "inv": {"Daga Noble": 1}, "stats": {"atk": 5}},
    "Discípulo":    {"gold": 20, "inv": {"Manual Básico": 1, "Espada de Madera": 1}, "stats": {"qi": 30}}
}

# 3. LEGADO (Sufijo): Define Objetos Raros o Talentos Ocultos
ORIGIN_SUFFIXES = {
    "Común":            {"inv": {}, "stats": {}},
    "de la Espada":     {"inv": {"Manual: Espada Básica": 1}, "stats": {"atk": 5}},
    "con un Anillo":    {"inv": {"Anillo Misterioso": 1}, "stats": {"luck": 10}}, # Tropo clásico
    "de Sangre Pura":   {"inv": {}, "stats": {"hp": 50}, "force_bloodline": True},
    "del Veneno":       {"inv": {"Píldora Tóxica": 3}, "stats": {"def": 5}},
    "de los Cielos":    {"inv": {}, "stats": {"qi": 100}, "force_root": "Celestial"},
    "Vengativo":        {"inv": {"Lista de Nombres": 1}, "stats": {"atk": 10}},
    "de Hueso":         {"inv": {}, "stats": {"def": 15}},
    "Místico":          {"inv": {"Amuleto Raro": 1}, "stats": {"comprension": 10}},
    "Caído":            {"inv": {"Arma Rota": 1}, "stats": {"qi": -20}},
    "de la Llama":      {"inv": {"Semilla de Fuego": 1}, "stats": {"atk": 5}},
    "Solitario":        {"inv": {}, "stats": {"comprension": 5, "luck": -5}}
}