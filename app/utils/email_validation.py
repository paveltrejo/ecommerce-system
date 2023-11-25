import requests
import json

"""
Para validar que un email no esta en blacklist ocuparemos un servicio llamado
abstract, este servicio tiene de forma gratuita hasta 100 consultas.
"""

abstract_base_url = "https://emailvalidation.abstractapi.com/v1"
ABSTRACT_API_KEY = "c9bd83683fbf4922863f9c10f7db6a6a"




def email_verification(email):
    querystring = {"email":email,"api_key":"c9bd83683fbf4922863f9c10f7db6a6a"}

    response = requests.request("GET", abstract_base_url, params=querystring)
    return json.loads(response.text)