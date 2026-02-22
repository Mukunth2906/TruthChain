# TruthChain

# ⛓️ TruthChain
### A Blockchain-Based AI Content Provenance & Accountability System

> A tamper-proof ledger that records the **origin**, **authorship**, and **modification history** of digital content — solving the growing crisis of unverifiable AI-generated media.

---

## 🧠 The Problem

In today's world, AI-generated content (text, images, videos) floods the internet. It's nearly impossible to answer:

- **Who created this content?**
- **Was it AI-generated or human-written?**
- **Has it been tampered with or modified?**
- **Can we trust this news article / research paper / image?**

---

## 💡 Our Solution

TruthChain is a **simple blockchain network** built from scratch that acts as a **tamper-proof ledger** for digital content — recording *who created what, when, and whether it's been modified.*

---

## 👥 Network Participants

| Participant | Role | Responsibility |
|---|---|---|
| **Content Creator** | Block Author | Publishes original content (article, image hash, video) to the chain |
| **AI Model / Tool** | Content Tagger | Flags content as "AI-Generated" with a confidence score |
| **Verifier / Fact Checker** | Node Validator | Validates and approves blocks before they're added |
| **Publisher / Platform** | Chain Node | Hosts a copy of the chain (e.g. a news site, social platform) |
| **End User / Reader** | Chain Reader | Queries the chain to verify content authenticity |

---

## 🔗 Block Structure

Each block on the TruthChain records the following:

```
Block {
  index          → Block number
  timestamp      → When it was recorded
  content_hash   → SHA-256 hash of the content (unique fingerprint)
  author         → Who created it (Creator name/ID)
  content_type   → "human-written" / "AI-generated" / "modified"
  ai_score       → AI detection confidence (0.0 - 1.0)
  previous_hash  → Links to previous block (tamper-proof chain)
  hash           → This block's own hash
}
```

---

## 🏗️ Build Phases

### Phase 1 — Core Blockchain (Python)
Build the blockchain engine with SHA-256 hashing, block creation, and chain validation logic from scratch — no external blockchain libraries.

### Phase 2 — Participants & Actions
Simulate all 5 participants performing real actions on the chain — creating content, tagging AI origin, and verifying blocks.

### Phase 3 — Tamper Detection Demo
Demonstrate what happens when someone tries to **modify** a block — the chain immediately detects the integrity breach and flags it.

### Phase 4 — CLI Dashboard
A terminal-based interface with colored output that displays the full chain, participant activity, block details, and verification status in real time.

### Phase 5 — Demo Recording
Run a full end-to-end simulation showing the complete lifecycle of content on TruthChain.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| Hashing | SHA-256 via built-in `hashlib` |
| Data Format | JSON blocks |
| Interface | Terminal / CLI with ANSI colored output |
| Dependencies | None — built entirely from scratch |

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/your-username/truthchain.git
cd truthchain

# Run the simulation
python truthchain.py
```

No external packages required. Just Python 3.

---

## 📁 Project Structure

```
truthchain/
│
├── truthchain.py        # Main blockchain engine & simulation
├── participants.py      # Participant roles and actions
├── tamper_demo.py       # Tamper detection demonstration
├── cli_dashboard.py     # Terminal dashboard with colored output
└── README.md            # You are here
```

---

## 🎓 Academic Context

This project was developed as part of a blockchain fundamentals assignment, simulating a real-world use case of distributed ledger technology applied to the problem of **AI content provenance and digital media accountability**.

---

## 📄 License

MIT License — free to use, modify, and distribute.