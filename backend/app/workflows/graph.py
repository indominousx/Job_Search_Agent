from langgraph.graph import StateGraph, END
from app.workflows.state import WorkflowState
from app.workflows.nodes import (
    discover_jobs_node,
    normalize_jobs_node,
    match_jobs_node,
    prepare_application_node
)

def build_job_workflow_graph() -> StateGraph:
    """
    Assembles the state graph for the job application workflow.
    """
    workflow = StateGraph(WorkflowState)

    # Add Nodes
    workflow.add_node("discover_jobs", discover_jobs_node)
    workflow.add_node("normalize_jobs", normalize_jobs_node)
    workflow.add_node("match_jobs", match_jobs_node)
    workflow.add_node("prepare_application", prepare_application_node)

    # Define standard flow edges with conditional routing
    workflow.set_entry_point("discover_jobs")
    
    def check_discovered(state: WorkflowState) -> str:
        return "normalize_jobs" if state.get("discovered_jobs") else END
        
    def check_matched(state: WorkflowState) -> str:
        return "prepare_application" if state.get("matched_jobs") else END

    workflow.add_conditional_edges("discover_jobs", check_discovered)
    workflow.add_edge("normalize_jobs", "match_jobs")
    workflow.add_conditional_edges("match_jobs", check_matched)
    workflow.add_edge("prepare_application", END)

    # Note: Conditional edges to short-circuit the graph if no jobs are discovered 
    # will be added in Phase 5 when the logic is fully implemented.

    return workflow

def get_compiled_graph(checkpointer=None):
    """
    Compiles the graph, optionally attaching a LangGraph checkpointer for state persistence.
    Example usage:
        from langgraph.checkpoint.postgres import PostgresSaver
        from psycopg_pool import ConnectionPool
        
        with ConnectionPool(settings.DATABASE_URL) as pool:
            checkpointer = PostgresSaver(pool)
            checkpointer.setup()
            graph = get_compiled_graph(checkpointer)
    """
    workflow = build_job_workflow_graph()
    return workflow.compile(checkpointer=checkpointer)
