# Campus Co-Pilot 🎓🤖

Campus Co-Pilot is an intelligent, agent-based assistant designed specifically for TUM (Technical University of Munich) students. It features a modern macOS-inspired web interface ("Campus OS") and a robust FastAPI backend powered by AWS Bedrock (Claude 3.5 Sonnet) and Cognee.

It allows students to chat via text or real-time voice to manage their university life, combining multiple specialized AI agents.


Check out the demo:
[demo](demo.mp4)


## 🌟 Key Features

- **TUM Copilot (Text Interface)**: A chat interface to interact with the AI assistant.
- **TUM Voice (Karaoke-style Voice Interface)**: A seamless voice-to-voice interaction mode. It uses **Deepgram** for live Speech-to-Text and **ElevenLabs** for real-time Text-to-Speech, featuring a dynamic teleprompter that highlights words as they are spoken.
- **TUM Calendar**: Visualizes your upcoming deadlines, exams, and classes.
- **TUM Courses**: Browse generated summaries for your courses and lectures.

## 🧠 AI Agents

The orchestrator dynamically routes requests to one or more of the following agents:
1. **Moodle Agent (📚)**: Retrieves and summarizes lecture slides and course documents.
2. **Agenda Agent (📅)**: Tracks deadlines, upcoming exams, and schedule events.
3. **Room Agent (🏫)**: Handles the reservation of study rooms on campus.

## 🏗️ Architecture

- **Backend**: Python (FastAPI, WebSockets).
- **AI Core**: AWS Bedrock (Anthropic Claude 3.5 Sonnet) for orchestration.
- **Memory & RAG**: Cognee (SQLite + FastEmbed) for student context and long-term memory.
- **Voice Stack**: Deepgram (Live STT) & ElevenLabs (Streaming TTS).
- **Frontend**: React + TypeScript (Framer Motion for animations).

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js & npm
- AWS Credentials (with Bedrock access)
- Deepgram API Key
- ElevenLabs API Key

### Backend Setup
1. Navigate to the project root directory.
2. Create and activate a Python virtual environment:
   ```bash
   conda create -n hack_env python=3.11
   conda activate hack_env
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your environment variables in a `.env` file:
   ```env
   AWS_DEFAULT_REGION=us-east-1
   BEDROCK_MODEL_ID=eu.anthropic.claude-sonnet-4-5-20250929-v1:0
   DEEPGRAM_API_KEY=your_key
   ELEVENLABS_API_KEY=your_key
   ELEVENLABS_VOICE_ID=your_voice_id
   ```
5. Start the backend server:
   ```bash
   python speech_interface.py
   ```
   *(Note: The server runs on `http://localhost:8000` and serves the API, WebSockets, and static frontend build if available).*

### Frontend Setup
1. Navigate to the `campus-os` directory:
   ```bash
   cd campus-os
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
   The application will be available at `http://localhost:3000`.

## 🤝 Contribution

Contributions are welcome! Please make sure to follow the current architecture and properly handle asynchronous agent calls when modifying `orchestrator.py` or the agent modules.
