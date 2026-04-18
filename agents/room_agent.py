import os
import sys
import subprocess
import datetime
from dotenv import load_dotenv, set_key

# LangChain et Bedrock
import json
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Chargement de l'environnement depuis le dossier agent-booking
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_BOOKING_DIR = os.path.join(BASE_DIR, "agent-booking")
load_dotenv(os.path.join(AGENT_BOOKING_DIR, ".env"))

HISTORY_FILE = os.path.join(AGENT_BOOKING_DIR, "reservation_history.json")

def log_reservation(date, time):
    """Enregistre une réservation dans le fichier d'historique."""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except:
                pass
    history.append({"date": date, "time": time, "timestamp": datetime.datetime.now().isoformat()})
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

CHAT_HISTORY_FILE = os.path.join(AGENT_BOOKING_DIR, "chat_history.json")

def load_chat_history(limit=10):
    """Charge l'historique de la conversation."""
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
                return history[-limit:]
            except:
                pass
    return []

def save_chat_message(role, content):
    """Sauvegarde un message dans l'historique."""
    history = []
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except:
                pass
    history.append({"role": role, "content": content})
    with open(CHAT_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def get_recent_reservations(limit=5):
    """Récupère les dernières réservations effectuées."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
                return history[-limit:]
            except:
                pass
    return []

TUM_USERNAME = os.getenv("TUM_USERNAME")
TUM_PASSWORD = os.getenv("TUM_PASSWORD")

@tool
def book_study_room(booking_time: str, target_days_ahead: int) -> str:
    """
    Outil pour réserver une salle d'étude individuelle (Study Desk) à la bibliothèque de la TUM (Main Campus).
    Args:
        booking_time: Les horaires souhaités au format 'HH:MM:SS-HH:MM:SS' (ex: '09:00:00-13:00:00')
        target_days_ahead: Le nombre de jours dans le futur pour la réservation (ex: 1 pour demain, 2 pour après-demain)
    """

    if target_days_ahead>4: 
        print("Impossible de réserver plus de 4 jours en avance")
        return
    print(f"🔧 Configuration de la réservation : {booking_time} (dans {target_days_ahead} jours)")
    
    engine_dir = os.path.join(AGENT_BOOKING_DIR, "manage-bookings")
    env_path = os.path.join(engine_dir, ".env")
    
    set_key(env_path, "USERNAME", TUM_USERNAME)
    set_key(env_path, "PASSWORD", TUM_PASSWORD)
    set_key(env_path, "SSO_PROVIDER", "tum")
    set_key(env_path, "TIMEZONE", "Europe/Berlin")
    set_key(env_path, "BOOKING_TIMES", booking_time)
    set_key(env_path, "TARGET_DAYS_AHEAD", str(target_days_ahead))
    set_key(env_path, "RESOURCE_URL_PATH", "/resources/study-desks-branch-library-main-campus/children")
    set_key(env_path, "SERVICE_ID", "601")
    
    try:
        # On utilise sys.executable pour être sûr d'utiliser le même venv
        result = subprocess.run([sys.executable, "book.py"], cwd=engine_dir, capture_output=True, text=True)
        # Détection plus souple du succès (insensible à la casse)
        output_combined = (result.stdout + result.stderr).lower()
        if result.returncode == 0 and ("success" in output_combined or "successful" in output_combined):
            # Calculer la date réelle de la réservation
            res_date = (datetime.datetime.now() + datetime.timedelta(days=target_days_ahead)).strftime("%Y-%m-%d")
            log_reservation(res_date, booking_time)
            return f"Succès: Réservation effectuée pour le {res_date} à {booking_time}."
        return f"Erreur: {result.stderr}\n{result.stdout}"
    except Exception as e:
        return f"Erreur système: {str(e)}"

@tool
def cancel_study_room(target_date: str) -> str:
    """
    Outil pour annuler une réservation existante.
    Args:
        target_date: La date de la réservation à annuler au format 'YYYY-MM-DD' (ex: '2026-04-21')
    """
    print(f"🔧 Configuration de l'annulation pour le : {target_date}")
    
    engine_dir = os.path.join(AGENT_BOOKING_DIR, "manage-bookings")
    env_path = os.path.join(engine_dir, ".env")
    
    set_key(env_path, "USERNAME", TUM_USERNAME)
    set_key(env_path, "PASSWORD", TUM_PASSWORD)
    set_key(env_path, "SSO_PROVIDER", "tum")
    set_key(env_path, "CANCEL_DATE", target_date)
    
    try:
        result = subprocess.run([sys.executable, "cancel.py"], cwd=engine_dir, capture_output=True, text=True)
        return f"Succès: {result.stdout}" if result.returncode == 0 else f"Erreur: {result.stderr}\n{result.stdout}"
    except Exception as e:
        return f"Erreur système: {str(e)}"

def run_room_agent(user_message):
    """Lance l'agent avec un message spécifié."""
    model_id = os.getenv("BEDROCK_MODEL_ID", "eu.anthropic.claude-sonnet-4-5-20250929-v1:0")
    llm = ChatBedrockConverse(model=model_id, temperature=0.0)
    tools = [book_study_room, cancel_study_room]
    llm_with_tools = llm.bind_tools(tools)

    today = datetime.datetime.now().strftime("%A %d %B %Y")
    recent_res = get_recent_reservations()
    history_context = ""
    if recent_res:
        history_context = "\n\nVoici l'historique de tes réservations réussies (pour référence) :\n"
        for i, res in enumerate(recent_res):
            history_context += f"- Date: {res['date']}, Heure: {res['time']}\n"
    
    sys_msg = f"Tu es un assistant IA très utile. Aujourd'hui nous sommes le {today}. Traduis les demandes d'horaires et de dates pour utiliser correctement tes outils `book_study_room` ou `cancel_study_room`. Pour annuler, utilise le format 'YYYY-MM-DD'.{history_context}. Si les horaires ne sont pas précisées, prend 2h de reservationVoici les prochains jours : dimanche 19, lundi 20, mardi 21"

    # Chargement de l'historique de conversation
    chat_history = load_chat_history()
    messages = [SystemMessage(content=sys_msg)]
    
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
            
    messages.append(HumanMessage(content=user_message))
    
    print(f"🧠 Agent en cours de réflexion sur : '{user_message}'")
    ai_msg = llm_with_tools.invoke(messages)

    response_content = ai_msg.content

    if ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            if tool_call['name'] == 'book_study_room':
                response_content = book_study_room.invoke(tool_call['args'])
            elif tool_call['name'] == 'cancel_study_room':
                response_content = cancel_study_room.invoke(tool_call['args'])
    
    # Sauvegarde de l'échange
    save_chat_message("user", user_message)
    save_chat_message("assistant", response_content)
    
    return response_content

if __name__ == "__main__":
    # Test rapide si lancé directement
    import sys
    if len(sys.argv) > 1:
        print(run_room_agent(sys.argv[1]))


print(run_room_agent("Annule les deux dernieres reservations effectuees"))