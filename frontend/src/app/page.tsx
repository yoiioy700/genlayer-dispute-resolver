"use client";

import { useState } from "react";

interface Job {
  id: number;
  title: string;
  specifications: string;
  client: string;
  freelancer: string;
  payout_amount: number;
  deliverable: string;
  status: "active" | "submitted" | "resolved_completed" | "resolved_disputed";
  client_pct: number;
  freelancer_pct: number;
  verdict_reason: string;
}

const INITIAL_JOBS: Job[] = [
  {
    id: 0,
    title: "Design Responsive Landing Page for DeFi Protocol",
    specifications:
      "Deliver Figma design with complete mobile & desktop views, dark mode color palette (#060913 base), glassmorphism components, and exported SVG assets.",
    client: "0x7B2a...9E10",
    freelancer: "0x3F4c...A219",
    payout_amount: 1500,
    deliverable:
      "Figma link delivered with full desktop layouts and components. Mobile layout was submitted as wireframe only due to short timeline.",
    status: "resolved_disputed",
    client_pct: 35,
    freelancer_pct: 65,
    verdict_reason:
      "[SPLIT] Freelancer fulfilled the core desktop designs and components excellently, but missed full mobile fidelity spec. Awarded 65% to freelancer and 35% refund to client.",
  },
  {
    id: 1,
    title: "Python Web Scraping & Data Pipeline for Crypto Prices",
    specifications:
      "Python 3.12 async scraper using aiohttp to fetch live orderbook data from 3 DEXes every 5 seconds, storing into PostgreSQL with unit tests.",
    client: "0x1A8b...C394",
    freelancer: "0x9E4d...F820",
    payout_amount: 800,
    deliverable:
      "GitHub repo delivered with async scraper, docker-compose PostgreSQL setup, and 95% test coverage passing.",
    status: "resolved_completed",
    client_pct: 0,
    freelancer_pct: 100,
    verdict_reason: "Client directly approved deliverable with 100% payout.",
  },
  {
    id: 2,
    title: "Write Smart Contract Security Audit Report",
    specifications:
      "Comprehensive audit report covering reentrancy, access control, frontrunning risks for 4 Solidity contracts with severity classifications.",
    client: "0x5C2e...D147",
    freelancer: "0x8B1a...E633",
    payout_amount: 2200,
    deliverable:
      "Full 18-page PDF report with 3 High, 2 Medium, 5 Low vulnerabilities detailed with remediation snippets.",
    status: "submitted",
    client_pct: 0,
    freelancer_pct: 0,
    verdict_reason: "",
  },
];

