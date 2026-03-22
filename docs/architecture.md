## 📁 Structure du projet

```text
zr-chat-test-data/
├── apps/
│   ├── api/        # backend Python
│   │   ├── pyproject.toml
│   │   └── src/
│   │       ├── main.py
│   │       ├── config/      # settings, env
│   │       ├── db/          # connexion Mongo
│   │       ├── models/      # schémas Pydantic
│   │       ├── services/    # logique métier data
│   │       ├── analytics/   # stats, tendances, comparaisons
│   │       ├── tools/       # fonctions appelées par le LLM
│   │       ├── agents/      # orchestration agentique
│   │       ├── routers/     # endpoints API
│   │       └── utils/       # helpers
│   └── web/        # frontend Next.js
│       ├── app/
│       ├── components/
│       └── lib/
├── packages/
│   └── shared/     # contrats partagés, payloads, prompts
├── docs/           # architecture, décisions, flow
├── infra/          # docker-compose, scripts infra
└── scripts/        # scripts utilitaires
```

## Convention de langage par couche

```text
Frontend: TypeScript
Backend/API: Python
Analytics: Python
Mongo queries: Python
LLM orchestration: Python
Shared schemas: JSON / TS types simples
```

## Architecture

```text
[Frontend Next.js]
    |
    v
[Backend FastAPI]
    |
    +--> [Agent / Orchestrator LLM]
    |         |
    |         +--> tools de recherche
    |         +--> tools d'analyse
    |         +--> tools de visualisation
    |
    +--> [Service data]
    |         |
    |         +--> MongoDB Tests
    |         +--> MongoDB Values
    |         +--> mappings UUID
    |
    +--> [Analytics engine]
              |
              +--> comparaison
              +--> tendance
              +--> stats
              +--> résumés
```