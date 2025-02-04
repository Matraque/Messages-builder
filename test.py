import requests
import json

API_KEY = "28dd324b1b444e88aa6f3f1d9d310d6d"

URL = f"https://openai-dev-fra-001.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-10-21"

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

system_message = {"role": "system", "content": 
    """
    Vous êtes un assistant IA intégré au logiciel Poly, développé par Lexis Nexis. Vos fonctionnalités sont exclusivement :

    - Fournir des informations sur les utilisateurs
    - Gérer des dossiers (récupération d’informations, création de dossier, facturation)
    - Fournir des informations sur les personnes physiques et morales
    - Rédiger des correspondances non juridiques (email, courrier, lettre, newsletter ou publication réseaux sociaux)
    - Traduire un texte. 

    Répondez avec concision à la demande de l’utilisateur, sauf dans les cas listés dans <exception> : refusez alors de répondre.
    
    <exception>
    Vous ne devez pas utiliser ou faire référence à des connaissances juridiques ou encyclopédiques comme l'histoire, la géographie ou les sciences.
    - Vous ne devez pas rédiger de documents juridiques, y compris les clauses ou articles de contrat, les résolutions, ou tout autre document ayant une portée légale.
    - Vous ne devez pas donner de conseils ou d'analyses juridiques.
    </exception>
    """}

user_input = """
Pouvez-vous m'aider à rédiger une lettre de motivation pour un emploi ?

"""
user_message = {"role": "user", "content": user_input}
messages = [system_message, user_message]

data = {
    "model": "gpt-4o",
    "messages": messages
}

try:
    response = requests.post(URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    response_data = response.json()
    
    if 'choices' in response_data and len(response_data['choices']) > 0:
        reply = response_data['choices'][0]['message']['content']
        print("Model reply:")
        print(reply)
    else:
        print("No reply from the model.")
        print(response_data)
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'An error occurred: {err}')