import ollama

def generate_text_with_llama(input_text: str) -> str:
    client = ollama.Client()

    # Making the API call
    response = client.generate(model="llama3.1:8b", prompt=input_text)

    # Extract the generated text from the 'response' key
    if "response" in response:
        generated_text = response["response"]
    else:
        raise ValueError("The 'response' key is missing in the API response.")

    return generated_text

if __name__ == "__main__":
    input_text = input(">:")
    result = generate_text_with_llama(input_text)
    print(result)
