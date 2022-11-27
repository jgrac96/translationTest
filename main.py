"""
    Author: James Grace
        from https://www.educative.io/blog/python-fastapi-tutorial
        https://github.com/argosopentech/argos-translate
    Date: 15/11/2022
    Translation API based off ArgosTranslate (offline)
"""
from fastapi import FastAPI, APIRouter
import argostranslate.package
import argostranslate.translate

# setup API
app = FastAPI(
    title="TranslationAPI - Wrapper for ArgosTranslate",
    openapi_url="/openapi.json"
)

# setup translation API - install argos translate packages for all the languages in the appropriate directions

languages = ["EN", "DE", "IT", "FR", "ES"]
print(argostranslate.package.load_available_packages())
print(argostranslate.translate.get_installed_languages())


# setup API routing
api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    return {"msg": "Hello, World"}


@api_router.get("/translate/")
def translate(sourceLang: str, targetLang: str, word: str):
    try:
        # get the correct translation direction
        installedLanguages = argostranslate.translate.get_installed_languages()
        from_lang = list(filter(
            lambda x: x.code == sourceLang.lower(),
            installedLanguages))[0]
        to_lang = list(filter(
            lambda x: x.code == targetLang.lower(),
            installedLanguages))[0]
        translation = from_lang.get_translation(to_lang)
        translatedText = translation.translate(word)
        return {
            "translation": translatedText,
            "success": True
        }
    except:
        return {
            "translation": "",
            "success": False
        }


app.include_router(api_router)
