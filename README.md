# AI Startup Investment Evaluation Agent
본 프로젝트는 인공지능 스타트업에 대한 투자 가능성을 자동으로 평가하는 에이전트를 설계하고 구현한 실습 프로젝트입니다.

## Overview

- Objective : AI 스타트업의 기술력, 시장성, 리스크 등을 기준으로 투자 적합성 분석
- Method : AI Agent + Agentic RAG 
- Tools : 도구A, 도구B, 도구C

## Features

- PDF 자료 기반 정보 추출 (예: IR 자료, 기사 등)
- 투자 기준별 판단 분류 (시장성, 팀, 기술력 등)
- 종합 투자 요약 출력 (예: 투자 유망 / 보류 / 회피)

## Tech Stack 

| Category   | Details                      |
|------------|------------------------------|
| Framework  | LangGraph, LangChain, Python |
| LLM        | GPT-4o-mini via OpenAI API   |
| Retrieval  | FAISS, Chroma                |

## Agents
 
- Agent A: Assesses technical competitiveness
- Agent B: Evaluates market opportunity and team capability

## Architecture
(그래프 이미지)

## Directory Structure
project-root/
│
├── data/                  # 스타트업 관련 PDF 및 원본 문서
│   ├── sample1.pdf
│   └── sample2.pdf
│
├── agents/                # 평가 기준별 Agent 모듈
│   ├── search_agent.py
│   ├── tech_agent.py
│   ├── market_agent.py
│   ├── owner_agent.py
│   ├── finance_agent.py
│   ├── investment_agent.py
│   └── report_agent.py
│
├── prompts/               # 프롬프트 템플릿 및 기준
│   ├── base_templates.py
│   └── scoring_criteria.json
│
├── outputs/               # 평가 결과 및 보고서 저장
│   ├── results.json
│   └── final_report.md
│
├── app.py                 # 전체 분석 실행 스크립트
└── README.md              # 프로젝트 설명


## Contributors 
- 강창진
- 김민혁
- 김준혁
- 김효준
