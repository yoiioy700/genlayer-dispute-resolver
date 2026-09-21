# AI Arbitrator Escrow - GenLayer Intelligent Contract & dApp

A decentralized, autonomous freelance escrow and dispute adjudication platform built on **GenLayer**.

When clients and freelancers face milestone disagreements, GenLayer AI validators independently evaluate the agreed job requirements against submitted deliverables to reach consensus on payout distribution via the **Equivalence Principle** (`gl.eq_principle.strict_eq`).

---

## 🌟 Architecture & Key Invariants

1. **Deterministic State Partition:**
   Contract state (`TreeMap[str, DisputeCase]`) stores verified case metadata, agreed requirement briefs, deliverable proof, and final adjudication outcomes with native `u256` integer typing.
2. **Equivalence Principle Consensus (`strict_eq`):**
   Non-deterministic natural-language reasoning is isolated in `gl.nondet.exec_prompt`. Validator committees evaluate deliverable fulfillment against the requirement brief and reach semantic consensus on fund allocation (`FREELANCER`, `CLIENT`, or `SPLIT`).
3. **Storage Boundary Enforcement:**
   Storage data is strictly copied into local string primitives before entering non-deterministic closures, preventing GenVM sub-VM pickling warnings and memory sandbox violations.

---

## 🛡️ Security Invariants & Access Control

* **Invariant 1 (Collision Resistance):** `create_case` verifies `case_id not in self.cases` to prevent malicious overwrites of active or settled escrow deposits.
* **Invariant 2 (Deliverable Authorization):** `submit_deliverable` enforces caller verification (`sender == case.freelancer or sender == case.client`), preventing third-party deliverable tampering.
* **Invariant 3 (Adjudication Gating):** `adjudicate_dispute` restricts callers to registered contract parties (`sender == case.client or sender == case.freelancer`) and requires `status == "SUBMITTED"` to prevent premature adjudication on empty proofs.
* **Invariant 4 (Finite State Machine):** Cases transition strictly `CREATED -> SUBMITTED -> RESOLVED`. No retroactive mutations or double-adjudications are permitted once settled.

---

## 📜 Verified Deployments

| Network | Chain ID | Contract Address | Status | Explorer |
| :--- | :--- | :--- | :--- | :--- |
| **GenLayer Asimov Testnet** | 4221 | `0x97fA8a8C34994477C17cc44933bA0B2203372760` | Finalized (`FINISHED_WITH_RETURN`) | [View on Asimov Explorer](https://explorer-asimov.genlayer.com/address/0x97fA8a8C34994477C17cc44933bA0B2203372760) |

### On-Chain Transaction Proofs:
* **Contract Deploy:** [`0xffde5b3c978b51f07421bac353258e884c2ca92d23be26c48466737240560000`](https://explorer-asimov.genlayer.com/tx/0xffde5b3c978b51f07421bac353258e884c2ca92d23be26c48466737240560000)
* **Create Case Tx:** [`0x649a9120c19ac4fcfa68523e2e3f737e6e50f3ef4c275039e80288f2bfa61553`](https://explorer-asimov.genlayer.com/tx/0x649a9120c19ac4fcfa68523e2e3f737e6e50f3ef4c275039e80288f2bfa61553)
* **Submit Deliverable Tx:** [`0x4a1631de91d4c1b3089c60c6ed29d85f060870b57779c11b6bd40735d71094b8`](https://explorer-asimov.genlayer.com/tx/0x4a1631de91d4c1b3089c60c6ed29d85f060870b57779c11b6bd40735d71094b8)
* **AI Consensus Adjudication Tx:** [`0x7a17f44ef44fccdb2b852a11b5382440e63fe87ba292df150cf9a0c5cbbe30e5`](https://explorer-asimov.genlayer.com/tx/0x7a17f44ef44fccdb2b852a11b5382440e63fe87ba292df150cf9a0c5cbbe30e5)

---

## 💻 Running the Frontend

The dApp frontend is built with **Next.js 16 (Turbopack)** and directly uses `genlayer-js` to connect to GenLayer Asimov:

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to create escrow cases, submit deliverables, and trigger AI arbitrator adjudication.

---

## 🧪 Unit Tests

Run direct-mode test suites:
```bash
pytest tests/
```
