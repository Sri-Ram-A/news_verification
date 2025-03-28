from system_prompts import *
import models
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
from pprint import pprint
init()  # Initialize colorama for Windows compatibility
# Load API keys from .env or api.key file
load_dotenv("api.key")
# Retrieve API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GROQ_API_KEY or not GEMINI_API_KEY :
    raise ValueError(f"Missing API Keys:")
print("All API keys are loaded successfully!")

def extract_claims(message:str)->dict:
    """
    INPUT
        message:str
    OUTPUT
        response :dict
            'claims':list[str] 
    '       questions':list[str]
    """
    print(f"{Fore.LIGHTGREEN_EX}THE MESSAGE ENTERED BY USER IS")
    print(message)
    chat_session = models.GeminiChat(api_key=GEMINI_API_KEY,system_prompt=GEMINI_EXTRACTOR_SYSTEM_PROMPT)
    response = chat_session.send_message(message)
    Style.RESET_ALL
    print(f"{Fore.MAGENTA}RESPONSE FROM CLAIM EXTRACTOR-GEMINI IS")
    print(response)
    Style.RESET_ALL
    return response


def fight(response):
    """
    INPUT
        response :dict
            'claims':list[str] 
    '       questions':list[str]
    """
    llama = models.LlamaChat(api_key=GROQ_API_KEY, system_prompt=LLAMA_SYSTEM_PROMPT)
    deepseek = models.DeepseekChat(api_key=GROQ_API_KEY, system_prompt=DEEPSEEK_SYSTEM_PROMPT)
    gemini=models.GeminiIntermediate(api_key=GEMINI_API_KEY,system_prompt=GEMINI_INTERMEDIATE_SYSTEM_PROMPT)  
    deepseek_response, llama_response = "", response[0]["claims"][0]
    claim = response[0]["claims"][0]
    status,i = 1,1
    while status:
        # DeepSeek's turn (blue)
        _,deepseek_response = deepseek.send_message(llama_response)
        print(f"\n{Fore.BLUE}=== DEEPSEEK (Round {i}) ===")
        print(f"Response:{Style.RESET_ALL} {deepseek_response}")
        deepseek_response=f"Claim is :{claim}"+f"Response from your opponent is :{deepseek_response}"
        
        # Llama's turn (red)
        llama_response = llama.send_message(deepseek_response)
        print(f"\n{Fore.RED}=== LLAMA (Round {i}) ===")
        print(f"Response:{Style.RESET_ALL} {llama_response}")
        llama_response=f"Claim is :{claim}"+f"Response from your opponent is :{llama_response}"

        #Gemini arbitrator (green)
        gemini_response=gemini.send_message(claim=claim,llama_response=llama_response,deepseek_response=deepseek_response)
        print(f"\n{Fore.GREEN}=== GEMINI  (Round {i}) ===")
        print(f"Response:{Style.RESET_ALL} {gemini_response}")
        status=gemini_response["status"]
        i+=1


fight(extract_claims("The Babri Masjid was built after forcibly demolishing a pre-existing Ram Temple in Ayodhya."))
