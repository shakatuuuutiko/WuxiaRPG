# --- MÓDULO: beast_db_massive.py ---
# Aquí pegarás el código correspondiente al sistema de BEAST_DB_MASSIVE
# --- BASE DE DATOS TAXONÓMICA MASIVA ---

# 1. RAÍCES (La forma base de la criatura)
ROOT_CREATURES = [
    # Mamíferos
    "Lobo", "Oso", "Tigre", "León", "Pantera", "Ciervo", "Jabalí", "Mamut", 
    "Simio", "Gorila", "Rata", "Murciélago", "Zorro", "Lince", "Hiena", "Tejón",
    "Búfalo", "Rinoceronte", "Elefante", "Armadillo", "Chacal", "Comadreja",
    
    # Reptiles/Dracónidos
    "Sierpe", "Dragón", "Draco", "Basilisco", "Víbora", "Pitón", "Cocodrilo", 
    "Tortuga", "Camaleón", "Gecko", "Salamandra", "Guiverno", "Hidra", "Cobra",
    
    # Insectos/Arácnidos
    "Mantis", "Araña", "Escorpión", "Escarabajo", "Avispa", "Hormiga", "Ciempiés", 
    "Langosta", "Polilla", "Gusano", "Larva", "Tarántula", "Mosquito", "Escarabajo",
    
    # Aves
    "Águila", "Halcón", "Fénix", "Cuervo", "Buitre", "Búho", "Grulla", "Garza", 
    "Roc", "Grifo", "Harpía", "Cóndor", "Cisne", "Gaviota", "Colibrí",
    
    # Acuáticos
    "Ballena", "Tiburón", "Kraken", "Leviatán", "Cangrejo", "Pulpo", "Medusa", 
    "Anguila", "Carpa", "Sirena", "Hipocampo", "Delfín", "Mantarraya",
    
    # Mitología / Humanoides / Otros
    "Gólem", "Demonio", "Asura", "Yaksha", "Oni", "Troll", "Ogro", "Cíclope", 
    "Ent", "Driade", "Espectro", "Fantasma", "Sombra", "Vampiro", "Liche",
    "Gárgola", "Minotauro", "Centauro", "Quimera", "Wendigo", "Skinwalker", "Slime"
]

# 2. PREFIJOS DE FAMILIA (Definen la naturaleza biológica/mágica)
FAMILY_PREFIXES = [
    # Elementales
    "Piro", "Crio", "Electro", "Geo", "Aero", "Hidro", "Magma", "Hielo", "Fuego", "Trueno",
    # Materiales
    "Ferro", "Cristal", "Jade", "Óseo", "Lito", "Aureo", "Argenta", "Diamante", "Acero", "Rubí",
    # Conceptuales
    "Astra", "Necro", "Crono", "Psico", "Espiritu", "Sombra", "Luz", "Caos", "Santo", "Maldito",
    "Vacío", "Éter", "Sangre", "Toxina", "Peste", "Guerra", "Paz", "Sueño", "Pesadilla",
    # Características
    "Mega", "Giga", "Micro", "Titan", "Ciber", "Meca", "Bio", "Fungico", "Espino",
    "Coraza", "Velox", "Nocturno", "Solar", "Lunar", "Estelar", "Abisal", "Infernal"
]

# 3. SUFIJOS DE CULTIVO (Variantes de Poder y Rareza)
VARIANTS = {
    "Baja": [
        "Común", "de los Bosques", "de Cueva", "Salvaje", "Menor", "de Río",
        "Gris", "Pardo", "Manchado", "Rayado", "de Barro", "Vagabundo", "Débil",
        "de la Pradera", "Rastrero", "del Pantano"
    ],
    "Media": [
        "de Hierro Negro", "de Cobre", "Luchador", "Soldado", "Cazador",
        "de la Niebla", "Tóxico", "Acorazado", "Voraz", "Veloz", "Guardián",
        "de Sangre", "de Batalla", "Rabioso", "Astuto", "de la Noche"
    ],
    "Alta": [
        "de Jade Blanco", "Rey", "Emperador", "Anciano", "de Sangre Pura",
        "del Trueno Divino", "Inmortal", "de Tres Cabezas", "de Nueve Colas",
        "Devorador de Almas", "Rompe-Cielos", "del Vacío Infinito", "Soberano",
        "Milenario", "de Ojos Dorados", "Celestial"
    ],
    "Mítica": [
        "Dios", "Primordial", "del Génesis", "del Apocalipsis", "Santo",
        "Demoníaco Ancestral", "Avatar", "Hijo del Cielo", "Prohibido",
        "Destructor de Mundos", "Eterno", "Caótico", "del Origen"
    ]
}

# 4. ANATOMÍA (Loot Table Dinámico)
ANATOMY = {
    "Mamífero": ["Piel", "Colmillo", "Garra", "Corazón", "Carne", "Hueso", "Pelaje"],
    "Reptil":   ["Escama", "Vesícula", "Ojo", "Sangre Fría", "Cola", "Cuerno", "Garras"],
    "Insecto":  ["Caparazón", "Ala", "Antena", "Saco de Veneno", "Pata", "Ojo Compuesto", "Aguijón"],
    "Ave":      ["Pluma", "Pico", "Garra", "Molleja", "Ala", "Cresta", "Ojo de Águila"],
    "Acuático": ["Aleta", "Escama", "Branquia", "Perla", "Aceite", "Diente", "Tentáculo"],
    "Planta":   ["Raíz", "Savia", "Hoja", "Fruto", "Espina", "Flor", "Corteza"],
    "Mítico":   ["Cuerno", "Esencia", "Alma", "Escama Inversa", "Sangre Divina", "Cristal de Vida"],
    "Gólem":    ["Núcleo de Roca", "Polvo Arcano", "Esquirla", "Runa", "Corazón de Piedra"]
}