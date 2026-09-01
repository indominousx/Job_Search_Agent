from typing import TypedDict, List, Dict, Any

class WorkflowState(TypedDict):
    """
    Represents the state of the job application orchestration graph.
    """
    user_id: str
    candidate_profile: Dict[str, Any]
    
    # Discovery Phase
    discovered_jobs: List[Dict[str, Any]]
    
    # Normalization Phase
    normalized_jobs: List[Dict[str, Any]]
    
    # Matching Phase
    matched_jobs: List[Dict[str, Any]]
    
    # Preparation Phase
    prepared_applications: List[Dict[str, Any]]
