# Implementing Dijkstra Algorithm on Capacitated Networks

This repository contains a Python implementation of **Dijkstra's algorithm** on a **capacitated network**, allowing us to find **shortest-cost paths** and send **flows** from a source to a sink. It also includes a **visualization** of the network showing **flows, capacities, and costs** on each edge.

## Problem Description

We are given a directed network with:

- **Nodes** (representing junctions, servers, or stations)  
- **Edges** connecting nodes, each with:
  - **Capacity**: maximum flow the edge can carry  
  - **Cost**: cost per unit of flow along the edge  

**Goal:** Send a **specified total flow** from a **source node** to a **sink node** while minimizing the total cost.

**Example network in this code:**

| Edge | Capacity | Cost |
|------|---------|------|
| 0 → 1 | 15 | 2 |
| 0 → 2 | 7  | 4 |
| 1 → 3 | 10 | 1 |
| 2 → 3 | 10 | 2 |
| 2 → 4 | 8  | 3 |
| 3 → 5 | 9  | 2 |
| 4 → 5 | 13 | 1 |

- **Source node:** 0  
- **Sink node:** 5  
- **Total flow to send:** 15  


