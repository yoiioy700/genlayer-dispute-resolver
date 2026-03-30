# GenLayer Dispute Resolver

Welcome to the **GenLayer Dispute Resolver**! This is a P2P dispute resolution dApp (Decentralized Application) built on GenLayer. It serves as an arbitration contract without a third-party human intermediary, relying entirely on AI consensus to resolve disputes.

## How It Works

Traditional blockchains rely on deterministic logic. GenLayer changes the paradigm by introducing **Intelligent Contracts**—smart contracts that can read web pages, query Large Language Models (LLMs), and make subjective decisions via a decentralized network of validators.

This project specifically leverages two of GenLayer's core innovations:

1. **Optimistic Democracy:** The network starts with a small group of validators (e.g., 5) to process a subjective AI decision. If they agree, the transaction is fast and cheap. If they disagree, an appeal process begins with more validators.
2. **Equivalence Principle:** Since AI models might phrase their answers differently, GenLayer uses an Equivalence Principle. For text-based judgments, the network evaluates whether the semantic meaning of the validators' conclusions is identical (e.g., whether both agree the "Worker" or the "Employer" wins), achieving consensus despite varying phrasing.

For an in-depth explanation and a step-by-step walkthrough of building this contract, please read our comprehensive [Tutorial](TUTORIAL.md).

## Setup Instructions

### Prerequisites
Before you begin, ensure you have the following installed on your machine:
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Docker](https://www.docker.com/) (v26 or higher)
- [Python](https://www.python.org/) (v3.8 or higher)

### 1. Install GenLayer CLI
Install the GenLayer Command Line Interface globally via npm:
```bash
npm install -g genlayer
genlayer --version
```

### 2. Run GenLayer Studio
GenLayer Studio provides a local sandboxed environment to develop, deploy, and interact with your contracts.

To initialize and start the local environment:
```bash
genlayer init
genlayer up
```

Once running, you can access the Studio in your browser at [http://localhost:8080](http://localhost:8080) or via the hosted interface at [https://studio.genlayer.com](https://studio.genlayer.com).

## Next Steps
Head over to the [TUTORIAL.md](TUTORIAL.md) for a detailed guide on how to deploy the dispute resolver contract, test it in GenLayer Studio, and connect it with the frontend.