#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Procedural de Lugares
Crea ciudades, templos, dungeons, sectas, pueblos y otros lugares
con nombres y características procedurales aleatorios.
"""

import random
import json
import os

# ============================================================================
# BASES DE DATOS PROCEDURALES
# ============================================================================

# Palabras para generar nombres
PREFIJOS = {
    "pueblo": ["Pueblo", "Villa", "Aldea", "Caserío"],
    "ciudad": ["Ciudad", "Metrópoli", "Urbe"],
    "secta": ["Secta", "Orden", "Templo Secreto", "Congregación"],
    "templo": ["Templo", "Santuario", "Monasterio", "Altar"],
    "dungeon": ["Ruinas de", "Catacumbas de", "Mazmorra de", "Cavernas de", "Torre de"],
    "castillo": ["Fortaleza", "Castillo", "Bastión", "Torre Negra"],
}

ELEMENTOS_PUEBLO = [
    "Tranquilo", "Próspero", "Antiguo", "Nuevo", "Humilde",
    "Florido", "Rocoso", "Costeño", "Montañoso", "Ribereño"
]

ELEMENTOS_CIUDAD = [
    "Dorada", "Plateada", "Antigua", "Nueva", "Sagrada",
    "Maldita", "Flotante", "Invisible", "Eterna", "Perdida"
]

ELEMENTOS_SECTA = [
    "Nube", "Dragón", "Fénix", "Tigre", "Serpiente",
    "Espada", "Vacío", "Abismo", "Luz", "Sombra",
    "Sangre", "Hueso", "Alma", "Espíritu", "Demonio"
]

ELEMENTOS_TEMPLO = [
    "Luminoso", "Sombrío", "Sagrado", "Profano", "Antiguo",
    "Dorado", "Plateado", "Cristalino", "Oculto", "Eterno"
]

ELEMENTOS_DUNGEON = [
    "Perdido", "Olvidado", "Maldito", "Sagrado", "Prohibido",
    "Eterno", "Abismal", "Celestial", "Demoníaco", "Ancestral"
]

ELEMENTOS_AMBIENTE = {
    "pueblo": ["en el Valle", "en la Llanura", "en la Orilla", "en el Oasis", "en la Colina"],
    "ciudad": ["en las Montañas", "en la Costa", "en el Desierto", "en el Bosque", "en la Isla"],
    "secta": ["de la Cumbre", "del Abismo", "de las Nubes", "del Vacío", "de los Reinos Oscuros"],
    "templo": ["Bajo Tierra", "en la Cima", "en el Templo Perdido", "en la Dimensión Oculta"],
    "dungeon": ["bajo el Mundo", "en la Brecha", "en el Tiempo Perdido", "en el Sueño Eterno"],
}

RAZAS_HABITANTES = ["Humanos", "Demonios", "Celestiales", "Bestias Espirituales", "Inmortales", "Híbridos"]
ARQUITECTURAS = ["Madera", "Piedra", "Cristal", "Metal Espiritual", "Energía Pura"]
CLIMA = ["Tropical", "Árido", "Templado", "Frío", "Tóxico", "Sagrado"]

# ============================================================================
# GENERADOR
# ============================================================================

class LocationGenerator:
    """Generador procedural de lugares."""
    
    def __init__(self, seed=None):
        if seed:
            random.seed(seed)
        self.generated = set()
    
    def gen_nombre_pueblo(self):
        """Genera nombre para un pueblo."""
        prefijo = random.choice(PREFIJOS["pueblo"])
        elemento = random.choice(ELEMENTOS_PUEBLO)
        ambiente = random.choice(ELEMENTOS_AMBIENTE["pueblo"])
        return f"{prefijo} {elemento} {ambiente}"
    
    def gen_nombre_ciudad(self):
        """Genera nombre para una ciudad."""
        prefijo = random.choice(PREFIJOS["ciudad"])
        elemento = random.choice(ELEMENTOS_CIUDAD)
        ambiente = random.choice(ELEMENTOS_AMBIENTE["ciudad"])
        return f"{prefijo} {elemento} {ambiente}"
    
    def gen_nombre_secta(self):
        """Genera nombre para una secta."""
        prefijo = random.choice(PREFIJOS["secta"])
        elemento = random.choice(ELEMENTOS_SECTA)
        ambiente = random.choice(ELEMENTOS_AMBIENTE["secta"])
        return f"{prefijo} {elemento} {ambiente}"
    
    def gen_nombre_templo(self):
        """Genera nombre para un templo."""
        prefijo = random.choice(PREFIJOS["templo"])
        elemento = random.choice(ELEMENTOS_TEMPLO)
        ambient = random.choice(ELEMENTOS_AMBIENTE["templo"])
        return f"{prefijo} {elemento} {ambient}"
    
    def gen_nombre_dungeon(self):
        """Genera nombre para un dungeon."""
        prefijo = random.choice(PREFIJOS["dungeon"])
        elemento = random.choice(ELEMENTOS_DUNGEON)
        ambient = random.choice(ELEMENTOS_AMBIENTE["dungeon"])
        return f"{prefijo} {elemento} {ambient}"
    
    def gen_descripcion_pueblo(self, nombre):
        """Genera descripción para un pueblo."""
        raza = random.choice(RAZAS_HABITANTES)
        arquitectura = random.choice(ARQUITECTURAS)
        clima = random.choice(CLIMA)
        
        descripciones = [
            f"Un pueblo construido en {arquitectura} donde habitan {raza}. El clima {clima} define su carácter.",
            f"Tranquilo asentamiento {raza} bajo clima {clima}. Las casas de {arquitectura} conforman su estructura.",
            f"Pueblo ancestral de {raza} con arquitectura de {arquitectura}. Influenciado por clima {clima}.",
        ]
        return random.choice(descripciones)
    
    def gen_descripcion_ciudad(self, nombre):
        """Genera descripción para una ciudad."""
        raza = random.choice(RAZAS_HABITANTES)
        arquitectura = random.choice(ARQUITECTURAS)
        clima = random.choice(CLIMA)
        
        descripciones = [
            f"Metrópolis de {raza} con imponentes estructuras de {arquitectura}. El clima {clima} la rodea con misterio.",
            f"Gran ciudad construida por {raza} usando {arquitectura}. Bajo clima {clima}, prospera como centro de poder.",
            f"Urbs legendaria donde {raza} dominan. Arquitectura de {arquitectura} refleja su gloria. Clima: {clima}.",
        ]
        return random.choice(descripciones)
    
    def gen_descripcion_secta(self, nombre):
        """Genera descripción para una secta."""
        camino = random.choice(["verdad", "poder", "sombra", "luz", "vacío", "sangre"])
        tecnica = random.choice(["Qi Ancestral", "Técnicas Olvidadas", "Magia Prohibida", "Cultivo Demoníaco", "Iluminación Celestial"])
        
        descripciones = [
            f"Orden dedicada al cultivo del camino de {camino}. Práctica de {tecnica} es su especialidad.",
            f"Secta rodeada de misterio que busca {camino}. Sus miembros dominan {tecnica}.",
            f"Congregación de cultivadores obsesionados con {camino}. Utilizan {tecnica} para ascender.",
        ]
        return random.choice(descripciones)
    
    def gen_descripcion_templo(self, nombre):
        """Genera descripción para un templo."""
        deidad = random.choice(["antiguos dioses", "fuerzas celestiales", "espíritus ancestrales", "inmortales olvidados"])
        poder = random.choice(["purificación", "bendición", "maldición", "revelación", "transmutación"])
        
        descripciones = [
            f"Templo sagrado dedicado a {deidad}. Se dice que otorga {poder} a los dignos.",
            f"Santuario donde habitan {deidad}. Sus poderes de {poder} atraen peregrinos de todo el mundo.",
            f"Templo milenario consagrado a {deidad}. Fuente de {poder} y sabiduría perdida.",
        ]
        return random.choice(descripciones)
    
    def gen_descripcion_dungeon(self, nombre):
        """Genera descripción para un dungeon."""
        contenido = random.choice(["tesoros olvidados", "bestias ancestrales", "secretos del pasado", "poder prohibido"])
        peligro = random.choice(["trampas mortales", "maldiciones antiguas", "guardianes despiadados", "energía corrupta"])
        
        descripciones = [
            f"Mazmorra llena de {contenido}. Protegida por {peligro}. Solo los más valientes se aventuran aquí.",
            f"Ruinas que contienen {contenido}. Pero cuidado: {peligro} acecha en las sombras.",
            f"Lugar de leyenda donde yace {contenido}. Sin embargo, {peligro} lo resguarda celosamente.",
        ]
        return random.choice(descripciones)
    
    def gen_npcs_pueblo(self):
        """Genera NPCs para un pueblo."""
        profesiones = [
            "Vendedor Local", "Posadero", "Herrero", "Curandera",
            "Maestro de Artes Marciales", "Granjero", "Comerciante"
        ]
        return random.sample(profesiones, random.randint(2, 4))
    
    def gen_npcs_ciudad(self):
        """Genera NPCs para una ciudad."""
        profesiones = [
            "Gobernador", "Consejero", "Guardián de la Ciudad", "Comerciante Maestro",
            "Bibliotecario", "Alquimista", "Guerrero de Élite", "Diplomático",
            "Investigador Secreto", "Maestro Gremio"
        ]
        return random.sample(profesiones, random.randint(3, 6))
    
    def gen_npcs_secta(self):
        """Genera NPCs para una secta."""
        rangos = [
            "Patriarca", "Matriarca", "Elder Senior", "Elder Menor",
            "Instructor de Cultivo", "Guardián de los Secretos", "Discípulo Destacado",
            "Guardián de Entrada", "Custodio de Reliquias"
        ]
        return random.sample(rangos, random.randint(3, 5))
    
    def gen_npcs_templo(self):
        """Genera NPCs para un templo."""
        roles = [
            "Sumo Sacerdote", "Sacerdotisa", "Guardián Sagrado",
            "Monje Meditador", "Portador de la Llave",
            "Custodio del Templo", "Aprendiz Sagrado"
        ]
        return random.sample(roles, random.randint(2, 4))
    
    def gen_npcs_dungeon(self):
        """Genera NPCs para un dungeon."""
        habitantes = [
            "Espíritu Guardián", "Bestia Ancestral", "Esqueleto Maldito",
            "Guardián Automático", "Fantasma del Pasado"
        ]
        return random.sample(habitantes, random.randint(1, 3))
    
    def gen_nivel(self, tipo):
        """Genera nivel de dificultad basado en tipo."""
        niveles = {
            "pueblo": (1, 5),
            "ciudad": (5, 15),
            "secta": (10, 30),
            "templo": (15, 35),
            "dungeon": (20, 50),
            "castillo": (25, 45),
        }
        minimo, maximo = niveles.get(tipo, (1, 10))
        return random.randint(minimo, maximo)
    
    def gen_ubicacion(self):
        """Genera coordenadas de ubicación."""
        return [random.randint(-2000, 2000), random.randint(-2000, 2000)]
    
    def generar_lugar(self, tipo=None):
        """Genera un lugar completo."""
        if tipo is None:
            tipo = random.choice(["pueblo", "ciudad", "secta", "templo", "dungeon", "castillo"])
        
        # Generar nombre
        if tipo == "pueblo":
            nombre = self.gen_nombre_pueblo()
            descripcion = self.gen_descripcion_pueblo(nombre)
            npcs = self.gen_npcs_pueblo()
        elif tipo == "ciudad":
            nombre = self.gen_nombre_ciudad()
            descripcion = self.gen_descripcion_ciudad(nombre)
            npcs = self.gen_npcs_ciudad()
        elif tipo == "secta":
            nombre = self.gen_nombre_secta()
            descripcion = self.gen_descripcion_secta(nombre)
            npcs = self.gen_npcs_secta()
        elif tipo == "templo":
            nombre = self.gen_nombre_templo()
            descripcion = self.gen_descripcion_templo(nombre)
            npcs = self.gen_npcs_templo()
        elif tipo == "dungeon":
            nombre = self.gen_nombre_dungeon()
            descripcion = self.gen_descripcion_dungeon(nombre)
            npcs = self.gen_npcs_dungeon()
        else:  # castillo
            nombre = f"Castillo {random.choice(ELEMENTOS_CIUDAD)} {random.choice(ELEMENTOS_AMBIENTE['ciudad'])}"
            descripcion = f"Fortaleza protegida por antiguos guardianes. Centro de poder y autoridad."
            npcs = ["Señor del Castillo", "Capitán de la Guardia", "Tesorero"]
        
        # Evitar duplicados
        if nombre in self.generated:
            return self.generar_lugar(tipo)
        self.generated.add(nombre)
        
        lugar = {
            "Lugar": nombre,
            "tipo": tipo,
            "nivel": self.gen_nivel(tipo),
            "NPCs": npcs,
            "descripcion": descripcion,
            "coordenadas": self.gen_ubicacion(),
        }
        
        return lugar
    
    def generar_multiples(self, cantidad=15, distribucion=None):
        """Genera múltiples lugares."""
        if distribucion is None:
            distribucion = {
                "pueblo": 4,
                "ciudad": 2,
                "secta": 3,
                "templo": 2,
                "dungeon": 3,
                "castillo": 1,
            }
        
        lugares = []
        for tipo, cant in distribucion.items():
            for _ in range(cant):
                lugares.append(self.generar_lugar(tipo))
        
        return lugares


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 80)
    print("GENERADOR PROCEDURAL DE LUGARES - WuxiaRPG")
    print("=" * 80)
    
    # Crear generador
    gen = LocationGenerator()
    
    print("\nGenerando 15 lugares procedurales...")
    lugares = gen.generar_multiples(15)
    
    # Guardar en JSON
    lugares_path = os.path.join(os.path.dirname(__file__), 'Lugares.json')
    
    print(f"\nGuardando en: {lugares_path}")
    with open(lugares_path, 'w', encoding='utf-8') as f:
        json.dump(lugares, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Guardado: {len(lugares)} lugares")
    
    # Mostrar resumen
    print("\n" + "=" * 80)
    print("RESUMEN DE LUGARES GENERADOS")
    print("=" * 80)
    
    by_type = {}
    for lugar in lugares:
        tipo = lugar["tipo"]
        by_type[tipo] = by_type.get(tipo, 0) + 1
    
    for tipo, count in sorted(by_type.items()):
        print(f"\n{tipo.upper()}: {count}")
        for lugar in sorted([l for l in lugares if l["tipo"] == tipo], key=lambda x: x["Lugar"]):
            print(f"  • {lugar['Lugar']}")
            print(f"    Nivel: {lugar['nivel']}")
            print(f"    NPCs: {', '.join(lugar['NPCs'][:2])}...")
            print(f"    {lugar['descripcion'][:60]}...")
    
    print("\n" + "=" * 80)
    print(f"Total: {len(lugares)} lugares generados exitosamente")
    print("=" * 80)

if __name__ == "__main__":
    main()
