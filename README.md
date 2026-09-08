# Text-to-SQL Agent

An end-to-end AI agent system that converts natural-language questions into
executable SQL queries across PostgreSQL, MySQL, and MongoDB databases.

## Overview
The Text-to-SQL Agent lets users ask questions in plain English and receive
accurate, executable database queries. Built with LangGraph and FastAPI, the
system orchestrates an agent workflow that interprets the question, generates
the query, validates it, and executes it against the connected database.

## Features
- Natural-language to SQL query generation
- Multi-database support: PostgreSQL, MySQL, MongoDB
- Agent orchestration with LangGraph
- REST API built with FastAPI
- Dockerised deployment

## Tech Stack
- Agent Framework: LangGraph
- API: FastAPI
- Databases: PostgreSQL, MySQL, MongoDB
- Language: Python (managed with uv)
- Deployment: Docker

## How to Run
# Docker
docker build -t text-to-sql-agent .
docker run -p 8000:8000 text-to-sql-agent

# Locally
git clone https://github.com/Trupal-Mendpara/Text-to-SQL-Agent.git
cd Text-to-SQL-Agent
uv sync
uv run [confirm entry command]

## Example Usage
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the top 5 customers by total order value?"}'

## Author
Trupal Mendpara
