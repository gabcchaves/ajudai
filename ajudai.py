# AjudaAI - Assistente virtual para sistemas operacionais baseados em Unix.
import openai, argparse, os

# :/
ENV_KEY_NAME = "OPENAI_API_KEY"

# Função para avaliar argumentos passados ao programa e retornar resultados.
def parse_cli_args():
    parser = argparse.ArgumentParser(
        prog="AjudAI",
        description="Assistente virtual para sistemas operacionais."
    )

    subparsers = parser.add_subparsers(
        title="Sub-comandos",
        description="Comandos válidos.",
        help="Informações adicionais."
    )

    subparsers.add_parser("conectar")
    subparsers.add_parser("desconectar")
    subparsers.add_parser("pergunta", aliases=["p"])
    subparsers.add_parser("comando", aliases=["c"])

    subparsers.choices["conectar"].add_argument("CHAVE")
    subparsers.choices["conectar"].set_defaults(func=login)
    subparsers.choices["desconectar"].set_defaults(func=logout)
    subparsers.choices["pergunta"].add_argument("PERGUNTA")
    #subparsers.choices["pergunta"].set_defaults()
    subparsers.choices["comando"].add_argument("COMANDO")
    ##subparsers.choices["comando"].set_defaults()

    return parser.parse_args()


# Controlador responsável por articular as respostas da API com o sistema
# operacional.
class Controller:
    def login():
        print("Hello")

# Classe que outorga a interação com a OpenAI API.
class OAPI:
    def __init__(self, distro_name: str, user: str, api_key: str):
        self.distro_name = distro_name
        self.user = user
        openai.api_key = api_key


    # 'explain' é um parâmetro opcional para determinar se uma explicação será
    # fornecida ao usuário.
    def build_prompt(self, distro_name, request: str, explain: bool = False):
        explain_text = ""
        format_text = "Comando: <inserir comando aqui>"

        if explain:
            explain_text = ("Também quero uma explicação detalhada sobre o"
                "código e como ele funciona")
            format_text += ("\nDescrição: <inserir descrição aqui>\nA descrição"
                            "deve ser escrita na mesma língua que a pergunta")
        
        # Lista que contém todas as informações que criam o prompt ideal
        #prompt_list = [ 
        #    (f"Instruções: Escreva um comando CLI que faz o seguinte: {request}.
        #               Tenha certeza de que esse comando está correto e funciona
        #               no {distro_name}. {explain_text}"),
        #    (f"Formato: {format_text}"),
        #    (f"Caso a explicação não seja pedida de forma explícita mostre apenas
        #               o comando e nenhuma explicação acerca do comando"),
        #    (f"Mostre o comando sem o caractere ` ou ´ ou '"),
        #    (f"Certifique de usar o formato acima de forma exata"),
        #]

        # Retorna uma string contendo as informações do prompt_list separadas por \n\n
        return "\n\n".join(prompt_list)


    def ask(self, request: str, explain: bool = False):
        prompt= self.build_prompt(request, self.os_name, self.shell_name, explain=explain)

        openai.api_key = "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"

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

    
def login(key: str):
    if "OPENAI_API_KEY" in os.environ.keys():
        print("Você tem uma sessão ativa.\nPara desativá-la, use o sub-comando"
              "'desconectar'.")
    else:
        # Teste de validade da chave.
        try:
            openai.api_key = key
            openai.Completion.create(
                model="gpt-3.5-turbo",
                prompt="Say this is a test",
                max_tokens=7,
                temperature=0
            )
        except Exception as e:
            if type(e) == openai.error.AuthenticationError:
                print("Chave inválida.")
        else:
            os.putenv("OPENAI_API_KEY", key)
            print("Conexão exitosa.")


def logout(anything):
    if ENV_KEY_NAME in os.environ.keys():
        os.unsetenv(ENV_KEY_NAME)
        print("Desconectado")
    else:
        print("Nenhuma sessão ativa.")


if __name__ == "__main__":
    cli_args = parse_cli_args()
    cli_args.func(cli_args)

    #user = ajudaAi("Linux", "Bash", "Pedro", "api-key")

    #print(user.ask("Como baixar e instalar o vscode pelo terminal usando o gerenciador de pacotes flatpak", explain=False))
