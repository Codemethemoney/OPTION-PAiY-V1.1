from fastapi import Header, HTTPException, Depends
from typing import Optional
from app.agents.financial_agent import FinancialAgent
from app.agents.rag_agent import RAGAgent
from app.agents.langchain_agent import LangChainAgent
from app.agents.pydantic_agent import PydanticAgent
from app.agents.manager_agent import ManagerAgent

async def get_token_header(x_token: Optional[str] = Header(None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

def get_financial_agent():
    return FinancialAgent()

def get_rag_agent():
    return RAGAgent()

def get_langchain_agent():
    return LangChainAgent()

def get_pydantic_agent():
    return PydanticAgent()

def get_manager_agent(
    financial_agent: FinancialAgent = Depends(get_financial_agent),
    rag_agent: RAGAgent = Depends(get_rag_agent),
    langchain_agent: LangChainAgent = Depends(get_langchain_agent),
    pydantic_agent: PydanticAgent = Depends(get_pydantic_agent)
):
    return ManagerAgent(financial_agent, rag_agent, langchain_agent, pydantic_agent)

def get_agents(
    manager_agent: ManagerAgent = Depends(get_manager_agent)
):
    return {
        "manager_agent": manager_agent,
        "financial_agent": manager_agent.financial_agent,
        "rag_agent": manager_agent.rag_agent,
        "langchain_agent": manager_agent.langchain_agent,
        "pydantic_agent": manager_agent.pydantic_agent
    }
