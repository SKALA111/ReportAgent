# AI Startup Investment Evaluation Agent

국내외 AI 스타트업에 대해 조사하고 기술력, 시장성, 재무 상태 등을 고려해 투자 판단을 내리는 에이전트를 설계하고 구현한 실습 프로젝트입니다.

## Overview

- Objective
  - AI 스타트업의 핵심 기술력, 시장성, 재무 상태 등을 기반으로 투자 적합성 분석하는 에이전트 시스템 구축
- Method
  - LangGraph + Agentic RAG 
- Tools
  - LLM: OpenAI GPT-4  
  - Web Search: Serper API (Google 기반 검색)  
  - Vector DB: Chroma + SentenceTransformer  
  - Orchestration: LangGraph  
  - Env 관리: python-dotenv  

## Features

- 웹 기반 스타트업 정보 수집 및 요약 (검색 API + LLM 기반)
- 투자 기준별 판단 분류 (기술력, 시장성, 재무 상태 등)
- 종합 투자 판단 자동화 ('추천' / '보류' / '기각')

## Tech Stack 

| Category     | Details                                |
|--------------|----------------------------------------|
| Framework    | LangGraph, LangChain, Python           |
| LLM          | GPT-4 via OpenAI API                   |
| Retrieval    | Chroma + SentenceTransformers          |
| Search API   | Serper API (Google 기반 웹 검색)        |
|--------------|----------------------------------------|

## Agents
 
- Search Agent: 스타트업 분석
- Tech Agent: 핵심 기술 분석
- Market Agent: 시장 경쟁 분석
- Finance Agent: 재무 상태 분석
- Investment Agent: 투자 결정 판단
- Report Agent: 종합 문서 작성

## Architecture
![architecture](./assets/architecture.png)

## Directory Structure
```
project-root/
│
├── data/                  # 스타트업 리스트 및 관련 문서
│   ├── startups.csv
│
├── agents/                # 평가 기준별 Agent 모듈
│   ├── search_agent.py
│   ├── tech_agent.py
│   ├── market_agent.py
│   ├── finance_agent.py
│   ├── investment_agent.py
│   └── report_agent.py
│
├── prompts/               # 프롬프트 템플릿 및 기준
│   └── prompts.py
│
├── models/                # LLM 호출 관련 모듈 정의
│   └── llm_wrapper.py
├── outputs/               # 평가 결과 및 보고서 저장
│   └── results.json
│
├── app.py                 # 전체 분석 실행 스크립트
└── README.md              # 프로젝트 설명
```

## Contributors 
- 강창진
- 김민혁
- 김준혁
- 김효준
