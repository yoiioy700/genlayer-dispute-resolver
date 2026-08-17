# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json


class FreelanceDisputeResolver(gl.Contract):
    """
    An Intelligent Contract for decentralized freelance escrow & dispute adjudication.

    When clients and freelancers have a dispute over milestone deliverables,
    GenLayer AI validators independently evaluate the original task specifications,
    the submitted deliverable, and the dispute arguments to reach consensus
    on a fair fund distribution percentage.
    """

    job_count: u256

    def __init__(self):
        self.job_count = u256(0)

    @gl.public.write
    def create_job(
        self,
        title: str,
        specifications: str,
        freelancer: Address,
        payout_amount: u256,
    ) -> u256:
        """
        Create a new freelance job escrow.

        Args:
            title: Job title
            specifications: Detailed work requirements and criteria
            freelancer: Freelancer's wallet address
            payout_amount: Escrow amount allocated for this job
        """
        if len(title) < 5:
            raise gl.vm.UserError("Job title must be at least 5 characters")
        if len(specifications) < 30:
            raise gl.vm.UserError(
                "Specifications must be at least 30 characters of clear criteria"
            )
        if payout_amount == u256(0):
            raise gl.vm.UserError("Payout amount must be greater than zero")

        job_id = int(self.job_count)
        job_data = {
            "id": job_id,
            "title": title,
            "specifications": specifications,
            "client": str(gl.message.sender_account),
            "freelancer": str(freelancer),
            "payout_amount": int(payout_amount),
            "deliverable": "",
            "status": "active",  # active, submitted, resolved_completed, resolved_disputed
            "client_pct": 0,
            "freelancer_pct": 0,
            "verdict_reason": "",
        }

        gl.storage.put(f"job_{job_id}", json.dumps(job_data))
        self.job_count = u256(job_id + 1)
        return u256(job_id)

    @gl.public.write
    def submit_deliverable(self, job_id: u256, deliverable_content: str) -> None:
        """Freelancer submits the deliverable for review."""
        raw_data = gl.storage.get(f"job_{int(job_id)}")
        if raw_data is None:
            raise gl.vm.UserError("Job not found")

        job = json.loads(raw_data)
        if str(gl.message.sender_account) != job["freelancer"]:
            raise gl.vm.UserError("Only the assigned freelancer can submit deliverable")
        if job["status"] != "active":
            raise gl.vm.UserError(f"Cannot submit deliverable in status {job['status']}")
        if len(deliverable_content) < 20:
            raise gl.vm.UserError("Deliverable content is too short")

        job["deliverable"] = deliverable_content
        job["status"] = "submitted"
        gl.storage.put(f"job_{int(job_id)}", json.dumps(job))

    @gl.public.write
    def complete_job(self, job_id: u256) -> None:
        """Client approves the deliverable and releases 100% of escrow to freelancer."""
        raw_data = gl.storage.get(f"job_{int(job_id)}")
        if raw_data is None:
            raise gl.vm.UserError("Job not found")

        job = json.loads(raw_data)
        if str(gl.message.sender_account) != job["client"]:
            raise gl.vm.UserError("Only the client can approve and complete the job")
        if job["status"] != "submitted":
            raise gl.vm.UserError("Deliverable has not been submitted yet")

        job["status"] = "resolved_completed"
        job["freelancer_pct"] = 100
        job["client_pct"] = 0
        job["verdict_reason"] = "Client directly approved deliverable."
        gl.storage.put(f"job_{int(job_id)}", json.dumps(job))

    @gl.public.write
    def adjudicate_dispute(
        self, job_id: u256, client_claim: str, freelancer_claim: str
    ) -> None:
        """
        AI-Validator consensus adjudication for contested deliverables.

        Validators evaluate the original specifications against the deliverable
        and both parties' claims to reach consensus on fund allocation (0-100%).
        """
        raw_data = gl.storage.get(f"job_{int(job_id)}")
        if raw_data is None:
            raise gl.vm.UserError("Job not found")

        job = json.loads(raw_data)
        sender = str(gl.message.sender_account)
        if sender != job["client"] and sender != job["freelancer"]:
            raise gl.vm.UserError(
                "Only involved client or freelancer can trigger dispute adjudication"
            )
        if job["status"] != "submitted" and job["status"] != "active":
            raise gl.vm.UserError("Job is already resolved")

        prompt = f"""You are a neutral decentralized arbitrator on GenLayer.
Evaluate this freelance contract dispute:

Title: {job['title']}
Original Specifications: {job['specifications']}
Submitted Deliverable: {job['deliverable']}
Client's Claim: "{client_claim}"
Freelancer's Claim: "{freelancer_claim}"

Rules:
1. Determine what percentage of the agreed fee the freelancer earned (0 to 100).
2. The client gets the remainder (100 - freelancer_percent).
3. If deliverable satisfies requirements substantially, award high percentage to freelancer.
4. If deliverable fails core requirements, award refund (high percentage) to client.

Respond with strict JSON ONLY:
{{"freelancer_pct": <integer 0-100>, "client_pct": <integer 0-100>, "decision": "<favor_freelancer or favor_client or split>", "reason": "<two sentence justification>"}}"""

        def leader_fn():
            res_str = gl.nondet.exec_prompt(prompt)
            return json.loads(res_str)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            leader_data = leaders_res.calldata
            my_raw = gl.nondet.exec_prompt(prompt)
            my_data = json.loads(my_raw)

            # Equivalence Principle: Decisions must match, and freelancer_pct within +/- 15% tolerance
            decision_match = my_data["decision"] == leader_data["decision"]
            pct_close = (
                abs(my_data["freelancer_pct"] - leader_data["freelancer_pct"]) <= 15
            )
            return decision_match and pct_close

        result = gl.vm.run_nondet(leader_fn, validator_fn)

        job["status"] = "resolved_disputed"
        job["freelancer_pct"] = result["freelancer_pct"]
        job["client_pct"] = 100 - result["freelancer_pct"]
        job["verdict_reason"] = (
            f"[{result['decision'].upper()}] {result.get('reason', '')}"
        )
        gl.storage.put(f"job_{int(job_id)}", json.dumps(job))

    @gl.public.view
    def get_job(self, job_id: u256) -> str:
        """Get details and adjudication status of a job."""
        data = gl.storage.get(f"job_{int(job_id)}")
        if data is None:
            raise gl.vm.UserError("Job not found")
        return data

    @gl.public.view
    def get_job_count(self) -> u256:
        """Get total count of created jobs."""
        return self.job_count
