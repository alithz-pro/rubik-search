# Rubik Search — AI Search Algorithms

An AI course project exploring different search strategies for solving the Rubik's Cube, including **uninformed search, informed search, local search, and metaheuristic optimization using Genetic Algorithms**.

The project was developed as an assignment for the Artificial Intelligence course at Shahid Beheshti University, with the goal of implementing and exploring different approaches to search and optimization problems.

> **Project type:** AI course assignment  
> **Problem domain:** Rubik's Cube solving  
> **Focus:** Search algorithms, heuristics, local search, and genetic algorithms

---

## Overview

The Rubik's Cube provides a challenging state-space search problem with a large number of possible configurations and a relatively small set of actions available at each state.

This project explores different AI approaches to the problem, from systematic search strategies that explore the state space to heuristic-driven and optimization-based approaches that attempt to find solutions more efficiently.

The assignment covers four major search categories:

- Uninformed Search
- Informed Search
- Local Search
- Metaheuristic Search — Genetic Algorithm

---

## Search Approaches

### 1. Uninformed Search

Uninformed algorithms explore the state space without relying on domain-specific heuristic estimates of how close a state is to the goal.

This category provides a baseline for understanding state exploration, search-tree expansion, and the computational challenges of solving complex puzzles.

Algorithms studied in this category include the applicable blind-search methods implemented in the project.

### 2. Informed Search

Informed search algorithms use heuristic information to guide the exploration toward more promising states.

The goal is to reduce unnecessary exploration by estimating how far a current state is from the target state.

Topics covered include:

- Heuristic functions
- State evaluation
- Search prioritization
- Path cost
- Goal-directed exploration

### 3. Local Search

Local search approaches operate by exploring neighboring candidate states and attempting to improve the current solution according to an evaluation function.

Unlike traditional tree-search methods, local search can focus on improving a candidate solution rather than systematically exploring paths from the initial state.

This approach introduces concepts such as:

- Neighborhoods
- Candidate solutions
- Evaluation functions
- Iterative improvement
- Search landscapes

### 4. Metaheuristic Search — Genetic Algorithm

The project also explores Genetic Algorithms (GA), an optimization approach inspired by biological evolution.

A population of candidate solutions is iteratively evolved through operations such as:

- Population initialization
- Fitness evaluation
- Selection
- Crossover
- Mutation
- Generational replacement

The objective is to improve candidate solutions over successive generations using a fitness function related to the puzzle-solving goal.

---

## AI Concepts

The project provides practical exposure to several fundamental AI concepts:

- State-space representation
- Initial and goal states
- Actions and transitions
- Search trees and graphs
- Search frontier
- Heuristic evaluation
- Fitness functions
- Neighborhood exploration
- Optimization
- Exploration strategies
- Algorithmic trade-offs

---

## Problem-Solving Perspective

The project explores how different algorithmic approaches behave when applied to the same puzzle domain.

Traditional search algorithms explore states according to their respective strategies, while heuristic and optimization-based approaches attempt to guide exploration toward promising candidates.

This provides a practical way to study the differences between systematic search, heuristic guidance, and iterative optimization.

---

## Course Context

This project was developed as part of the Artificial Intelligence course at Shahid Beheshti University.

The assignment focused on implementing and understanding several categories of AI search algorithms and applying them to the Rubik's Cube problem.

---

## Learning Goals

- Understanding state-space search
- Implementing AI search algorithms
- Comparing uninformed and informed approaches
- Designing and using heuristics
- Exploring local-search strategies
- Understanding genetic algorithms
- Applying optimization techniques to combinatorial problems
- Analyzing algorithmic trade-offs

---

## Educational Scope

This repository is an educational AI project. Its purpose is to explore and implement search and optimization methods in the context of a puzzle problem, rather than provide a competitive or production-grade Rubik's Cube solver.

---

## Disclaimer

This project is an educational implementation for coursework and is not affiliated with or endorsed by the official Rubik's Cube brand or its owners.
