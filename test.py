import requests
import json

API_KEY = "28dd324b1b444e88aa6f3f1d9d310d6d"

URL = f"https://openai-dev-fra-001.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-06-01"

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

system_message = {"role": "system", "content": 
    """
que souhaite faire l'utilisateur avec le document partagé dans cet historique de conversation entre un utilisateur et son assistant ?  
    """}

user_input = """
            {
                {
            "Role": "User",
            "Content": "Bonjour",
            "CreatedDate": "2025-02-03T11:04:42.8305448+00:00",
            "IsHidden": true,
            "IsSummarized": false,
            "Error": null,
            "Metadata": null
        },
        {
            "Role": "Assistant",
            "Content": "Bonjour, comment puis-je vous aider aujourd'hui ?",
            "CreatedDate": "2025-02-03T11:04:42.9111968+00:00",
            "IsHidden": true,
            "IsSummarized": false,
            "Error": null,
            "Metadata": null
        },
        {
            "Role": "User",
            "Content": "Crée un dossier",
            "CreatedDate": "2025-02-03T11:04:44.1377947+00:00",
            "IsHidden": false,
            "IsSummarized": false,
            "Error": null,
            "Metadata": null
        },
                {
            "Role": "Assistant",
            "Content": "pour cela j'ai besoin de plus d'informations", comme la forme juridique de la socité et son numero siren"
            "CreatedDate": "2025-02-03T11:04:42.9111968+00:00",
            "IsHidden": true,
            "IsSummarized": false,
            "Error": null,
            "Metadata": null
        },
            "Role": "document",
            "Content": "[Répondez à la requête à partir du document suivant.]\r\n        SINON\r\n        [Si aucune requête utilisateur n'est spécifiée, demandez à l'utilisateur de préciser son intention. Si le document contient des informations sur une société, proposez à l'utilisateur de créer un dossier à partir du document.]\r\n\r\n        Document :\"\"\"Greffe du Tribunal de Commerce de Nantes\nIMMEUBLE RHUYS                                            Code de vérification : slsz24kcdR\n2BIS QU FRANCOIS MITTERRAND                               https://controle.infogreffe.fr/controle\nBP 86209\n44262 NANTES CEDEX 2\nN° de gestion 2009B02406\n                                                Extrait Kbis\n\n     EXTRAIT D'IMMATRICULATION PRINCIPALE AU REGISTRE DU COMMERCE ET DES SOCIETES\n                                          à jour au 6 novembre 2024\n\nIDENTIFICATION DE LA PERSONNE MORALE\nImmatriculation au RCS, numéro             518 452 750 R.C.S. Nantes\nDate d'immatriculation                     01/12/2009\n\nDénomination ou raison sociale             ISATEC\nForme juridique                            Société à responsabilité limitée (Société à associé unique)\nCapital social                             100 000,00 Euros\n\nAdresse du siège                           parc d'Activités du Verger 405 allée des Fruitiers 44690 La Haye\n                                           Fouassiere \n\nNomenclature d'activités française (code NAF) 7112B\nDurée de la personne morale                Jusqu'au 30/11/2108\nDate de clôture de l'exercice social       31 décembre\n\nGESTION, DIRECTION, ADMINISTRATION, CONTROLE, ASSOCIES OU MEMBRES\nGérant - Associé unique\n      Nom, prénoms                         RIVIERE Didier Jacques\n      Date et lieu de naissance            Le 03/03/1966 à CARMAUX  (81)  \n      Nationalité                          Française\n      Domicile personnel                   15 route de la fontenelle 44120 Vertou \n\nRENSEIGNEMENTS RELATIFS A L'ACTIVITE ET A L'ETABLISSEMENT PRINCIPAL\nAdresse de l'établissement                 parc d'Activités du Verger 405 allée des Fruitiers 44690 La Haye\n                                           Fouassiere \n\nNom commercial                             ISATEC\n\nActivité(s) exercée(s)                     Etude  réalisation  réglage  essais  mise  au  point  conseil  et  maintenance  des\n                                           installations  de  production  d'énergie  et  de  distribution  de  tous  fluides\n                                           formation afférentes aux concepts ci-dessus\nNomenclature d'activités française (code NAF) 7112B\nDate de commencement d'activité            01/12/2009\n\nOrigine du fonds ou de l'activité          Création\n\nMode d'exploitation                        Exploitation directe\n\n                                                                                                 Le Greffier\n\n\n                                                                                            FIN DE L'EXTRAIT\n\n\nR.C.S.Nantes - 07/11/2024 - 14:44:07                                                                 page 1/1\"\"\"",
            "CreatedDate": "2025-02-03T11:04:41.4614784+00:00",
            "IsHidden": false,
            "IsSummarized": false,
            "Error": null,
            "Metadata": {
                "Name": "Extrait KBIS - ISATEC.pdf",
                "Size": 734484,
                "NumberOfCharacters": 2755,
                "NumberOfPages": 1
            }
        },
        
            """
user_message = {"role": "user", "content": user_input}
messages = [system_message, user_message]

data = {
    "model": "gpt-4o",
    "messages": messages,
    "temperature": 0
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