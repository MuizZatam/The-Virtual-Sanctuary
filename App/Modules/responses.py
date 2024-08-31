from llama_cpp import Llama

llm = Llama.from_pretrained(

    repo_id = "microsoft/Phi-3-mini-4k-instruct-gguf",
    filename = "Phi-3-mini-4k-instruct-q4.gguf",
    verbose = False
)

def narrate(species: str) -> str:

    output = llm(

        f"You are David Attenborough, providing a documentary-style narration about the list of following species - {species}, explain the species' role and importance within its native ecosystem. Use the common name for the specified species in narration even if the given species is in scientific name. Offer details on the population status, including any relevant conservation data. Describe intriguing or amusing aspect of the species' life. Note any unique significance the species might have, whether to the ecosystem, culture, or human history. With all that being said, do not provide any ambiguous information. Do not provide any additional context such as background tone or what your name or role is or any clarifications. Stick to the request only. Use only one paragraph with no linebreaks",
        max_tokens=1000
    )
    
    output_text = output.get('choices')[0].get("text")

    last_period_index = output_text.rfind(".")
    
    if last_period_index != -1:

        output_text = output_text[:last_period_index + 1]  
        
    else:

        output_text = output_text  

    return output_text
