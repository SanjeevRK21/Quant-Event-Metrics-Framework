# Quant Event Metrics Framework
### Modular Financial Intelligence System with Local LLM Integration
A scalable, event-driven stock analytics framework that combines quantitative finance models with LLM-powered interpretation and a context-aware research chatbot.This project demonstrates system design, financial modeling, modular architecture, and AI integration in a production-style structure.

## What This Project Demonstrates
1. Layered system architecture  
2. Event-based pipeline design  
3. Quantitative financial modeling  
4. Prompt engineering & LLM grounding  
5. Local LLM deployment (Ollama)  
6. Separation of computation, visualization, and interpretation  
7. Extensible & testable modular components  

## Core Idea
Most analytics tools show numbers.  

This framework explains:  
- What those numbers mean
- How they impact investor experience
- Why they may have occurred
- How the stock behaves across multiple financial dimensions
- Each financial dimension is treated as an independent event pipeline, ensuring scalability and clean separation of concerns.

## Event Pipelines

Each pipeline includes:
- Mathematical computation
- Visual representation
- LLM interpretation

## Supported Event Metrics
| Category |	Metrics |  
|:---------|:--------:|  
| Growth	| Total Returns, CAGR |
| Risk	| Volatility, Downside Volatility, Max Drawdown |
| Risk-Adjusted	| Sharpe, Sortino, Calmar |
| Tail Risk	| Skewness, Kurtosis, VaR, CVaR |
| Stability	| Rolling Sharpe, Recovery Duration |
| Market Sensitivity | Alpha, Beta, R² (CAPM) |
| Drawdown Events	| Worst & Recent Drawdowns |
| Investment Simulation	| Portfolio Growth & P&L Extremes |  

## AI Integration
🔹 _Event-Level LLM Interpreter_  
- Converts quantitative outputs into structured explanations
- Describes investor experience (volatility, emotional stress)
- Adds contextual market reasoning
- Uses grounded prompts based only on computed data

🔹 _Global Research Chatbot_
- Answers stock-specific questions
- References structured event outputs
- Handles broader financial queries
- Avoids hallucination by grounding in pipeline results
- Powered locally via Ollama (phi3:mini).

## Architecture Overview
🔸 _Layered design:_
1. Main Orchestrator
2. Data Layer (Yahoo Finance ingestion)
3. Event Orchestrator
4. Engine Computation Layer
5. Visual Layer
6. LLM Interpreter
7. Context Builder
8. LLM Caller (Local model interface)

🔸 _Design Benefits:_
- Plug-and-play event modules
- Independent testing of metrics
- Reduced coupling
- Easy extensibility
- Clear abstraction boundaries

## Project Structure
```
engine/
pipeline/
visuals/
chat/
llm/
main.py
```
Each module is isolated to maintain separation of concerns and simplify testing.

 ## Tech Stack
- Python
- Pandas / NumPy
- Matplotlib
- yFinance
- Ollama (Local LLM Hosting)
- phi3:mini

## Running the Project
1. Install Dependencies
```
pip install -r requirements.txt
```
2. Start Ollama Server
```
ollama run phi3:mini
```
Ensure Ollama is running at:
```
http://localhost:11434
```
3. Run the System
```
python main.py
```
Input:  
- Ticker
- Start date
- End date

## Engineering Highlights
- CAPM regression modeling
- Rolling risk metrics
- Tail risk statistical modeling
- Event-driven modular architecture
- Structured prompt engineering
- Local LLM inference over HTTP (JSON-based API calls)
- Context-aware knowledge injection

## Why This Matters
This project bridges:  
- Quantitative finance  
- System architecture  
- AI reasoning  

It reflects real-world design thinking beyond isolated scripts — suitable for fintech, AI systems, backend engineering, and applied ML roles.


## Future Extensions
- Multi-stock comparative analysis
- Portfolio optimization module
- REST API deployment
- Cloud-based LLM deployment
- Real-time streaming data support

## Author
***Sanjeev R.K***
