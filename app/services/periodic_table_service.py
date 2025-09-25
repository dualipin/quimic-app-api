import json
from pathlib import Path
from typing import List
from app.schemas.periodic_table_schema import ElementSchema
from .audio_service import get_audio_path, stream_audio_response  # noqa


def get_all_elements() -> List[ElementSchema]:
    """Carga todos los elementos desde el archivo JSON y los mapea a ElementSchema."""
    file_path = Path("app") / "statics" / "json" / "elements.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Definimos un diccionario de mapeo para evitar repeticiones y errores de escritura
    key_mapping = {
        "numeroAtomico": "atomicNumber",
        "pesoAtomico": "atomicWeight",
        "puntoEbullicion": "boilingPoint",
        "valencia": "valence",
        "puntoFusion": "meltingPoint",
        "simbolo": "symbol",
        "densidad": "density",
        "estructuraAtomica": "atomicStructure",
        "nombre": "name",
        "grupo": "group",
        "periodo": "period",
        "categoria": "category",
        "datoCurioso": "funFact",
        "imagen": "image",
    }

    elements_list: List[ElementSchema] = []
    for element_data in data.get("elementos", []):
        # Mapear las claves usando el diccionario de mapeo
        mapped_element = {
            key_mapping[old_key]: value
            for old_key, value in element_data.items()
            if old_key
            in key_mapping  # Asegurarse de que solo mapeamos claves que nos interesan
        }
        elements_list.append(
            ElementSchema(**mapped_element)
        )  # Crear una instancia de ElementSchema

    return elements_list
