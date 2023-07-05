# AjudaAI - Assistente virtual para sistemas operacionais baseados em Unix.
import openai, argparse, os


class OAPI():
    _ENV_API_KEY_NAME = "OPENAI_API_KEY"


    # Procedimento para definir chave da API, se for válida.
    def set_api_key(key: str):
        if not OAPI.is_set_api_key():
            if OAPI.is_valid_api_key(key):
                os.putenv(self._ENV_API_KEY_NAME, key)
            else:
                print("Chave inválida.")
        else:
            if OAPI.is_valid_api_key(os.getenv(self._ENV_API_KEY_NAME)):
                print("Uma sessão já está ativa.")
            else:
                print("Uma sessão inválida está ativa, e será desativada.")
                OAPI.unset_api_key()


    # Procedimento para desativar chave da API.
    def unset_api_key(anything):
        if OAPI.is_set_api_key():
            os.unsetenv(_ENV_API_KEY_NAME)
            print("Desconectado.")
        else:
            print("Nenhuma sessão ativa.")


    # Função para verificar se uma chave está definida.
    def is_set_api_key():
        if OAPI._ENV_API_KEY_NAME in os.environ.keys():
            return True
        else:
            return False


    # Função para verificar se uma chave é válida.
    def is_valid_api_key(key: str):
        try:
            openai.api_key = os.getenv(self._ENV_API_KEY_NAME)
            openai.Completion.create(
                model="gpt-3.5-turbo",
                prompt="Say this is a test",
                max_tokens=7,
                temperature=0
            )
        except Exception as e:
            if type(e) == openai.error.AuthenticationError:
                return False
        else:
            return True


    def submit(self, request: str, explain: bool = False):
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
    subparsers.choices["conectar"].set_defaults(func=OAPI.set_api_key)
    subparsers.choices["desconectar"].set_defaults(func=OAPI.unset_api_key)
    subparsers.choices["pergunta"].add_argument("PERGUNTA")
    #subparsers.choices["pergunta"].set_defaults()
    subparsers.choices["comando"].add_argument("COMANDO")
    ##subparsers.choices["comando"].set_defaults()

    return parser.parse_args()


## Classe que outorga a interação com a OpenAI API.
#class OAPI:
#    def __init__(self, distro_name: str, user: str, api_key: str):
#        self.distro_name = distro_name
#        self.user = user
#        openai.api_key = api_key
#
#
#    # 'explain' é um parâmetro opcional para determinar se uma explicação será
#    # fornecida ao usuário.
#    def build_prompt(self, distro_name, request: str, explain: bool = False):
#        explain_text = ""
#        format_text = "Comando: <inserir comando aqui>"
#
#        if explain:
#            explain_text = ("Também quero uma explicação detalhada sobre o"
#                "código e como ele funciona")
#            format_text += ("\nDescrição: <inserir descrição aqui>\nA descrição"
#                            "deve ser escrita na mesma língua que a pergunta")
#        
#        # Lista que contém todas as informações que criam o prompt ideal
#        #prompt_list = [ 
#        #    (f"Instruções: Escreva um comando CLI que faz o seguinte: {request}.
#        #               Tenha certeza de que esse comando está correto e funciona
#        #               no {distro_name}. {explain_text}"),
#        #    (f"Formato: {format_text}"),
#        #    (f"Caso a explicação não seja pedida de forma explícita mostre apenas
#        #               o comando e nenhuma explicação acerca do comando"),
#        #    (f"Mostre o comando sem o caractere ` ou ´ ou '"),
#        #    (f"Certifique de usar o formato acima de forma exata"),
#        #]
#
#        # Retorna uma string contendo as informações do prompt_list separadas por \n\n
#        return "\n\n".join(prompt_list)


if __name__ == "__main__":
    cli_args = parse_cli_args()
    cli_args.func(cli_args)

    #user = ajudaAi("Linux", "Bash", "Pedro", "api-key")

    #print(user.ask("Como baixar e instalar o vscode pelo terminal usando o gerenciador de pacotes flatpak", explain=False))
