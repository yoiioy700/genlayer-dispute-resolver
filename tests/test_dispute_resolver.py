# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from genlayer.testing import direct_mode
import pytest


def test_contract_initial_state():
    """Verify initial contract state has 0 jobs."""
    with direct_mode() as dm:
        contract = dm.deploy("contracts/dispute_resolver.py")
        count = dm.call(contract, "get_job_count")
        assert count == 0


def test_create_job_validation():
    """Verify input validation rules on job creation."""
    with direct_mode() as dm:
        contract = dm.deploy("contracts/dispute_resolver.py")

        # Short title
        with pytest.raises(Exception, match="Job title must be at least"):
            dm.call(
                contract,
                "create_job",
                "App",
                "Valid specs that meet the requirement length.",
                "0x1111111111111111111111111111111111111111",
                100,
            )

        # Short specs
        with pytest.raises(Exception, match="Specifications must be at least"):
            dm.call(
                contract,
                "create_job",
                "Valid Job Title",
                "Too short",
                "0x1111111111111111111111111111111111111111",
                100,
            )


def test_get_nonexistent_job():
    """Verify querying non-existent job raises proper error."""
    with direct_mode() as dm:
        contract = dm.deploy("contracts/dispute_resolver.py")
        with pytest.raises(Exception, match="Job not found"):
            dm.call(contract, "get_job", 999)
