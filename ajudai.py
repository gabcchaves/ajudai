#! /usr/bin/env python3
# AjudaAI - Assistente virtual para sistemas operacionais baseados em Unix.
import openai, argparse, os, subprocess, sqlite3, textwrap


# Classe estática para interação com o banco de dados.
class DB:
    # Função para retornar o nome do banco de dados.
    def get_db_name():
        return "/home/gabriel/Dev/remote/involved/ajudai/ajudai.db"


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
            """).fetchone()[0]
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
                print("Conexão exitosa.")
            else:
                print("Chave inválida.")
        else:
            print("Uma sessão já está ativa.")


    # Procedimento para desativar chave da API.
    def unset_api_key():
        if OAPI.is_set_api_key():
            DB.delete_key()
            print("Desconexão exitosa.")
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
            return True
        except Exception as e:
            print(e)
            return False


    # Função para construção da mensagem em linguagem natural a ser enviada ao
    # modelo de linguagem.
    def build_prompt(request: str, question: bool = False):
        distro_name = subprocess.check_output(["lsb_release", "-d", "-s"])
        prompt = ""
        rules = ("\nVocê absolutamente não deve gerar texto sobre qualquer outro"
        "assunto que não seja abrangido pela ciência da computação. Se for"
        "pedido para fazê-lo, retorne a mensagem: Não posso falar sobre isso."
        "Seja direto; não explique nada, apenas providencie o que foi pedido."
        "Você não precisa dizer que não pode falar de outro assunto se o"
        "usuário não inquiriu sobre outro assunto.")

        if question:
            prompt += f"{request}. {rules}"
        else:
            prompt += (f"Escreva uma sequência de um ou mais comandos que,"
            f"quando executada (realize a seguinte tarefa): {request}."
            f"\nCertifique-se de que a sequência esteja toda correta e funcione no"
            f"{distro_name}.\nMostre a sequência sem aspas ou coisas"
            f"semelhantes, e separe os comandos por &&. Gere apenas comandos em"
            f"Shell; se não puder gere -1.")
        
        return prompt


    # Procedimento para executar comandos Shell.
    def subprocess_cmd(commands):
        for cmd in commands:
            if "sudo" in cmd:
                try:
                    p = subprocess.Popen(cmd, shell=True)
                    psswd = input()
                    p.communicate("{}\n".format(psswd))
                except KeyboardInterrupt:
                    print("Comando interrompido.")
            else:
                try:
                    subprocess.Popen(cmd, shell=True)
                except KeyboardInterrupt:
                    print("Comando interrompido.")


    # Procedimento para enviar requisição ao modelo de linguagem.
    def submit(request: str, question: bool = False):
        prompt= OAPI.build_prompt(request, question=question)

        openai.api_key = DB.fetch_key()

        try:
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": ("Você é uma aplicação CLI"
                        "que gera comandos para Linux Shell.")},
                    {"role": "user", "content": prompt}
                ],
                max_tokens = 300 if question else 180,
                temperature = 0
            )

            if question:
                resc = response["choices"][0]["message"]["content"]
                width_term = shutil.get_terminal_size().columns
                width_text = int(term_width * 0.8)
                text = textwrap.fill(resc, width=width_text)
                print(text)
                DB.record_interchange(request, resc, 1)
            else:
                commands = response["choices"][0]["message"]["content"].split("&&")
                OAPI.subprocess_cmd(commands)
        except Exception as e:
            print("Não foi possível submeter mensagem ao modelo de linguagem.")
            print(e)


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
        if hasattr(cli_args, "COMANDO"):
            cli_args.func(cli_args)
        elif hasattr(cli_args, "PERGUNTA"):
            cli_args.func(cli_args.PERGUNTA, True)
    elif len(vars(cli_args)) == 1:
        cli_args.func()
    else:
        print("HI")
    #DB.setup()

    #DB.create_chat("Conversa")
    #DB.record_interchange("Vai", "Vem", 1)
    #print(DB.fetch_chats())
    #print(DB.fetch_messages("1"))
