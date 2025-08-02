<h1 align="center">🕹️ Data Dash — real-time metrics game on AWS EKS</h1>

<p align="center">
  <img src="diagrams/datadash-banner.png" width="500"/>
</p>

> **What it is**  
> A tiny FastAPI + JavaScript WebSocket game that streams fake events and renders live KPIs.  
> **Where it runs**  
> Fully containerised, pushed to Amazon ECR, and deployed on **EKS Fargate** behind an **Application Load Balancer**.

---

## 📐 Architecture

```mermaid
flowchart LR
    Browser -->|WS / HTTP| ALB
    ALB --> Service
    Service --> Pod[(FastAPI ≅ WS + Static HTML)]
    subgraph Amazon EKS (Fargate)
      Pod
    end
