# Campus Copilot - Agent TUM Library (Auto-Booking)

Ce projet permet à un agent IA autonome de réserver des places d'étude à la Technical University of Munich (TUM) via une interface en langage naturel. 

## Structure
- `TUM_Library_Agent.ipynb` : L'interface IA pour discuter avec l'agent.
- `manage-bookings/` : Le moteur léger de réservation/annulation.

## Installation
1. Créez un environnement virtuel et installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Configurez votre fichier `.env` avec vos accès TUM et AWS Bedrock.

## Utilisation
Ouvrez le notebook et demandez simplement : *"Réserve pour demain à 14h"* ou *"Annule ma place de mardi"*.
