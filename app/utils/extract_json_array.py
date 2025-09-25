import json
import re


def extract_json_array(text: str) -> list[dict]:
    """Extrae el primer array JSON válido de un string."""
    match = re.search(r"\[\s*{.*?}\s*]", text, re.DOTALL)
    if not match:
        raise ValueError("No se encontró un array JSON válido en la respuesta.")
    return json.loads(match.group(0))


def clean_json_from_markdown(text: str) -> str:
    """Limpia etiquetas como ```json ... ``` y devuelve solo el bloque JSON."""
    # Elimina encabezado ```json o ``` y cualquier texto fuera del array
    cleaned = re.sub(r"```json|```", "", text).strip()
    # Busca el primer array JSON
    match = re.search(r"\[\s*{.*?}\s*]", cleaned, re.DOTALL)
    if not match:
        raise ValueError("No se encontró un array JSON válido.")
    return match.group(0)
