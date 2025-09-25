import google.generativeai as genai
from fastapi import Depends
from typing_extensions import Annotated
from app.core.config import Settings, get_settings


def get_api_key(settings: Annotated[Settings, Depends(get_settings)]) -> str:
    return settings.gemini_api_key


genai.configure(api_key=get_api_key(get_settings()))

model = genai.GenerativeModel("gemini-2.0-flash")
