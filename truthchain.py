"""
================================================
  TruthChain - Blockchain-Based AI Content
      Provenance & Accountability System
================================================
  Menu-Driven | HuggingFace AI Detection
  Participants:
    1. Content Creator  - Publishes content
    2. AI Tagger        - Detects AI vs Human
    3. Fact Checker     - Verifies blocks
    4. Publisher        - Validates chain
    5. End User         - Queries provenance
================================================
"""

import hashlib
import json
import time
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# ── Load API Key from .env ─────────────────────
load_dotenv()
HF_API_KEY   = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/openai-community/roberta-base-openai-detector"
# ── Colors ─────────────────────────────────────
R  = "\033[91m"   # Red
G  = "\033[92m"   # Green
Y  = "\033[93m"   # Yellow
B  = "\033[94m"   # Blue
M  = "\033[95m"   # Magenta
C  = "\033[96m"   # Cyan
W  = "\033[97m"   # White
BO = "\033[1m"    # Bold
X  = "\033[0m"    # Reset


# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════
def banner():
    print(f"{C}{BO}")
    print("=" * 52)
    print("  ⛓️  TruthChain - AI Content Provenance System")
    print("=" * 52)
    print(X)

def sec(title):
    print(f"\n{Y}{BO}{'─'*52}\n  {title}\n{'─'*52}{X}")

def log(who, msg, color=W):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{ts}] [{who}] {msg}{X}")

def pause():
    input(f"\n{C}  ↵ Press Enter to continue...{X}")

def bar(score, total=10):
    filled = int(score * total)
    return "█" * filled + "░" * (total - filled)


# ══════════════════════════════════════════════
#  HUGGING FACE AI DETECTOR
# ══════════════════════════════════════════════
def detect_ai(text):
    """
    Calls HuggingFace roberta-base-openai-detector.
    Returns: ai%, human%, confidence, verdict, explanation
    """
    if len(text.split()) < 20:
        print(f"{Y}  ⚠️  Text too short for accurate detection (need 20+ words).{X}")

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}

    log("AI Tagger", "Calling HuggingFace API...", M)

    try:
        resp = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=30)

        # Model cold-start — wait and retry
        if resp.status_code == 503:
            log("AI Tagger", "Model loading, retrying in 20s...", Y)
            time.sleep(20)
            resp = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=30)

        if resp.status_code == 401:
            log("AI Tagger", "❌ Invalid API Key! Check your .env file.", R)
            return None

        if resp.status_code != 200:
            log("AI Tagger", f"❌ API Error {resp.status_code}: {resp.text}", R)
            return None

        data   = resp.json()
        scores = {item["label"]: item["score"] for item in data[0]}

        # roberta model: "Fake" = AI-generated, "Real" = Human-written
        ai_score    = scores.get("Fake", scores.get("LABEL_1", 0.0))
        human_score = scores.get("Real", scores.get("LABEL_0", 0.0))

        # Confidence + verdict based on AI score
        if ai_score >= 0.85:
            confidence  = f"{R}VERY HIGH{X}"
            verdict     = f"{R}Almost Certainly AI-Generated{X}"
            explanation = "Highly structured, formal patterns strongly indicate AI authorship."
        elif ai_score >= 0.60:
            confidence  = f"{Y}HIGH{X}"
            verdict     = f"{Y}Likely AI-Generated{X}"
            explanation = "Writing style and structure suggest AI generation."
        elif ai_score >= 0.40:
            confidence  = f"{C}MEDIUM{X}"
            verdict     = f"{C}Uncertain — Could Be Either{X}"
            explanation = "Mixed signals. Possibly AI-assisted or paraphrased."
        elif ai_score >= 0.20:
            confidence  = f"{G}LOW{X}"
            verdict     = f"{G}Likely Human-Written{X}"
            explanation = "Natural phrasing and variation suggest human authorship."
        else:
            confidence  = f"{G}VERY LOW{X}"
            verdict     = f"{G}Almost Certainly Human-Written{X}"
            explanation = "Strong human writing signals. Very unlikely AI-generated."

        return {
            "ai_pct"     : round(ai_score * 100, 2),
            "human_pct"  : round(human_score * 100, 2),
            "confidence" : confidence,
            "verdict"    : verdict,
            "explanation": explanation,
            "raw"        : ai_score
        }

    except requests.exceptions.Timeout:
        log("AI Tagger", "❌ Request timed out. Check internet.", R)
        return None
    except Exception as e:
        log("AI Tagger", f"❌ Error: {e}", R)
        return None


