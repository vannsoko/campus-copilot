# Agent IA TUM Library (Auto-Booking)

Ce projet permet à un agent IA autonome de réserver des places d'étude à la Technical University of Munich (TUM) via une interface en langage naturel. 

Il repose sur l'association de :
1. **Amazon Bedrock (Claude 3.5/4.5)** : L'IA qui comprend votre demande ("Réserve pour demain à 14h").
2. **anny-booking-automation** : Un script open-source extrêmement fiable en arrière-plan qui réalise la réservation silencieusement via Playwright.

## Installation

1. Assurez-vous d'avoir Python installé et de créer un environnement virtuel :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Le dépôt va automatiquement télécharger le dossier `anny-booking-automation` ou vous pouvez l'avoir dans le répertoire courant via l'agent.

## Configuration

Configurez vos accès dans le fichier `.env` :

```env
# Identifiants TUM (Shibboleth SSO)
TUM_USERNAME=go59jun
TUM_PASSWORD=VotreMotDePasse

# AWS Credentials (pour Amazon Bedrock)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=eu-central-1 

# Modèle recommandé
BEDROCK_MODEL_ID=eu.anthropic.claude-sonnet-4-5-20250929-v1:0
```

## Utilisation

Ouvrez le notebook Jupyter `TUM_Library_Agent.ipynb`.
Modifiez simplement la requête en langage naturel dans la dernière cellule :
```python
user_request = "Salut ! Est-ce que tu peux me réserver une place demain de 10h à 15h ?"
```
Exécutez les cellules. L'agent comprendra vos horaires, configurera l'outil de réservation et lancera l'automatisation de manière invisible !
