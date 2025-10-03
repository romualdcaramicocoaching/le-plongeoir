import os, csv, json, datetime, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
POSTS = SITE / "_posts"
CONTENT = ROOT / "content"

LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "").strip()
LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
POSTS_PER_RUN = int(os.getenv("POSTS_PER_RUN", "1"))

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s-]+", "-", s).strip("-")
    return s[:70]

def call_llm(prompt):
    if not LLM_ENDPOINT or not LLM_API_KEY:
        return f"""# {prompt.split(':',1)[-1].strip()}

**Résumé rapide** : guide pratique généré automatiquement.

## Étapes
1. Échauffement (5-10 min)
2. Corps de séance : 3 blocs progressifs
3. Technique : 3 points clés
4. Erreurs fréquentes et corrections
5. Variante sans équipement

## FAQ
- *Combien de fois/semaine ?* 2-3
- *Combien de temps ?* 30-45 min
- *Quand voir des progrès ?* 4-6 semaines
"""
    import json, urllib.request
    req = urllib.request.Request(
        LLM_ENDPOINT,
        data=json.dumps({"model":"generic","input":prompt,"max_tokens":800}).encode("utf-8"),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {LLM_API_KEY}"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        res = r.read().decode("utf-8")
    try:
        obj = json.loads(res)
        if "text" in obj: return obj["text"]
        if "output" in obj: return obj["output"]
        if "choices" in obj and obj["choices"]:
            c = obj["choices"][0]
            return c.get("text") or c.get("message",{}).get("content","")
    except Exception:
        pass
    return res

def main():
    POSTS.mkdir(parents=True, exist_ok=True)
    processed_path = CONTENT / "processed.json"
    if not processed_path.exists(): processed_path.write_text("[]", encoding="utf-8")
    processed = json.loads(processed_path.read_text(encoding="utf-8"))

    rows = []
    with open(CONTENT / "keywords.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["keyword"] not in processed:
                rows.append(r)

    if not rows:
        print("No keywords left")
        return

    to_make = rows[:POSTS_PER_RUN]
    today = datetime.date.today().strftime("%Y-%m-%d")
    affiliates = json.loads((CONTENT / "affiliates.json").read_text(encoding="utf-8")) if (CONTENT / "affiliates.json").exists() else {}

    def cta(keys):
        if not keys: return ""
        items = []
        for k in [x.strip() for x in keys.split(";") if x.strip()]:
            a = affiliates.get(k)
            if a: items.append(f"- [{a['name']}]({a['url']})")
        if not items: return ""
        return "\n<div class=\"cta-box\">\n<h3>Ressources utiles</h3>\n\n" + "\n".join(items) + "\n\n</div>\n"

    for r in to_make:
        kw = r["keyword"]
        slug = slugify(kw)
        filename = f"{today}-{slug}.md"
        path = POSTS / filename
        prompt = f'''Vous êtes un coach expert. Rédigez un article étape par étape sur: "{kw}".
- Langue: Français, ton direct, concret.
- Inclure: échauffement, points techniques clés, erreurs fréquentes, progressions, variante sans équipement.
- Public: débutant à intermédiaire.
'''
        body = call_llm(prompt)
        front = f"""---
layout: post
title: "{kw}"
date: {today}
categories: [natation, materiel]
---
"""
