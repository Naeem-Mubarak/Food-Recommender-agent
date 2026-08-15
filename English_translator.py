from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from config import translator_llm_prompt
from voice_llm import voice_transcript_generator,path

data=voice_transcript_generator(path)

def english_translator(data):

    parser=StrOutputParser()
    model=ChatGoogleGenerativeAI(model='gemini-3.5-flash')
    chain = translator_llm_prompt | model | parser
    response = chain.invoke({
        'sentence': data
    })

    return response

re=english_translator(data)
print(re)