from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "Ihre Aufgabe besteht darin, bestimmte Informationen aus dem folgenden Textinhalt zu extrahieren: {dom_content}. "
    "Bitte befolgen Sie diese Anweisungen sorgfältig: \n\n"
    "1. **Informationen extrahieren:** Extrahieren Sie nur die Informationen, die direkt mit der bereitgestellten Beschreibung übereinstimmen: {parse_description}. "
    "2. **Kein zusätzlicher Inhalt:** Fügen Sie Ihrer Antwort keinen zusätzlichen Text, keine Kommentare oder Erklärungen hinzu. "
    "3. **Leere Antwort:** Wenn keine Informationen mit der Beschreibung übereinstimmen, geben Sie eine leere Zeichenfolge ('') zurück."
    "4. **Nur direkte Daten:** Ihre Ausgabe sollte nur die Daten enthalten, die explizit angefordert wurden, und keinen anderen Text."
)
model = OllamaLLM(model="llama3.2")


def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []
    for idx, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {idx} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
