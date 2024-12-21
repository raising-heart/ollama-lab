from typing import List, Dict, Optional
from ollama import Client
from config import OLLAMA_MODEL, MAX_RETRIES, OLLAMA_HOST, OLLAMA_HEADERS
import time
from functools import lru_cache
from abc import ABC, abstractmethod
from logging import getLogger
from traits import AI_BUTLER_INSTRUCTIONS

logger = getLogger(__name__)

# Maximum number of messages to keep in conversation history
MAX_HISTORY_MESSAGES = 50

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self):
        self.retry_count = 0
        self.client = Client(
            host=OLLAMA_HOST,
            headers=OLLAMA_HEADERS
        )
        
    def _make_api_call(self, messages: List[Dict[str, str]], retry_count: int = 0) -> str:
        """
        Make an API call with retry logic
        
        Args:
            messages: List of message dictionaries
            retry_count: Current retry attempt
            
        Returns:
            str: API response content
            
        Raises:
            RuntimeError: If max retries exceeded
        """
        try:
            response = self.client.chat(
                model=OLLAMA_MODEL,
                messages=messages
            )
            return response.message.content
            
        except Exception as e:
            if retry_count < MAX_RETRIES:
                logger.warning(f"API call failed, retrying... ({retry_count + 1}/{MAX_RETRIES})")
                time.sleep(2 ** retry_count)  # Exponential backoff
                return self._make_api_call(messages, retry_count + 1)
            else:
                logger.error(f"Max retries exceeded: {str(e)}")
                raise RuntimeError(f"API call failed after {MAX_RETRIES} retries")

    @abstractmethod
    def process(self, *args, **kwargs):
        """Abstract method to be implemented by child classes"""
        pass

class ToneAnalyzer(BaseAgent):
    def process(self, text: str) -> str:
        """Implementation of abstract method"""
        return self.analyze_input(text)

    @lru_cache(maxsize=100)
    def analyze_input(self, text: str) -> str:
        """
        Analyze the tone of input text
        
        Args:
            text: Input text to analyze
            
        Returns:
            str: Tone analysis result
        """
        if not text:
            raise ValueError("Input text cannot be empty")
            
        messages = [
            {
                "role": "system", 
                "content": """
                    You are an advanced sentiment and tone analyzer. Analyze the following aspects:
                    1. Basic Emotions (joy, sadness, anger, fear, surprise, disgust)
                    2. Complex Emotions (love, jealousy, guilt, pride, nostalgia, hope, confusion)
                    3. Social Tones (casual, formal, humorous, sarcastic, sympathetic, aggressive, supportive)
                    Provide a concise analysis focusing on the most prominent aspects.
                """
            },
            {
                "role": "user",
                "content": text
            }
        ]
        
        return self._make_api_call(messages)

class AIButler(BaseAgent):
    def process(self, user_input: str, tone_analysis: str, conversation_history: List[Dict[str, str]]) -> str:
        """Implementation of abstract method"""
        return self.generate_response(user_input, tone_analysis, conversation_history)

    def generate_response(self, user_input: str, tone_analysis: str, 
                         conversation_history: List[Dict[str, str]]) -> str:
        """
        Generate a response as an AI Butler
        
        Args:
            user_input: User's input text
            tone_analysis: Result of tone analysis
            conversation_history: Previous conversation messages
            
        Returns:
            str: Generated response
        """
        # Prepare the conversation context
        messages = [
            {
                "role": "system",
                "content": "You are an AI Butler. You must ALWAYS respond as a professional butler would - formal, courteous, and proper. Never break character.\n\n" + AI_BUTLER_INSTRUCTIONS + """
                Remember to always structure your response using these exact icons:
                🎯 Analysis: Your assessment of the situation or query
                🔧 Process: Your approach or steps to address the request
                🗣️ Response: Your formal response to the user, always maintaining a butler's tone
                """
            }
        ]
        
        # Add conversation history, keeping the last MAX_HISTORY_MESSAGES messages
        messages.extend(conversation_history[-MAX_HISTORY_MESSAGES:])
        
        # Add current context
        messages.extend([
            {
                "role": "user",
                "content": f"[Tone Analysis: {tone_analysis}]\n\nUser's message: {user_input}"
            }
        ])
        
        return self._make_api_call(messages)
