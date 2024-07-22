import time
import requests
import base64
import pandas as pd
import json
import time
from AesEverywhere import aes256

url = 'https://api.infosimples.com/api/v2/consultas/ecac/situacao-fiscal'

# Lista de CNPJs
perfis = ["35985762000179",	"49125988000104",
]

for perfil in perfis:
    try:
      args = {
        "pkcs12_cert":            aes256.encrypt(base64.b64encode(open("C:\\Users\\conta\\Downloads\\S3D_4_240521114403.pfx", "rb").read()).decode(), "pubHoTc5dEwU6eTtpmwaawmECSPH2TQrrT-5tJ8z"),
        "pkcs12_pass":            aes256.encrypt("12345678", "pubHoTc5dEwU6eTtpmwaawmECSPH2TQrrT-5tJ8z"),
        "perfil_procurador_cnpj": perfil,
        "token":                  "odklhCcKzsww0J8axxNTjfjvnKRAU1SRXXJLGHiH",
        "timeout":                300
      }

      response = requests.post(url, args)
      response_json = response.json()
      response.close()

      if response_json['code'] == 200:
          print("Retorno com sucesso: ", response_json['data'])
      elif response_json['code'] in range(600, 799):
          mensagem = "Resultado sem sucesso. Leia para saber mais: \n"
          mensagem += "Código: {} ({})\n".format(response_json['code'], response_json['code_message'])
          mensagem += "; ".join(response_json['errors'])
          print(mensagem)

      # Salve o retorno em um arquivo JSON
      with open(f'{perfil}.json', 'w') as f:
          json.dump(response_json, f)

      print("Cabeçalho da consulta: ", response_json['header'])
      print("URLs com arquivos de visualização (HTML/PDF): ", response_json['site_receipts'])
    except Exception as e:
        print(f"Erro ao consultar o CNPJ {perfil}: {e}"
              f"\nVerifique se o certificado digital está correto e se o CNPJ é válido."
              f"\nSe o erro persistir, entre em contato com o suporte.")
    time.sleep(5)
    print("Próximo CNPJ:", perfil) 