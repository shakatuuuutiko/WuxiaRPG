# data/origins_db.py

ORIGIN_PREFIXES = {
    "Maldito": {"stats": {"luck": -10, "hp": -20}, "desc": "El cielo te odia."},
    "Genio": {"stats": {"comprension": 20, "qi": 50}, "desc": "Talento natural."},
    "Exiliado": {"stats": {"atk": 10}, "gold": 0, "desc": "Sin hogar."},
    "Afortunado": {"stats": {"luck": 20}, "gold": 100, "desc": "Nacido con estrella."}
}

ORIGIN_ROLES = {
    "Mendigo": {"gold": 0, "inv": {"Cuenco Roto": 1}, "stats": {"def": 5}},
    "Príncipe": {"gold": 2000, "inv": {"Sello Real": 1}, "stats": {"atk": 5}},
    "Esclavo": {"gold": 0, "inv": {"Grilletes": 1}, "stats": {"hp": 20}},
    "Erudito": {"gold": 50, "inv": {"Libro": 1}, "stats": {"comprension": 10}},
    "Cazador": {"gold": 20, "inv": {"Arco": 1, "Piel": 2}, "stats": {"atk": 10}}
}

ORIGIN_SUFFIXES = {
    "Común": {"inv": {}, "stats": {}},
    "de la Espada": {"inv": {"Manual: Espada Básica": 1}, "stats": {"atk": 5}},
    "con un Anillo": {"inv": {"Anillo Misterioso": 1}, "stats": {"luck": 10}},
    "de Sangre Pura": {"inv": {}, "stats": {"hp": 50}, "force_bloodline": True}
}