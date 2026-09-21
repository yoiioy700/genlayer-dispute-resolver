# AI Arbitrator Escrow - GenLayer Intelligent Contract

A decentralized, autonomous escrow and dispute adjudication Intelligent Contract built on **GenLayer**.

When clients and freelancers face milestone disagreements, GenLayer AI validators independently evaluate the agreed job requirements against the submitted deliverables to reach consensus on payout distribution via the **Equivalence Principle**.

---

## 🌟 Architecture & Key Invariants

1. **Deterministic State Partition:**
   Contract state (`TreeMap[str, DisputeCase]`) stores verified case metadata, agreed requirement briefs, deliverable hashes/links, and final adjudication outcomes.
2. **Equivalence Principle Consensus (`gl.eq_principle.strict_eq`):**
   Non-deterministic natural-language reasoning is isolated in `gl.nondet.exec_prompt`. Validator committees evaluate the deliverable against the requirement contract and reach semantic consensus on whether to award funds to the freelancer, refund the client, or execute a partial split.
3. **Ghost Contract Compatibility:**
   Fully compatible with GenLayer L2 (Chain ID 4221) and Ghost contract execution standards.

---

## 📜 Deployed Contracts

| Network | Chain ID | Contract Address | Status | Explorer |
| :--- | :--- | :--- | :--- | :--- |
| **GenLayer Asimov Testnet** | 4221 | `0xFD2C068A93A38Ba95d1ff7EB78b647f80d7A93c2` | Finalized (`FINISHED_WITH_RETURN`) | [View on Asimov Explorer](https://explorer-asimov.genlayer.com/address/0xFD2C068A93A38Ba95d1ff7EB78b647f80d7A93c2) |
| **GenLayer Bradbury Testnet** | 4221 | `0x9263BC62311614fdcdA0030d2e493B210f133ffc` | Finalized (`FINISHED_WITH_RETURN`) | [View on Bradbury Explorer](https://explorer-bradbury.genlayer.com/address/0x9263BC62311614fdcdA0030d2e493B210f133ffc) |

---

## ⚙️ Contract Interface

### State Structure: `DisputeCase`
```python
@allow_storage
@dataclass
class DisputeCase:
    case_id: str
    client: Address
    freelancer: Address
    amount: u256
    requirements: str
    deliverable: str
    status: str  # "CREATED", "SUBMITTED", "RESOLVED"
    verdict: str  # "CLIENT", "FREELANCER", "SPLIT"
    client_share_pct: u256
    reason: str
```

### Write Methods
* `create_case(case_id: str, freelancer_addr: str, amount_wei: u256, requirements: str) -> str`:
  Initializes an escrow case funded by the client (`gl.message.sender_address`).
* `submit_deliverable(case_id: str, deliverable: str) -> None`:
  Freelancer submits the proof of work (deliverable URL or technical summary).
* `adjudicate_dispute(case_id: str) -> dict`:
  Triggers non-deterministic prompt evaluation via GenVM LLM modules. The leader proposes an allocation, and validators reach consensus using `strict_eq`.

### View Methods
* `get_case(case_id: str) -> dict`: Returns the full case record, payout verdict, and reasoning.
* `get_total_cases() -> int`: Returns total count of registered cases.

---

## 🧪 Testing & Deployment

Deployable via `genlayer-js` or GenLayer CLI:
```bash
# Using GenLayer CLI
genlayer deploy --contract contracts/AIArbitratorEscrow.py
```

Built with GenLayer standard library and CPython 3.13 WebAssembly sandbox (`py-genlayer`).
