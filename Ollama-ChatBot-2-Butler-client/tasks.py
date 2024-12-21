from typing import List, Dict
from agents import ToneAnalyzer, AIButler
from logging import getLogger
from functools import lru_cache

logger = getLogger(__name__)

def analyze_input_task(text: str, conversation_history: List[Dict[str, str]]) -> str:
    """
    Analyze input text and generate a butler response.
    
    Args:
        text: The input text to analyze
        conversation_history: List of previous conversation messages
        
    Returns:
        str: Formatted string containing analysis and response
        
    Raises:
        ValueError: If input text is empty or invalid
        RuntimeError: If API calls fail
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string")
        
    try:
        # Use ToneAnalyzer to analyze the tone/type of the input
        analyzer = ToneAnalyzer()
        analysis = analyzer.analyze_input(text)
        
        # Generate butler response with conversation history
        butler = AIButler()
        response = butler.generate_response(text, analysis, conversation_history)
        
        return f"""Input Analysis: {analysis}
        
Butler's Response:\n{response}"""
        
    except Exception as e:
        logger.error(f"Error in analyze_input_task: {str(e)}")
        raise RuntimeError(f"Failed to process input: {str(e)}")
