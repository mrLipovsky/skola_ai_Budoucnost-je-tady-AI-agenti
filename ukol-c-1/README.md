# Úkol č. 1 – LLM API + Tool Calling

Python skript zavolá LLM API, zpřístupní modelu nástroj `calculate`, vykoná požadovaný výpočet a výsledek pošle zpět LLM. LLM následně vytvoří finální odpověď uživateli.

## Princip

```text
Uživatel → LLM → tool call → Python funkce → tool result → LLM → odpověď
```

## Instalace

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Do `.env` doplň vlastní `OPENAI_API_KEY`. Soubor `.env` je v `.gitignore` a nesmí se commitnout.

## Spuštění

```bash
python main.py
```

Příklad vstupu:

```text
Kolik je 125 krát 37? Použij kalkulačku.
```

Skript:
1. odešle otázku LLM,
2. LLM požádá o zavolání funkce `calculate`,
3. Python funkci vykoná,
4. výsledek odešle zpět LLM,
5. vypíše finální odpověď.

Model lze změnit pomocí proměnné `OPENAI_MODEL` v souboru `.env`.
