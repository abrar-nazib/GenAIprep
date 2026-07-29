"""Parallel workflow with reducers"""

from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
import operator

from pathlib import Path
from dotenv import load_dotenv

cwd = Path(__file__).parent
load_dotenv(cwd/".env")

llm = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    openrouter_provider={
        "order":["baidu", "streamlake"], 
        "allow_fallbacks": True
        }
    ,
    temperature=0
)


class EvaluationSchema(BaseModel):
    feedback: str = Field(description="Detailed feedback for the essay")
    score: float = Field(description="Score out of 10", ge=0, le=10)
    
structured_model = llm.with_structured_output(EvaluationSchema)

paragraph = """
Failure is an unavoidable part of learning and personal growth. However, failure becomes valuable only when a person reflects on it and identifies what went wrong. By analyzing mistakes, one can improve strategies, develop better judgment, and avoid repeating the same errors. In contrast, ignoring the lessons of failure creates a cycle in which the same problems return. Successful people are not those who never fail, but those who use failure as feedback. Therefore, learning from failure is essential for progress. Without reflection, correction, and adaptation, failure remains meaningless, and repeated failure becomes almost inevitable in both life and work.
"""


class EssayState(TypedDict):
    
    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: Annotated[list[int], operator.add]
    # The reducer function is the add. Instead of replace, add operation will happen.
    avg_score: float
    
def evaluate_language(state: EssayState):
    essay = state["essay"]
    prompt = f"Evaluate the language quality of the following essay and provide a feedback and assign a score out of 10\n{essay}"
    output:EvaluationSchema = structured_model.invoke(prompt)
    return {"language_feedback": output.feedback, "individual_scores": [output.score]}
    
def evaluate_analysis(state: EssayState):
    essay = state["essay"]
    prompt = f"Evaluate the analysis quality of the following essay and provide a feedback and assign a score out of 10\n{essay}"
    output:EvaluationSchema = structured_model.invoke(prompt)
    return {"analysis_feedback": output.feedback, "individual_scores": [output.score]}
    

def evaluate_thought(state: EssayState):
    essay = state["essay"]
    prompt = f"Evaluate the clarity of thought quality of the following essay and provide a feedback and assign a score out of 10\n{essay}"
    output:EvaluationSchema = structured_model.invoke(prompt)
    return {"clarity_feedback": output.feedback, "individual_scores": [output.score]}
    
def final_evaluation(state: EssayState):
    # Summary feedback
    prompt = f"Based on the following feedbacks, create a summarized feedback\n language feedback:\n{state['language_feedback']} \n analysis feedback:\n{state['analysis_feedback']}\n clarity of thought feedback:\n{state['clarity_feedback']}"
    
    overall_feedback = llm.invoke(prompt).content
    
    avg_score = sum(state["individual_scores"])/len(state["individual_scores"])
    
    return {"overall_feedback": overall_feedback, "avg_score": avg_score}

# Create edges
graph = StateGraph(EssayState)
graph.add_node("evaluate_language", evaluate_language)
graph.add_node("evaluate_analysis", evaluate_analysis)
graph.add_node("evaluate_thought", evaluate_thought)
graph.add_node("final_evaluation", final_evaluation)


graph.add_edge(START, "evaluate_language")
graph.add_edge(START, "evaluate_analysis")
graph.add_edge(START, "evaluate_thought")
graph.add_edge("evaluate_language", "final_evaluation")
graph.add_edge("evaluate_analysis", "final_evaluation")
graph.add_edge("evaluate_thought", "final_evaluation")
graph.add_edge("final_evaluation", END)

workflow = graph.compile()

png_bytes = workflow.get_graph().draw_mermaid_png()
with open(cwd/"graph.png", "wb") as f:
	f.write(png_bytes)
 
initial_state:EssayState = {
    "essay" : paragraph
}

result = workflow.invoke(initial_state)

print(result)