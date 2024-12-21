from tasks import analyze_input_task
from datetime import datetime
import os

def create_session_file():
    # Create sessions directory if it doesn't exist
    if not os.path.exists('sessions'):
        os.makedirs('sessions')
        print(f"Created sessions directory at: {os.path.abspath('sessions')}")
    
    # Generate filename with current date and time
    current_time = datetime.now()
    filename = f"sessions/session[{current_time.strftime('%d%b%y')}][{current_time.strftime('%H:%M')}].md"
    
    print(f"Creating session file at: {os.path.abspath(filename)}")
    
    # Create and return the file object
    return open(filename, 'w')

def main():
    # Initialize conversation memory
    conversation_history = []
    
    # Open session file
    session_file = create_session_file()
    print("Session file created successfully")
    
    # Write header to session file
    session_file.write("# Conversation Session with AI Butler\n\n")
    
    try:
        while True:
            user_input = input("User: ").strip()
            
            if user_input.lower() == "exit":
                print("Thank you for using AI Butler. Have a great day!")
                # Log exit in session file
                session_file.write("\n---\nSession ended.\n")
                break
            else:
                # Add user input to conversation history
                conversation_history.append({"role": "user", "content": user_input})
                
                # Pass both current input and history to analysis task
                result = analyze_input_task(user_input, conversation_history)
                print("\nButler:", result)
                
                # Extract butler's response and add to history
                response_start = result.find("Butler's Response:")
                if response_start != -1:
                    butler_response = result[response_start + len("Butler's Response:"):].strip()
                    conversation_history.append({"role": "assistant", "content": butler_response})
                
                # Log interaction in session file
                session_file.write(f"## User\n")
                session_file.write(f"```\n{user_input}\n```\n\n")
                session_file.write(f"## Butler\n")
                session_file.write(f"{result}\n\n")
                # Ensure the file is written immediately
                session_file.flush()
    
    finally:
        # Make sure to close the file
        session_file.close()
        print("Session file closed")

if __name__ == "__main__":
    main()
