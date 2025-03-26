from system_prompts import *
import models
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
from tavily_search import tavily_search


init()  # Initialize colorama for Windows compatibility
# Load API keys from .env or api.key file
load_dotenv("api.key")
# Retrieve API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
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
    llama=models.LlamaChat(api_key=GROQ_API_KEY,system_prompt=LLAMA_SYSTEM_PROMPT)
    deepseek=models.DeepseekChat(api_key=GROQ_API_KEY,system_prompt=DEEPSEEK_SYSTEM_PROMPT)
    deepseek_response,llama_response="", response["claims"][0]
    claim=response["claims"][0]
    for i in range(3):
        deepseek_response=deepseek.send_message(llama_response)
        deepseek_response=f"Claim is :{claim}"+f"Response from your opponent is :{deepseek_response}"
        llama_response=llama.send_message(deepseek_response)
        llama_response=f"Claim is :{claim}"+f"Response from your opponent is :{llama_response}"


def colored_fight(response):
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
        if str(deepseek_response) == "None":
            deepseek_response="I dont know what to reply,my token limits have exceeded"
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
        sources={}
        if gemini_response["questions"]:
            for question in gemini_response["questions"]:
                tavily_response=tavily_search(query=question,max_results=1,TAVILY_API_KEY=TAVILY_API_KEY)
                sources[question]=tavily_response
        if sources:
            sources_text = "\n\n".join([f"- {question}: {sources[question]}" for question in sources])
            source_context = f"\n\n🔍 **Fact-Checked Sources:**\n{sources_text}"
            deepseek_response += source_context
            llama_response += source_context

        i+=1


colored_fight(extract_claims("Does caffeine improve memory?"))
