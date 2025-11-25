# --- MÓDULO: items_db.py ---
# Aquí pegarás el código correspondiente al sistema de ITEMS_DB
# --- BASE DE DATOS DE ITEMS Y MATERIALES ---

ITEMS_DB = {
    # === MATERIALES DE ALQUIMIA ===
    # 'tags' define qué aporta al caldero (Elemento: Potencia)
    
    "Hierba Espiritual Común": {
        "tipo": "Material",
        "tags": {"Madera": 5, "Estabilidad": 10, "Vida": 2},
        "desc": "Hierba básica llena de vitalidad leve."
    },
    "Flor de Siete Colores": {
        "tipo": "Material",
        "tags": {"Fuego": 10, "Agua": 10, "Pureza": 20},
        "desc": "Rara flor que equilibra el Yin y el Yang."
    },
    "Raíz de Ginseng Sangriento": {
        "tipo": "Material",
        "tags": {"Vida": 50, "Sangre": 30, "Yang": 20},
        "desc": "Un ginseng que ha absorbido sangre de bestias durante 100 años."
    },
    "Loto del Volcán": {
        "tipo": "Material",
        "tags": {"Fuego": 50, "Destrucción": 10, "Pureza": 5},
        "desc": "Crece en lava. Quema al tacto."
    },
    "Fruto de Hielo Milenario": {
        "tipo": "Material",
        "tags": {"Hielo": 60, "Yin": 40, "Estabilidad": 20},
        "desc": "Congela el Qi para solidificar la base."
    },
    "Escoria Alquímica": {
        "tipo": "Basura",
        "tags": {"Impureza": 100},
        "desc": "Resultado de un fallo. Tóxico."
    },

    # === MATERIALES DE FORJA ===
    # 'stats_forja' define las propiedades base del arma resultante
    
    "Hierro Negro": {
        "tipo": "Metal",
        "stats_forja": {"dureza": 15, "conductividad": 5, "peso": 10},
        "afinidad": "Neutro",
        "desc": "Metal estándar para cultivadores."
    },
    "Acero de Sangre de Dragón": {
        "tipo": "Metal",
        "stats_forja": {"dureza": 40, "conductividad": 30, "peso": 15},
        "afinidad": "Fuego",
        "desc": "Metal forjado con sangre de dragón real."
    },
    "Plata Estelar": {
        "tipo": "Metal",
        "stats_forja": {"dureza": 25, "conductividad": 50, "peso": 5},
        "afinidad": "Espacio",
        "desc": "Metal ligero que canaliza Qi espacial."
    },
    "Hueso de Demonio": {
        "tipo": "Material",
        "stats_forja": {"dureza": 35, "conductividad": 10, "peso": 8},
        "afinidad": "Oscuridad",
        "desc": "Huesos malditos usados para armas viles."
    },
        "Hierro de Qi": {
        "tipo": "Metal",
        "stats_forja": {"dureza": 30, "conductividad": 40, "peso": 9},
        "afinidad": "Neutro",
        "desc": "Metal estándar para cultivadores."
    },

    # === CONSUMIBLES COMUNES ===
    "Píldora Curativa": {"tipo": "Consumible", "efecto": {"hp": 100}, "desc": "Restaura heridas leves."},
    "Píldora de Qi": {"tipo": "Consumible", "efecto": {"qi": 50}, "desc": "Recupera energía espiritual."},
    "Píldora de Fundación": {"tipo": "Consumible", "efecto": {"breakthrough_chance": 0.4}, "desc": "Aumenta la chance de llegar al Reino Fundación."},
    "Píldora de Longevidad": {"tipo": "Consumible", "efecto": {"lifespan": 25}, "desc": "Extiende la vida 25 años."},
    "Píldora de Lavado de Médula": {"tipo": "Consumible", "efecto": {"root_cleanse": True}, "desc": "Purifica Raíces Espirituales."}
}