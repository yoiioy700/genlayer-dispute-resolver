# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
from dataclasses import dataclass
from genlayer import *


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


class AIArbitratorEscrow(gl.Contract):
    cases: TreeMap[str, DisputeCase]
    total_cases: u256

    def __init__(self):
        self.cases = TreeMap()
        self.total_cases = u256(0)

    @gl.public.write
    def create_case(
        self,
        case_id: str,
        freelancer_addr: str,
        amount_wei: u256,
        requirements: str
    ) -> str:
        client_addr = gl.message.sender_address
        freelancer = Address(freelancer_addr) if isinstance(freelancer_addr, (str, bytes)) else freelancer_addr
        
        new_case = DisputeCase(
            case_id=case_id,
            client=client_addr,
            freelancer=freelancer,
            amount=u256(int(amount_wei)),
            requirements=requirements,
            deliverable="",
            status="CREATED",
            verdict="PENDING",
            client_share_pct=u256(0),
            reason=""
        )
        self.cases[case_id] = new_case
        self.total_cases = u256(int(self.total_cases) + 1)
        return case_id

    @gl.public.write
    def submit_deliverable(self, case_id: str, deliverable: str) -> None:
        case = self.cases[case_id]
        case.deliverable = deliverable
        case.status = "SUBMITTED"
        self.cases[case_id] = case

    @gl.public.write
    def adjudicate_dispute(self, case_id: str) -> dict:
        case = self.cases[case_id]
        
        # Extract storage values to local primitive strings before nondet execution
        req_text = str(case.requirements)
        deliv_text = str(case.deliverable)

        def evaluate_case() -> str:
            prompt = f"""You are a decentralized dispute arbitrator evaluating a freelance delivery.

Requirements:
{req_text}

Submitted Deliverable:
{deliv_text}

Analyze whether the deliverable fulfills the agreed requirements.
Decide the verdict:
- "FREELANCER" if requirements are fully or substantially met (100% to freelancer).
- "CLIENT" if deliverable is entirely missing, fraudulent, or failed (0% to freelancer).
- "SPLIT" if partially completed.

Respond ONLY with valid JSON with this exact schema:
{{
    "verdict": "FREELANCER" | "CLIENT" | "SPLIT",
    "client_share_pct": int, // 0 if FREELANCER, 100 if CLIENT, or 50 if SPLIT
    "reason": "concise explanation"
}}
"""
            res = gl.nondet.exec_prompt(prompt, response_format="json")
            return json.dumps(res, sort_keys=True)

        # Reach consensus across validator committee using Equivalence Principle
        consensus_res_str = gl.eq_principle.strict_eq(evaluate_case)
        result = json.loads(consensus_res_str)

        case.verdict = result.get("verdict", "SPLIT")
        case.client_share_pct = u256(int(result.get("client_share_pct", 50)))
        case.reason = result.get("reason", "Consensus adjudication")
        case.status = "RESOLVED"
        self.cases[case_id] = case

        return result

    @gl.public.view
    def get_case(self, case_id: str) -> dict:
        case = self.cases[case_id]
        return {
            "case_id": case.case_id,
            "client": str(case.client),
            "freelancer": str(case.freelancer),
            "amount": int(case.amount),
            "requirements": case.requirements,
            "deliverable": case.deliverable,
            "status": case.status,
            "verdict": case.verdict,
            "client_share_pct": int(case.client_share_pct),
            "reason": case.reason
        }

    @gl.public.view
    def get_total_cases(self) -> int:
        return int(self.total_cases)
