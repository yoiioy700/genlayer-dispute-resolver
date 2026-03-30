import json
from typing import Dict, List, Any

class DisputeResolver:
    def __init__(self):
        # We store cases in memory for this simple example
        self.cases = {}
        self.case_counter = 0

    def create_case(self, title: str, description: str, evidence: List[str]) -> int:
        \"\"\"Create a new dispute case.\"\"\"
        self.case_counter += 1
        case_id = self.case_counter
        
        self.cases[case_id] = {
            "id": case_id,
            "title": title,
            "description": description,
            "evidence": evidence,
            "status": "open",
            "votes": {"plaintiff": 0, "defendant": 0},
            "voters": set()
        }
        return case_id

    def get_case(self, case_id: int) -> Dict[str, Any]:
        \"\"\"Retrieve a case by ID.\"\"\"
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
        
        # Format for return (convert set to list for JSON serialization)
        case = self.cases[case_id].copy()
        case["voters"] = list(case["voters"])
        return case

    def vote(self, case_id: int, voter_id: str, vote_for: str) -> bool:
        \"\"\"Vote on an open case.\"\"\"
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
            
        case = self.cases[case_id]
        
        if case["status"] != "open":
            raise ValueError(f"Case {case_id} is no longer open")
            
        if voter_id in case["voters"]:
            raise ValueError(f"Voter {voter_id} has already voted on this case")
            
        if vote_for not in ["plaintiff", "defendant"]:
            raise ValueError("Vote must be either 'plaintiff' or 'defendant'")
            
        case["votes"][vote_for] += 1
        case["voters"].add(voter_id)
        
        return True

    def resolve_case(self, case_id: int) -> str:
        \"\"\"Resolve a case based on votes.\"\"\"
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
            
        case = self.cases[case_id]
        
        if case["status"] != "open":
            return case["resolution"]
            
        votes = case["votes"]
        
        if votes["plaintiff"] > votes["defendant"]:
            resolution = "plaintiff_wins"
        elif votes["defendant"] > votes["plaintiff"]:
            resolution = "defendant_wins"
        else:
            resolution = "tie"
            
        case["status"] = "resolved"
        case["resolution"] = resolution
        
        return resolution
