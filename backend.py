# AjudaAI - Assistente virtual para sistemas operacionais baseados em Unix.
import openai, argparse

# Função para avaliar argumentos passados ao programa e retornar resultados.
def parse_cli_args():
    parser = argparse.ArgumentParser(
        prog="AjudAI",
        description="Assistente virtual para sistemas operacionais."
    )

    parser.add_argument(
        "--connect",
        help="Autentica usuário a por meio da chave OpenAI passada como argumento."
    )
    parser.add_argument(
        "--disconnect",
        help="Desconecta usuário."
    )
    args = parser.parse_args()

    if args.connect:
        print("Connection.")
    elif args.disconnect:
        print("Disconnect.")

    return args


# Controlador responsável por articular as respostas da API com o sistema
# operacional.

# 'Language Model' - Classe que outorga a interação com a OpenAI API.
class LM:
    def __init__(self, os_name: str, shell_name: str, user: str, api_key: str):
        self.os_name = os_name
        self.shell_name = shell_name
        self.user = user
        openai.api_key = api_key


    # 'explain' é um parâmetro opcional para determinar se uma explicação será
    # fornecida ao usuário.
    def build_prompt(self, request: str, os_name: str, shell_name: str,
                     explain: bool = False):
        explain_text = ""
        format_text = "Comando: <inserir comando aqui>"

        if explain:
            # Obriga ao chat à escrever uma descrição sobre o comando e atribui
            # um formato para essa descrição
            explain_text = ("Também quero uma explicação detalhada sobre o"
                "código e como ele funciona")
            format_text += ("\nDescrição: <inserir descrição aqui>\nA descrição"
                            "deve ser escrita na mesma língua que a pergunta")
        
        # Lista que contém todas as informações que criam o prompt ideal
        prompt_list = [ 
            f"Instruções: Escreva um comando CLI que faz o seguinte: {request}. Tenha certeza de que esse comando está correto e funiona no {os_name} usando o {shell_name}. {explain_text}",
            f"Formato: {format_text}",
            f"Caso a explicação não seja pedida de forma explícita mostre apenas o comando e nenhuma explicação acerca do comando",
            f"Mostre o comando sem o caractere ` ou ´ ou '",
            f"Certifique de usar o formato acima de forma exata",
        ]

        # Retorna uma string contendo as informações do prompt_list separadas por \n\n
        return "\n\n".join(prompt_list)


    def ask(self, request: str, explain: bool = False):
        prompt= self.build_prompt(request, self.os_name, self.shell_name, explain=explain)

        reponse = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "Você é uma aplicação CLI que gera comandos de terminal"},
                {"role": "user", "content": prompt}
            ],
            max_tokens = 300 if explain else 180,
            temperature = 0
        )

        return reponse["choices"][0]["message"]["content"]


if __name__ == "__main__":
    cli_args = parse_cli_args()

    #user = ajudaAi("Linux", "Bash", "Pedro", "api-key")

    #print(user.ask("Como baixar e instalar o vscode pelo terminal usando o gerenciador de pacotes flatpak", explain=False))
