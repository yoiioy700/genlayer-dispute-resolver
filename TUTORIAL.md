# Tutorial: Building a P2P Dispute Resolution dApp with AI on GenLayer

**Project Repository:** [https://github.com/yoiioy700/genlayer-dispute-resolver](https://github.com/yoiioy700/genlayer-dispute-resolver)

Traditional blockchains can only execute deterministic logic (if A then B). They cannot answer subjective questions like: *"Has this work been done well enough and deserves to be paid?"* because doing so requires judgment.

**GenLayer** changes this limitation by introducing **Intelligent Contracts**—Python-based smart contracts that can call Large Language Models (LLMs), browse the web, and make subjective decisions, all achieved through decentralized network consensus.

In this beginner-friendly GenLayer tutorial, we will build a **P2P Dispute Resolution** application—an arbitration contract without a third-party intermediary, settled by AI consensus.

---

## Part 1: The Concept of Optimistic Democracy + Equivalence Principle

Before diving into the code, let's understand the two core concepts that make GenLayer truly unique.

### 1.1 Optimistic Democracy Consensus
On GenLayer, when a contract asks for a subjective form of judgment (e.g., *"Is the logo design satisfactory?"*), different AI models might provide different answers.

The **Optimistic Democracy** consensus works like this:
1. The **Leader Validator** executes the contract (calls the LLM, browses the web, and provides a result).
2. The **Follower Validators** independently verify (running the same logic and comparing their outputs with the Leader's).
3. Based on the results, a **Majority Agreement** means the Transaction is Accepted. If a Disagreement occurs, an Appeal process is triggered.

This system is *optimistic* (starting with 5 validators to be fast and cheap), *scalable* (can scale up to 1,000 validators in the event of a dispute), *AI-native*, and provides incentives or penalties according to the majority vote.

### 1.2 The Equivalence Principle
If AI Validator A says *"Yes, the work is satisfactory"* and AI Validator B says *"Yes, the results meet the requirements"*, they essentially agree even though the phrasing is different.

As a developer, you will define what "equivalent" means for each non-deterministic operation. There are two modes:
- `gl.eq_principle_strict_eq`: For numbers or True/False (validators' answers must be identical).
- `gl.eq_principle_prompt_comparative`: For subjective text. Another LLM will be used to judge whether the answers among validators carry the same meaning.

---

## Part 2: Setup (GenLayer CLI, Studio, etc.)

### 2.1 Prerequisites
Ensure your system has the following installed:
- Node.js (v18+)
- Docker (v26+)
- Python (v3.8+)

### 2.2 Install GenLayer CLI
```bash
npm install -g genlayer
genlayer --version
```

### 2.3 Run GenLayer Studio
GenLayer Studio is a local development sandbox (visual IDE + full GenLayer network via Docker).
```bash
genlayer init   # First-time setup
genlayer up     # Starts the Studio
```
Open your browser at **http://localhost:8080** or use the hosted version at **https://studio.genlayer.com**.

---

## Part 3: Python Contract (Dispute Resolver AI Judgment)

This is the **Intelligent Contract** we are building in the repository: `/contracts/dispute_resolver.py`.

The workflow is as follows:
1. The **Employer** submits a complaint with evidence (URL).
2. The **Worker** submits a defense with evidence (URL).
3. The `resolve_dispute()` function is called, and the AI reads both pieces of evidence to determine the winner.
4. Funds are automatically disbursed to the winner.

### Key Code Snippet:
In Python, the *AI magic* part is wrapped in a non-deterministic block as a plain function:

```python
# Part of the dispute_resolver.py file
def ai_judgment() -> str:
    # Read the web and information from parameters
    employer_evidence = gl.get_webpage(employer_url, mode="text")
    worker_evidence = gl.get_webpage(worker_url, mode="text")
    
    prompt = f"""Act as a neutral arbitration board for this dispute.
    ... Job Description, Employer's Claim, Worker's Defense ...
    Determine the winner: EMPLOYER or WORKER.
    """
    return gl.exec_prompt(prompt)

# Using the Equivalence Principle to find an agreement
verdict = gl.eq_principle_prompt_comparative(
    ai_judgment,
    "Does the response clearly state EMPLOYER or WORKER? An agreement is reached if they award the victory to the same party."
)
```

Once an agreement (*verdict*) is reached by the majority of validators, the *state update* process (determining `self.winner`) executes **deterministically**.

---

## Part 4: Testing in GenLayer Studio

1. Open GenLayer Studio (**http://localhost:8080**).
2. Click **"New Contract"**, paste the written code for `dispute_resolver.py`.
3. Enter the *constructor* parameters (the `worker` address, `job_description` message, and `value` representing the escrow asset amount).
4. Click **Deploy** and copy the generated *Contract Address*.

To simulate the Studio UI, you can:
- Call the `submit_employer_evidence` method (passing the URL for the claim/complaint evidence).
- Switch to the *worker* address and call `submit_worker_evidence` (URL for the work report evidence).
- Call `resolve_dispute()`. In the Studio panel, 5 simulated AI validators will deliberate. The winning outcome will appear in the `get_dispute_details()` method as `status: resolved`.

---

## Part 5: React + genlayer-js Frontend

In the `/frontend` directory (Next.js), you utilize the `genlayer-js` installation.

```bash
npm install genlayer-js
```

This frontend reads the state from GenLayer using `@tanstack/react-query` and handles *writeContract* just like in regular Web3 apps, but it connects directly to the Localnet/Testnet.

Example configuration in `genlayer.ts`:
```typescript
import { createClient, createAccount } from "genlayer-js";
import { localnet } from "genlayer-js/chains";

const account = createAccount();
export const client = createClient({
  chain: localnet,
  account,
});
export const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS as `0x${string}`;
```

Users can interact by attaching a URL, and by pressing the *Resolve* button, the `genlayer-js` API system will execute the background process, eventually returning a transaction once the status is `FINALIZED`.

---

## Part 6: AI Resolution Diagram

What truly happens behind the scenes when you click the *"Resolve with AI"* button?

```text
User (Clicks Resolve Dispute)
       ↓ 
[genlayer-js] sends a transaction to the GenLayer Network
       ↓ 
[Network] Selects 5 Validators
       ↓ 
Validator 1 (Leader): 
 - Fetches employer_url & worker_url.
 - Calls the LLM for a decision.
 - Proposes the result: "WORKER wins because specifications are met"
       ↓ 
Validator 2-5 (Followers):
 - Independently fetch and also execute their respective LLMs.
 - Arrive at a similar conclusion that favors the WORKER.
       ↓ 
[Equivalence Principle Check]:
 - Do the semantics of the decisions agree on WORKER? Yes. ✓
 - Consensus is reached.
       ↓ 
*Blockchain State is Updated*
       ↓ 
The Frontend UI automatically loads the final result.
```

---

## Part 7: Next Steps & Further Development

Congratulations! You now have a functional arbitration dApp. Here are some ideas for further development:

- **Deadline-Based Refunds**: An *auto-refund* feature if evidence is not submitted within N blocks of creation (due to a deadlock).
- **Appeal System**: Adding an option to escalate and increase the number of GenLayer validators.
- **Decentralized Evidence Storage**: Utilizing IPFS (e.g., Pinata) rather than just copying raw URLs.

With the tools you've learned, ideas like an *AI Oracle* system, *Subjective P2P Betting*, or an *Automated Worker Reputation System* can now be intelligently built on **GenLayer**.

Don't forget to explore the code and contribute directly to the source repository:
[https://github.com/yoiioy700/genlayer-dispute-resolver](https://github.com/yoiioy700/genlayer-dispute-resolver)