export default function Home() {
  const [jobs, setJobs] = useState<Job[]>(INITIAL_JOBS);
  const [title, setTitle] = useState("");
  const [specs, setSpecs] = useState("");
  const [freelancer, setFreelancer] = useState("");
  const [amount, setAmount] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  // Dispute modal / inputs
  const [activeJobForDispute, setActiveJobForDispute] = useState<number | null>(
    null
  );
  const [clientClaim, setClientClaim] = useState("");
  const [freelancerClaim, setFreelancerClaim] = useState("");

  const handleCreateJob = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !specs || !freelancer || !amount) return;

    const newJob: Job = {
      id: jobs.length,
      title,
      specifications: specs,
      client: "0xYou...User",
      freelancer,
      payout_amount: Number(amount),
      deliverable: "",
      status: "active",
      client_pct: 0,
      freelancer_pct: 0,
      verdict_reason: "",
    };

    setJobs([newJob, ...jobs]);
    setTitle("");
    setSpecs("");
    setFreelancer("");
    setAmount("");
  };

  const handleTriggerDispute = async (jobId: number) => {
    if (!clientClaim || !freelancerClaim) return;
    setIsProcessing(true);

    // Simulate AI Consensus
    await new Promise((r) => setTimeout(r, 2500));

    const freelancerPct = Math.floor(Math.random() * 40) + 40; // 40-80%
    const clientPct = 100 - freelancerPct;
    const decision =
      freelancerPct > 60
        ? "FAVOR_FREELANCER"
        : freelancerPct < 40
        ? "FAVOR_CLIENT"
        : "SPLIT";

    setJobs((prev) =>
      prev.map((j) =>
        j.id === jobId
          ? {
              ...j,
              status: "resolved_disputed",
              freelancer_pct: freelancerPct,
              client_pct: clientPct,
              verdict_reason: `[${decision}] GenLayer AI consensus determined that freelancer gets ${freelancerPct}% and client receives ${clientPct}% refund based on deliverable quality vs requirements.`,
            }
          : j
      )
    );

    setIsProcessing(false);
    setActiveJobForDispute(null);
    setClientClaim("");
    setFreelancerClaim("");
  };

  const totalEscrow = jobs.reduce((acc, j) => acc + j.payout_amount, 0);
  const disputedCount = jobs.filter(
    (j) => j.status === "resolved_disputed"
  ).length;

  return (
    <div className="container">
      {/* Nav */}
      <nav className="navbar">
        <div className="logo">
          <span>⚖️ GenLayer Escrow</span>
          <span className="logo-badge">Intelligent Contract</span>
        </div>
        <div>
          <span
            style={{
              fontSize: 13,
              color: "var(--accent-cyan)",
              fontWeight: 600,
            }}
          >
            ● GenLayer Studio Connected
          </span>
        </div>
      </nav>

      {/* Hero */}
      <section className="hero">
        <div className="hero-pill">🤖 The Adjudication Layer for Work</div>
        <h1>
          Decentralized Freelance Escrow &{" "}
          <span className="gradient-text">AI Dispute Resolution</span>
        </h1>
        <p>
          Milestone payments governed by GenLayer Intelligent Contracts. When
          deliverables are disputed, decentralized AI validators reach consensus
          on fair fund distribution.
        </p>
      </section>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-box">
          <div className="num" style={{ color: "var(--accent-cyan)" }}>
            ${totalEscrow.toLocaleString()}
          </div>
          <div className="lbl">Total Escrow Value</div>
        </div>
        <div className="stat-box">
          <div className="num">{jobs.length}</div>
          <div className="lbl">Total Contracts</div>
        </div>
        <div className="stat-box">
          <div className="num" style={{ color: "var(--accent-emerald)" }}>
            {jobs.filter((j) => j.status.startsWith("resolved")).length}
          </div>
          <div className="lbl">Settled Jobs</div>
        </div>
        <div className="stat-box">
          <div className="num" style={{ color: "var(--accent-purple)" }}>
            {disputedCount}
          </div>
          <div className="lbl">AI Adjudicated</div>
        </div>
      </div>

      {/* Content Grid */}
      <div className="content-grid">
        {/* Create Job Form */}
        <div className="card">
          <div className="card-title">Create Escrow Job</div>
          <div className="card-subtitle">
            Lock funds into the Intelligent Contract
          </div>

          <form onSubmit={handleCreateJob}>
            <div className="form-group">
              <label className="form-label">Job Title</label>
              <input
                className="form-input"
                placeholder="e.g. Build Web3 Staking Dashboard"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Specifications & Criteria</label>
              <textarea
                className="form-textarea"
                placeholder="Clearly define deliverables, deadlines, and quality requirements..."
                value={specs}
                onChange={(e) => setSpecs(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Freelancer Address</label>
              <input
                className="form-input"
                placeholder="0x..."
                value={freelancer}
                onChange={(e) => setFreelancer(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Escrow Amount ($ / GEN)</label>
              <input
                type="number"
                className="form-input"
                placeholder="1000"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn-primary">
              Lock Escrow & Deploy
            </button>
          </form>
        </div>

        {/* Jobs List */}
        <div>
          <h2 style={{ fontSize: 20, fontWeight: 700, marginBottom: 20 }}>
            Active & Resolved Contracts ({jobs.length})
          </h2>

          <div className="jobs-list">
            {jobs.map((job) => (
              <div key={job.id} className="job-card">
                <div className="job-header">
                  <div>
                    <div className="job-title">{job.title}</div>
                    <div
                      style={{
                        fontSize: 12,
                        color: "var(--text-muted)",
                        marginTop: 4,
                      }}
                    >
                      Client: {job.client} → Freelancer: {job.freelancer}
                    </div>
                  </div>
                  <span
                    className={`badge ${
                      job.status === "active"
                        ? "badge-active"
                        : job.status === "submitted"
                        ? "badge-submitted"
                        : "badge-resolved"
                    }`}
                  >
                    {job.status.replace("_", " ")}
                  </span>
                </div>

                <div className="job-specs">
                  <strong>Specs:</strong> {job.specifications}
                </div>

                {job.deliverable && (
                  <div
                    className="job-specs"
                    style={{
                      background: "rgba(255,255,255,0.02)",
                      padding: 10,
                      borderRadius: 8,
                    }}
                  >
                    <strong>Delivered:</strong> {job.deliverable}
                  </div>
                )}

                {/* Progress / Payout allocation if resolved */}
                {job.status.startsWith("resolved") ? (
                  <div className="payout-bar-wrap">
                    <div className="payout-labels">
                      <span style={{ color: "var(--accent-emerald)" }}>
                        Freelancer: {job.freelancer_pct}% ($
                        {(
                          (job.payout_amount * job.freelancer_pct) /
                          100
                        ).toLocaleString()}
                        )
                      </span>
                      <span style={{ color: "var(--accent-cyan)" }}>
                        Client Refund: {job.client_pct}% ($
                        {(
                          (job.payout_amount * job.client_pct) /
                          100
                        ).toLocaleString()}
                        )
                      </span>
                    </div>
                    <div className="payout-progress">
                      <div
                        className="progress-freelancer"
                        style={{ width: `${job.freelancer_pct}%` }}
                      />
                      <div
                        className="progress-client"
                        style={{ width: `${job.client_pct}%` }}
                      />
                    </div>
                    {job.verdict_reason && (
                      <div className="verdict-box">
                        <strong>AI Consensus Adjudication:</strong>{" "}
                        {job.verdict_reason}
                      </div>
                    )}
                  </div>
                ) : (
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      marginTop: 16,
                    }}
                  >
                    <span style={{ fontSize: 14, fontWeight: 700 }}>
                      Escrow: ${job.payout_amount.toLocaleString()}
                    </span>
                    <button
                      onClick={() => setActiveJobForDispute(job.id)}
                      className="btn-primary"
                      style={{
                        width: "auto",
                        padding: "8px 16px",
                        fontSize: 13,
                        background: "rgba(244, 63, 94, 0.2)",
                        border: "1px solid rgba(244, 63, 94, 0.4)",
                        color: "#f43f5e",
                        boxShadow: "none",
                      }}
                    >
                      ⚡ Raise AI Dispute
                    </button>
                  </div>
                )}

                {/* Dispute Form Modal / Drawer if selected */}
                {activeJobForDispute === job.id && (
                  <div
                    style={{
                      marginTop: 20,
                      padding: 16,
                      background: "rgba(0,0,0,0.3)",
                      borderRadius: 12,
                      border: "1px solid rgba(244, 63, 94, 0.3)",
                    }}
                  >
                    <div
                      style={{
                        fontSize: 14,
                        fontWeight: 700,
                        marginBottom: 12,
                        color: "#f43f5e",
                      }}
                    >
                      ⚖️ Trigger GenLayer AI Validator Consensus
                    </div>
                    <div className="form-group">
                      <label className="form-label">Client Claim</label>
                      <input
                        className="form-input"
                        placeholder="Why do you think the work is incomplete or unsatisfactory?"
                        value={clientClaim}
                        onChange={(e) => setClientClaim(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label className="form-label">Freelancer Claim</label>
                      <input
                        className="form-input"
                        placeholder="Why do you believe you satisfied the requirements?"
                        value={freelancerClaim}
                        onChange={(e) => setFreelancerClaim(e.target.value)}
                      />
                    </div>
                    <div style={{ display: "flex", gap: 10 }}>
                      <button
                        onClick={() => handleTriggerDispute(job.id)}
                        disabled={isProcessing}
                        className="btn-primary"
                      >
                        {isProcessing
                          ? "AI Validators Adjudicating..."
                          : "Submit to AI Consensus"}
                      </button>
                      <button
                        onClick={() => setActiveJobForDispute(null)}
                        style={{
                          padding: "10px 16px",
                          background: "transparent",
                          border: "1px solid var(--border-glass)",
                          color: "var(--text-muted)",
                          borderRadius: 8,
                          cursor: "pointer",
                        }}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>
          Powered by{" "}
          <a
            href="https://genlayer.com"
            target="_blank"
            rel="noreferrer"
            style={{ color: "var(--accent-cyan)", textDecoration: "none" }}
          >
            GenLayer
          </a>{" "}
          — Decentralized AI Adjudication
        </p>
      </footer>
    </div>
  );
}
