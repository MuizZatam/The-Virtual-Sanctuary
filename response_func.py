import ollama
import socket

def generate_text_with_llama(input_text: str) -> str:
    client = ollama.Client()

    try:
        # Attempt to generate text with the specified model
        response = client.generate(model="phi3:mini", prompt=input_text)
    except socket.error as e:
        raise RuntimeError(f"Connection error: {str(e)}. Please check if the Ollama service is running.")
    except Exception as e:
        # Check if the exception message indicates that the model was not found
        if "model not found" in str(e).lower():
            print("Model not found. Attempting to pull the model...")
            client.pull_model("phi3:mini")
            print("Model pulled successfully. Trying to generate text again...")
            response = client.generate(model="phi3:mini", prompt=input_text)
        else:
            raise RuntimeError(f"An error occurred while generating text: {str(e)}")

    # Extract the generated text from the 'response' key
    if "response" in response:
        generated_text = response["response"]
    else:
        raise ValueError("The 'response' key is missing in the API response.")

    return generated_text

if __name__ == "__main__":
    input_text = input(">: ")
    try:
        result = generate_text_with_llama(input_text)
        print(result)
    except Exception as e:
        print(f"Failed to generate text: {str(e)}")
