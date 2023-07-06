# AjudaAI - Assistente virtual para sistemas operacionais baseados em Unix.
import openai, argparse, os, subprocess, sqlite3


# Classe estática para interação com o banco de dados.
class DB:
    # Função para retornar o nome do banco de dados.
    def get_db_name():
        return "ajudai.db"


    # Procedimento para criar estrutura básica do banco de dados.
    def setup():
        con = sqlite3.connect(DB.get_db_name())

        try:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Chat(
                    Id INTEGER,
                    Title TEXT NOT NULL,
                    PRIMARY KEY (Id)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Interchange(
                    Id INTEGER,
                    IdChat INTEGER,
                    RequestContent TEXT NOT NULL,
                    ResponseContent TEXT NOT NULL,
                    PRIMARY KEY (Id),
                    FOREIGN KEY (IdChat) REFERENCES Chat(Id)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Key(
                    Id INTEGER PRIMARY KEY,
                    Key TEXT NOT NULL
                );
            """)
            cur.close()
        except sqlite3.Error as e:
            print(e)

        con.commit()
        con.close()


    # Procedimento para criar uma conversa.
    def create_chat(title: str):
        con = sqlite3.connect(DB.get_db_name())

        try:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO Chat (Title) VALUES ('{title}');
            """.format(title=title))
            cur.close()
        except sqlite3.Error as e:
            print("Não foi possível criar nova conversa.")
            print(e)

        con.commit()
        con.close()


    # Procedimento para gravar uma mensagem.
    def record_interchange(reqc: str, resc: str, chat_id: int):
        con = sqlite3.connect(DB.get_db_name())

        try:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO Interchange(RequestContent, ResponseContent, IdChat)
                VALUES ('{req}', '{res}', '{chat_id}');"""
                .format(req=reqc, res=resc, chat_id=chat_id)
            )
            cur.close()
        except sqlite3.Error as e:
            print("Não foi possível gravar troca de mensagem.")
            print(e)

        con.commit()
        con.close()


    # Procedimento para deletar uma conversa.
    def delete_chat(chat_id: int):
        con = sqlite3.connect(DB.get_db_name())

        try:
            cur = con.cursor()
            cur.execute("""
                DELETE FROM Chat WHERE Id='{chat_id}';
            """.format(title=title))
            cur.close()
        except sqlite3.Error as e:
            print("Não foi possível deletar a conversa.\n")
            print(e)

        con.commit()
        con.close()


    # Procedimento para deletar uma troca de mensagem.
    def delete_interchange(iid: int):
        con = sqlite3.connect(DB.get_db_name())

        try:
            cur = con.cursor()
            cur.execute("""
                DELETE FROM Interchange WHERE Id='{iid}';
            """.format(iid=iid))
            cur.close()
        except sqlite3.Error as e:
            print("Não foi possível deletar a troca de mensagem.")
            print(e)

        con.commit()
        con.close()


    # Função para consultar todas as conversas.
    def fetch_chats():
        con = sqlite3.connect(DB.get_db_name())

        result = None
        try:
            cur = con.cursor()
            result = cur.execute("""
                SELECT * FROM Chat;
            """).fetchall()
            cur.close()
        except sqlite3.Error as e:
            print("Não foi possível recuperar as conversas.")
            print(e)

        con.commit()
        con.close()
        return result


    # Função para consultar as mensagens de uma conversa.
    def fetch_messages(chat_id: int):
        con = sqlite3.connect(DB.get_db_name())

        result = None
        try:
            cur = con.cursor()
            result = cur.execute("""
                SELECT * FROM Interchange
                WHERE IdChat='{chat_id}';
            """.format(chat_id=chat_id)).fetchall()
            cur.close()
        except sqlite3.Error as e:
            print("Não foi possível recuperar as mensagens da conversa.")
            print(e)

        con.commit()
        con.close()
        return result


    # Procedimento para gravar uma chave.
    def record_key(api_key: str):
        con = sqlite3.connect(DB.get_db_name())

        try:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO Key(Key)
                VALUES ('{api_key}');
            """.format(api_key=api_key))
            cur.close()
        except sqlite3.Error as e:
            print("Não foi possível gravar chave.")
            print(e)
            
        con.commit()
        con.close()


    # Função para recuperar chave.
    def fetch_key():
        con = sqlite3.connect(DB.get_db_name())

        result = None
        try:
            cur = con.cursor()
            result = cur.execute("""
                SELECT Key FROM Key
                WHERE Id=1;
            """).fetchone()
            cur.close()
        except sqlite3.Error as e:
            print("Não foi possível recuperar chave.")
            print(e)

        con.commit()
        con.close()
        return result


    # Procedimento para deletar chave.
    def delete_key():
        con = sqlite3.connect(DB.get_db_name())

        try:
            cur = con.cursor()
            cur.execute("""
                DELETE FROM Key
                WHERE Id=1;
            """)
            cur.close()
        except sqlite3.Error as e:
            print("Não foi possível deletar chave.")
            print(e)

        con.commit()
        con.close()


# Classe estática para interação com a OpenAI API.
class OAPI:
    # Procedimento para definir chave da API, se for válida.
    def set_api_key(key: str):
        if not OAPI.is_set_api_key():
            if OAPI.is_valid_api_key(key.CHAVE):
                DB.record_key(key.CHAVE)
            else:
                print("Chave inválida.")
        else:
            print("Uma sessão já está ativa.")


    # Procedimento para desativar chave da API.
    def unset_api_key():
        if OAPI.is_set_api_key():
            DB.delete_key()
            print("Desconectado.")
        else:
            print("Nenhuma sessão ativa.")


    # Função para verificar se uma chave está definida.
    def is_set_api_key():
        if DB.fetch_key() != None:
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
            return True
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
    DB.setup()
    if len(vars(cli_args)) > 1:
        cli_args.func(cli_args)
    elif len(vars(cli_args)) == 1:
        cli_args.func()
    #else:
    #    print("HI")
    #DB.setup()

    #DB.create_chat("Conversa")
    #DB.record_interchange("Vai", "Vem", 1)
    #print(DB.fetch_chats())
    #print(DB.fetch_messages("1"))
