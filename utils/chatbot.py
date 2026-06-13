import requests
from huggingface_hub import InferenceClient

def get_chat_response(prompt, api_key):
    """
    Calls Hugging Face Inference API for the music assistant chat.
    Uses a standard instruct model like Mistral or Zephyr.
    """
    if not api_key:
        return "Please provide a Hugging Face API Key in the sidebar to use the assistant."
        
    # Example model: Mistral-7B-Instruct
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    
    try:
        client = InferenceClient(model=model_id, token=api_key)
        
        system_prompt = (
            "You are an expert AI Music Producer and Remix Assistant. "
            "Help the user with music production tips, instrument choices, and remix ideas. "
            "Keep answers concise, professional, and practical."
        )
        
        formatted_prompt = f"<s>[INST] {system_prompt} \n\nUser: {prompt} [/INST]"
        
        response = client.text_generation(
            formatted_prompt, 
            max_new_tokens=250,
            temperature=0.7,
            return_full_text=False
        )
        return response.strip()
    except Exception as e:
        return f"Error connecting to AI Assistant: {str(e)}"
