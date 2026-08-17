# ⚖️ GenLayer Freelance Escrow & AI Dispute Resolver

A decentralized escrow and milestone arbitration system built as a **GenLayer Intelligent Contract**. When clients and freelancers disagree on deliverables, decentralized AI validators independently analyze project criteria, deliverable content, and party claims to reach consensus on fund allocation using GenLayer's **Optimistic Democracy** and **Equivalence Principle**.

> **About GenLayer:** GenLayer is the first adjudication layer for the agentic economy — enabling smart contracts to reason, evaluate natural language, and settle subjective disputes trustlessly on-chain without human bottlenecks.

---

## 🎯 Key Features

1. **Milestone Escrow:** Client locks funds on-chain for freelance deliverables with verifiable specifications.
2. **AI Dispute Adjudication:** If work quality or completion is contested, GenLayer AI validators evaluate:
   - Original task specifications
   - Submitted deliverable content
   - Client and Freelancer arguments
3. **Consensus-Backed Fairness:** Multiple validators independently assess the dispute using LLMs via `gl.nondet.exec_prompt()` and agree on the payout ratio (0-100%).
4. **Equivalence Principle:** Results are checked for semantic equivalence (matching decision category and fund allocation within tolerance).
5. **Fullstack Interface:** Modern Next.js application with escrow dashboard, dispute filing, and real-time AI allocation visualizations.

---

## 📁 Repository Structure

```
genlayer-dispute-resolver/
├── contracts/
│   └── dispute_resolver.py       # GenLayer Intelligent Contract (Python)
├── frontend/
│   ├── src/app/
│   │   ├── page.tsx              # Escrow & Adjudication Dashboard
│   │   ├── layout.tsx            # Next.js Root Layout
│   │   └── globals.css           # Modern Dark-Mode UI Styles
│   └── package.json
├── tests/
│   └── test_dispute_resolver.py  # Direct-Mode Unit Tests
└── README.md
```

---

## ⚡ Quick Start

### 1. Requirements
- Node.js 18+ & npm
- Python 3.12+
- Docker (for GenLayer local node / Studio)

### 2. Deploy Contract
Launch GenLayer Studio:
```bash
npx genlayer init
```
Open `http://localhost:8080`, paste `contracts/dispute_resolver.py`, and deploy!

### 3. Run Frontend
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:3000` to interact with the decentralized escrow dashboard.

---

## 🧪 Testing

Run direct-mode in-memory tests:
```bash
pytest tests/test_dispute_resolver.py -v
```

---

## 📜 License
MIT
