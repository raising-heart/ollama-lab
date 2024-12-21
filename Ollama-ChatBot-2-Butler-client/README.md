# AI Butler System (Ollama Version)

An intelligent AI Butler system powered by local LLM through Ollama, designed to provide professional and structured assistance across various tasks and inquiries.

## Prerequisites

1. Python 3.8 or higher
2. Ollama installed and running locally (default port: 11434)
3. llama3.2 model downloaded in Ollama
4. Network access to Ollama host (if not running locally)

## Installation

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The system can be configured through `config.py`:
- `OLLAMA_MODEL`: Specify the Ollama model to use (default: "llama3.2:3b")
- `OLLAMA_HOST`: Configure the Ollama host URL (default: "http://localhost:11434")
- `OLLAMA_HEADERS`: Custom headers for API requests
- `MAX_RETRIES`: Number of retry attempts for failed API calls

## Usage

1. Make sure Ollama is running and the llama3.2 model is available
2. Run the main script:
   ```bash
   python main.py
   ```
3. Start interacting with your AI Butler! Type 'exit' to end the conversation

## Features

- Professional and structured responses using clear icons:
  - 🎯 Analysis: Assessment of the situation or query
  - 🔧 Process: Approach or steps to address the request
  - 🗣️ Response: Formal response to the user
- Advanced conversation memory (last 50 messages)
- Emotional tone analysis of user input
- Session logging with timestamped files
- Automatic retry mechanism for failed API calls

## Project Structure

- `main.py`: Main application entry point
- `agents.py`: Implementation of AI agents (ToneAnalyzer and AIButler)
- `tasks.py`: Core task management and processing
- `traits.py`: AI Butler's personality and responsibility definitions
- `config.py`: Configuration settings

## Session Management

The system automatically creates session files for each conversation, stored in the `sessions/` directory. These files contain the complete interaction history with timestamps.

## Note

This implementation uses client-side access to LLM models via the standard Ollama URL, ensuring professional-grade assistance capabilities while maintaining flexibility and ease of deployment. While the majority of responses adhere to the structured format and Butler persona, occasional inconsistencies may arise where the model deviates from the expected format or tone. This is a known limitation when interfacing with remote LLMs, and ongoing updates aim to enhance response consistency and reliability.
