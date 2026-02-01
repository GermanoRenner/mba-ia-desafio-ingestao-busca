from search import search_prompt
from dotenv import load_dotenv

def main():
    while True:
        question = input("\nFaça sua pergunta: ")
        if question.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando chat...")
            break

        answer = search_prompt(question)
        if not answer:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return
        
        print("""PERGUNTA: {question} \n RESPOSTA: {answer.content}""".format(question=question, answer=answer))

if __name__ == "__main__":
    load_dotenv()
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrando chat...")
    except Exception as e:
        print(f"Erro ao iniciar o chat: {e}")