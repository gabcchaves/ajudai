# AjudaAI - Assistente virtual para sistemas operacionais baseados em Unix.
import openai, argparse, os, subprocess


class OAPI():
    # Função que retorna nome da variável de ambiente que deve conter a chave
    # OpenAI.
    def get_env_var_api_key_name():
        return "OPENAI_API_KEY"


    # Procedimento para definir chave da API, se for válida.
    def set_api_key(key: str):
        if not OAPI.is_set_api_key():
            if OAPI.is_valid_api_key(key.CHAVE):
                os.putenv(OAPI.get_env_var_api_key_name(), key.CHAVE)
            else:
                print("Chave inválida.")
        else:
            if OAPI.is_valid_api_key(os.getenv(OAPI.get_env_var_api_key_name())):
                print("Uma sessão já está ativa.")
            else:
                print("Uma sessão inválida está ativa, e será desativada.")
                OAPI.unset_api_key()


    # Procedimento para desativar chave da API.
    def unset_api_key():
        if OAPI.is_set_api_key():
            os.unsetenv(OAPI.get_env_var_api_key_name())
            print("Desconectado.")
        else:
            print("Nenhuma sessão ativa.")


    # Função para verificar se uma chave está definida.
    def is_set_api_key():
        if OAPI.get_env_var_api_key_name() in os.environ.keys():
            return True
        else:
            return False


    # Função para verificar se uma chave é válida.
    def is_valid_api_key(key: str):
        try:
            openai.api_key = key
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello!"}
                ]
            )
            print(completion.choices[0].message)
            return true
        except Exception as e:
            print(e)
            return False


    # Função para construção da mensagem em linguagem natural a ser enviada ao
    # modelo de linguagem.
    def build_prompt(request: str, explain: bool = False):
        distro_name = subprocess.check_output(["lsb_release", "-d", "-s"])
        explain_text = ""
        format_text = "Comando: <inserir comando aqui>"

        if explain:
            explain_text = ("Também quero uma explicação detalhada sobre o"
                "código e como ele funciona")
            format_text += ("\nDescrição: <inserir descrição aqui>\nA descrição"
                            "deve ser escrita na mesma língua que a pergunta")
        
        prompt_list = [ 
            (f"Instruções: Escreva um comando CLI que faz o seguinte:"
            f"{request}. Tenha certeza de que esse comando está correto e"
            f"funciona no {distro_name}. {explain_text}"),
            (f"Formato: {format_text}"),
            (f"Caso a explicação não seja pedida de forma explícita mostre"
            f"apenas o comando e nenhuma explicação acerca do comando"),
            (f"Mostre o comando sem o caractere ` ou ´ ou '"),
            (f"Certifique de usar o formato acima de forma exata"),
        ]

        return "\n\n".join(prompt_list)


    def submit(request: str, explain: bool = False):
        prompt= OAPI.build_prompt(request, explain=explain)

        try:
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
        except Exception as e:
            if type(e) == openai.error.AuthenticationError:
                print("Nenhuma sessão ativa. Conecte-se usando o subcomando"
                    "'conectar")


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
    subparsers.choices["pergunta"].set_defaults(func=OAPI.submit)
    subparsers.choices["comando"].add_argument("COMANDO")
    subparsers.choices["comando"].set_defaults(func=OAPI.submit)

    return parser.parse_args()


if __name__ == "__main__":
    cli_args = parse_cli_args()
    if len(vars(cli_args)) > 1:
        cli_args.func(cli_args)
    elif len(vars(cli_args)) == 1:
        cli_args.func()
    else:
        print("HI")