def show_ai_result(r):
    if not r:
        print(f"{R}  ❌ AI Detection failed.{X}")
        return
    print(f"""
  {BO}🤖 AI Detection Report{X}
  ┌────────────────────────────────────────────────┐
  │  AI Probability    :  {R}{r['ai_pct']}%{X}
  │  AI Score          :  {R}[{bar(r['raw'])}]{X}
  │  Human Probability :  {G}{r['human_pct']}%{X}
  │  Human Score       :  {G}[{bar(1 - r['raw'])}]{X}
  │  Confidence Level  :  {r['confidence']}
  │  Verdict           :  {r['verdict']}
  │  Explanation       :  {r['explanation']}
  └────────────────────────────────────────────────┘""")


# ══════════════════════════════════════════════
#  BLOCK
# ══════════════════════════════════════════════
class Block:
    def __init__(self, index, author, content, content_type, ai_result, previous_hash):
        self.index         = index
        self.timestamp     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.author        = author
        self.content       = content
        self.content_hash  = hashlib.sha256(content.encode()).hexdigest()
        self.content_type  = content_type
        self.ai_result     = ai_result
        self.verified_by   = None
        self.previous_hash = previous_hash
        self.hash          = self.calc_hash()

    def calc_hash(self):
        data = json.dumps({
            "index"        : self.index,
            "timestamp"    : self.timestamp,
            "author"       : self.author,
            "content_hash" : self.content_hash,
            "content_type" : self.content_type,
            "ai_score"     : self.ai_result.get("raw", 0.0) if self.ai_result else 0.0,
            "verified_by"  : self.verified_by,
            "previous_hash": self.previous_hash,
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def show(self):
        r        = self.ai_result or {}
        ai_pct   = r.get("ai_pct", 0.0)
        hum_pct  = r.get("human_pct", 0.0)
        conf     = r.get("confidence", "N/A")
        verdict  = r.get("verdict", "N/A")
        raw      = r.get("raw", 0.0)
        verified = f"{G}✔ {self.verified_by}{X}" if self.verified_by else f"{Y}⏳ Pending{X}"
        tamper   = f"{G}Intact ✅{X}" if self.hash == self.calc_hash() else f"{R}Tampered ❌{X}"

        print(f"""
  {BO}Block #{self.index}{X}
  ├─ Timestamp        : {self.timestamp}
  ├─ Author           : {C}{self.author}{X}
  ├─ Content Preview  : "{self.content[:60]}{'...' if len(self.content)>60 else ''}"
  ├─ Content Hash     : {M}{self.content_hash[:36]}...{X}
  ├─ Content Type     : {B}{self.content_type}{X}
  ├─ AI Probability   : {R}{ai_pct}% [{bar(raw)}]{X}
  ├─ Human Probability: {G}{hum_pct}%{X}
  ├─ Confidence       : {conf}
  ├─ Verdict          : {verdict}
  ├─ Verified By      : {verified}
  ├─ Integrity        : {tamper}
  ├─ Prev Hash        : {M}{self.previous_hash[:36]}...{X}
  └─ Block Hash       : {G}{self.hash[:36]}...{X}""")


# ══════════════════════════════════════════════
#  BLOCKCHAIN
# ══════════════════════════════════════════════
class Blockchain:
    def __init__(self):
        self.chain = []
        self._genesis()

    def _genesis(self):
        g = Block(
            index         = 0,
            author        = "TruthChain System",
            content       = "Genesis Block — TruthChain Initialized",
            content_type  = "system",
            ai_result     = {"ai_pct":0,"human_pct":100,"confidence":"N/A",
                             "verdict":"System Block","explanation":"Genesis.","raw":0.0},
            previous_hash = "0" * 64
        )
        g.verified_by = "System"
        g.hash = g.calc_hash()
        self.chain.append(g)
        log("SYSTEM", "✅ Genesis Block created — TruthChain is live!", G)

    def latest(self):
        return self.chain[-1]

    def add(self, block):
        block.previous_hash = self.latest().hash
        block.hash = block.calc_hash()
        self.chain.append(block)

    def validate(self):
        for i in range(1, len(self.chain)):
            cur  = self.chain[i]
            prev = self.chain[i - 1]
            if cur.hash != cur.calc_hash():
                print(f"{R}  ❌ Block #{i}: Hash invalid — data was tampered!{X}")
                return False
            if cur.previous_hash != prev.hash:
                print(f"{R}  ❌ Block #{i}: Previous hash mismatch — chain broken!{X}")
                return False
        return True

    def get(self, idx):
        return self.chain[idx] if 0 <= idx < len(self.chain) else None

    def show_all(self):
        sec("📦 FULL BLOCKCHAIN")
        for b in self.chain:
            b.show()
            if b.index < len(self.chain) - 1:
                print(f"  {M}        ↓  linked via hash{X}")


# ══════════════════════════════════════════════
#  ACTION 1 — PUBLISH CONTENT (Creator)
# ══════════════════════════════════════════════
def publish(bc):
    sec("✍️  PARTICIPANT 1 — CONTENT CREATOR")
    author = input(f"{C}  Your name (Creator): {X}").strip()

    print(f"{C}  Paste your content below.")
    print(f"  Press Enter on an empty line when done:{X}")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    content = " ".join(lines).strip()

    if not author or not content:
        print(f"{R}  ❌ Name and content cannot be empty!{X}")
        pause(); return

    log(author, f'Content received: "{content[:70]}..."', C)

    # Auto-run AI detection
    sec("🤖 PARTICIPANT 2 — AI TAGGER (Auto-Scanning via HuggingFace)")
    ai = detect_ai(content)
    show_ai_result(ai)

    if ai:
        ctype = "AI-generated" if ai["raw"] >= 0.5 else "human-written"
    else:
        ctype = "unknown"
        ai = {"ai_pct":0,"human_pct":0,"confidence":"N/A",
              "verdict":"Detection Failed","explanation":"API failed.","raw":0.0}

    b = Block(len(bc.chain), author, content, ctype, ai, bc.latest().hash)
    bc.add(b)
    log(author, f"✅ Block #{b.index} added to TruthChain!", G)
    pause()


# ══════════════════════════════════════════════
#  ACTION 2 — VERIFY BLOCK (Fact Checker)
# ══════════════════════════════════════════════
def verify(bc):
    sec("🔍 PARTICIPANT 3 — FACT CHECKER / VERIFIER")

    if len(bc.chain) <= 1:
        print(f"{R}  ❌ No content blocks yet. Publish content first.{X}")
        pause(); return

    checker = input(f"{C}  Your name (Fact Checker): {X}").strip()

    print(f"\n{W}  Blocks available to verify:{X}")
    for b in bc.chain[1:]:
        status = f"{G}✔ {b.verified_by}{X}" if b.verified_by else f"{Y}⏳ Pending{X}"
        print(f"  [{b.index}] by {b.author} — {status}")

    try:
        idx = int(input(f"\n{C}  Enter block number to verify: {X}"))
        b   = bc.get(idx)

        if not b or idx == 0:
            print(f"{R}  ❌ Invalid block number!{X}"); pause(); return

        if b.verified_by:
            print(f"{Y}  ⚠️  Already verified by {b.verified_by}{X}"); pause(); return

        log(checker, f"Reviewing Block #{idx}...", B)
        time.sleep(0.5)

        if b.hash == b.calc_hash():
            b.verified_by = checker
            b.hash = b.calc_hash()
            log(checker, f"✅ Block #{idx} VERIFIED and APPROVED!", G)
        else:
            log(checker, f"❌ Block #{idx} hash mismatch — REJECTED!", R)

    except ValueError:
        print(f"{R}  ❌ Enter a valid number!{X}")
    pause()


# ══════════════════════════════════════════════
#  ACTION 3 — CHECK CHAIN INTEGRITY (Publisher)
# ══════════════════════════════════════════════
def integrity(bc):
    sec("🏢 PARTICIPANT 4 — PUBLISHER / CHAIN INTEGRITY")
    publisher = input(f"{C}  Platform name: {X}").strip()

    log(publisher, "Running full chain validation...", Y)
    time.sleep(0.8)

    if bc.validate():
        log(publisher, f"✅ CHAIN VALID — All {len(bc.chain)} blocks intact!", G)
    else:
        log(publisher, "❌ CHAIN COMPROMISED — Tampered block detected! Alert raised!", R)
    pause()


# ══════════════════════════════════════════════
#  ACTION 4 — QUERY PROVENANCE (End User)
# ══════════════════════════════════════════════
def query(bc):
    sec("👤 PARTICIPANT 5 — END USER / READER")

    if len(bc.chain) <= 1:
        print(f"{R}  ❌ No content blocks yet!{X}"); pause(); return

    user = input(f"{C}  Your name (Reader): {X}").strip()

    print(f"\n{W}  Available blocks:{X}")
    for b in bc.chain[1:]:
        print(f"  [{b.index}] by {b.author} — {b.timestamp}")

    try:
        idx = int(input(f"\n{C}  Enter block number to query: {X}"))
        b   = bc.get(idx)

        if not b or idx == 0:
            print(f"{R}  ❌ Invalid block!{X}"); pause(); return

        log(user, f"Fetching provenance for Block #{idx}...", C)
        time.sleep(0.4)

        r       = b.ai_result or {}
        tamper  = f"{G}YES ✅{X}" if b.hash == b.calc_hash() else f"{R}NO ❌  TAMPERED!{X}"
        verified= b.verified_by or "Not Verified Yet"

        print(f"""
  {BO}📋 PROVENANCE REPORT — Block #{idx}{X}
  ┌────────────────────────────────────────────────┐
  │  Author            :  {b.author}
  │  Published         :  {b.timestamp}
  │  Content Type      :  {b.content_type}
  │  AI Probability    :  {R}{r.get('ai_pct', 'N/A')}%{X}
  │  Human Probability :  {G}{r.get('human_pct', 'N/A')}%{X}
  │  Confidence Level  :  {r.get('confidence', 'N/A')}
  │  Verdict           :  {r.get('verdict', 'N/A')}
  │  Explanation       :  {r.get('explanation', 'N/A')}
  │  Verified By       :  {verified}
  │  Tamper-Proof      :  {tamper}
  └────────────────────────────────────────────────┘""")

    except ValueError:
        print(f"{R}  ❌ Enter a valid number!{X}")
    pause()


# ══════════════════════════════════════════════
#  ACTION 5 — TAMPER ATTACK SIMULATION
# ══════════════════════════════════════════════
def tamper(bc):
    sec("💀 SIMULATE TAMPER ATTACK")

    if len(bc.chain) <= 1:
        print(f"{R}  ❌ No blocks to tamper!{X}"); pause(); return

    print(f"\n{W}  Available blocks:{X}")
    for b in bc.chain[1:]:
        print(f"  [{b.index}] by {b.author}")

    try:
        idx  = int(input(f"\n{C}  Block number to tamper: {X}"))
        b    = bc.get(idx)

        if not b or idx == 0:
            print(f"{R}  ❌ Invalid block!{X}"); pause(); return

        fake = input(f"{R}  Enter fake/modified content to inject: {X}").strip()

        log("ATTACKER", f"Targeting Block #{idx}...", R)
        time.sleep(0.4)
        log("ATTACKER", f'Injecting: "{fake[:60]}"', R)

        # Modify data but do NOT update hash — this is what gets caught
        b.content      = fake
        b.content_hash = hashlib.sha256(fake.encode()).hexdigest()
        b.content_type = "human-written"
        b.ai_result    = {"ai_pct":0,"human_pct":100,"confidence":"VERY LOW",
                          "verdict":"Likely Human-Written","explanation":"Tampered.","raw":0.0}

        log("ATTACKER", "⚠️  Data injected! Run option 3 to see if chain catches it...", Y)

    except ValueError:
        print(f"{R}  ❌ Enter a valid number!{X}")
    pause()


# ══════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════
def menu(bc):
    while True:
        print(f"""
{C}{BO}
  ╔══════════════════════════════════════════════╗
  ║           ⛓️  TRUTHCHAIN MENU               ║
  ╠══════════════════════════════════════════════╣
  ║  1.  ✍️   Publish Content   (Creator)        ║
  ║  2.  🔍  Verify Block       (Fact Checker)   ║
  ║  3.  🏢  Check Integrity    (Publisher)      ║
  ║  4.  👤  Query Provenance   (End User)       ║
  ║  5.  💀  Simulate Tamper Attack              ║
  ║  6.  📦  View Full Blockchain                ║
  ║  0.  🚪  Exit                                ║
  ╚══════════════════════════════════════════════╝
{X}  {W}Chain length: {len(bc.chain)} block(s){X}""")

        choice = input(f"{C}  Choose (0-6): {X}").strip()

        if   choice == "1": publish(bc)
        elif choice == "2": verify(bc)
        elif choice == "3": integrity(bc)
        elif choice == "4": query(bc)
        elif choice == "5": tamper(bc)
        elif choice == "6": bc.show_all(); pause()
        elif choice == "0":
            print(f"\n{G}{BO}  👋 Goodbye! TruthChain signing off. ⛓️{X}\n")
            break
        else:
            print(f"{R}  ❌ Invalid choice. Pick 0–6.{X}")


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════
if __name__ == "__main__":
    banner()

    if not HF_API_KEY:
        print(f"{R}  ❌ HUGGINGFACE_API_KEY missing from .env file!")
        print(f"  Add this to your .env:{X}")
        print(f"  HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxx\n")
        exit(1)

    print(f"{G}  ✅ API Key loaded from .env{X}")
    print(f"{W}  Model : roberta-base-openai-detector (HuggingFace){X}\n")

    bc = Blockchain()
    menu(bc)