# 🛠️ ZwickRoell Data Intelligence Orchestrator
**Projet START Hack 2026** | Team **Inglorious BaSTART**

> Une plateforme d'analyse industrielle permettant d'interroger, comparer et monitorer 31 000+ rapports d'essais de matériaux via une interface naturelle, déterministe et transparente.

---

## 🏗️ Architecture Technique : "Deterministic MCP Orchestrator"

Contrairement aux approches "Agentiques" classiques (souvent lentes, coûteuses et imprévisibles), nous avons implémenté une **Architecture d'Orchestration Déterministe** basée sur les standards du **Model Context Protocol (MCP)** :

1. **Intent Routing & Local Fallback** : Classification haute performance des requêtes (JSON Mode) doublée d'une logique heuristique locale. Si le LLM échoue, le système reste fonctionnel.
2. **MCP-Powered Tooling & Semantic Mapper (The Glue)** : En exploitant le **Model Context Protocol (MCP)**, nous avons standardisé l'interface entre le LLM et nos sources de données. Avant d'interroger MongoDB, un pré-processeur normalise les entités (Machines, Matériaux) et gère la **Normalisation automatique des unités** (ex: kN ↔ N) pour garantir la pertinence des comparaisons.
3. **Explainable AI (XAI)** : Chaque réponse est accompagnée d'un `Tool Trace` (Chain of Thought visible) montrant précisément quelles données ont été extraites via le protocole MCP et quel outil a été exécuté.

---

## 📂 Arborescence du Projet

```text
.
├── backend/
│   ├── api/                # Points d'entrée FastAPI (Chat, Data)
│   ├── models/             # Schémas Pydantic (Validation stricte)
│   ├── services/           
│   │   ├── llm_orchestrator.py # Cerveau (Routing & Fallback)
│   │   ├── semantic_mapper.py  # Normalisation sémantique & unités
│   │   └── data_access_layer.py # Interface MongoDB
│   └── tools/              # Logique métier (Trend, Compare, Inspect, Find)
├── frontend/
│   ├── app/                # Next.js 15 App Router
│   ├── components/         # UI Components (Charts, Stats Cards)
│   │   └── response/       # Rendu riche (Markdown GFM, ChartRenderer)
│   ├── globals.css         # Tailwind v4 Config (@plugin typography)
│   └── lib/                # API Client & Types
└── README.md
```

## 🚀 Le "Golden Path" (Scénario de Démo)

La démo a été conçue pour montrer la robustesse du système face à des données industrielles réelles :

* **Search** : *"Show me 3 tests for steel"*
    * **Feature** : Extraction de limite numérique et rendu en tableau Markdown dynamique.
* **Inspect** : *"Inspect data structure for BAR 52"*
    * **Feature** : Découverte dynamique de schéma (Zero-shot schema detection).
* **Compare** : *"Compare Standard force between BAR 52 and metal plate"*
    * **Feature** : **Moment "Wow"** - Détection de disparité d'unités (kN vs N) et recalcul automatique pour une comparaison physique juste.
* **Trend** : *"Show me the trend over time"*
    * **Feature** : Analyse de Volatilité - Calcul de l'écart-type en temps réel. Si un pic (outlier) est détecté, le système alerte sur l'instabilité du process.

---

## 💻 Installation et Lancement

### 1. Backend (FastAPI)
*Nécessite Python 3.10+*

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Créer un fichier .env avec OPENAI_API_KEY et MONGO_URI
uvicorn main:app --reload --port 8000
```

### 2. Frontend (Next.js)
*Nécessite Node.js 18+*

```bash
# Aller dans le dossier web
cd frontend/web

# Installer les dépendances de base
npm install

# Installation des plugins de rendu (Markdown & Typography)
npm install @tailwindcss/typography react-markdown remark-gfm

# Lancer l'application en mode développement
npm run dev
```

L'application est alors accessible sur **[http://localhost:3000](http://localhost:3000)**.

---

## 🛠️ Stack Technologique

* **Frontend** : Next.js 15 (App Router), Tailwind CSS v4, Recharts, React-Markdown.
* **Backend** : FastAPI, Pydantic v2, OpenAI GPT-4o-mini (Structured Outputs).
* **Data** : MongoDB (31k records).
* **Logic** : Orchestration déterministe stateless (Latence < 1.5s).

---

*Développé par la Team **Inglorious BaSTART** pour le START Hack 2026.*

