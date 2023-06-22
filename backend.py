import openai


class ajudaAi:
    

    def __init__(self, os_name: str, shell_name: str, user: str, api_key: str):
        self.os_name = os_name
        self.shell_name = shell_name
        self.user = user
        openai.api_key = api_key
    
    # 'explain' é um parametro opcional na qual infere se haverá explicação ou não acerca do comando
    def build_prompt(self, wish: str, os_name: str, shell_name: str, explain: bool = False):
        explain_text = ""
        format_text = "Comando: <inserir comando aqui>"

        if explain:
            # Obriga ao chat à escrever uma descrição sobre o comando e atribui um formato para essa descrição
            explain_text += "Também quero uma explicação detalhada sobre o código e como ele funciona"
            format_text += "\nDescrição: <inserir descrição aqui>\nA descrição deve ser escrita na mesma língua que a pergunta"
        
        # Lista que contém todas as informações que criam o prompt ideal
        prompt_list = [ 
            f"Instruções: Escreva um comando CLI que faz o seguinte: {wish}. Tenha certeza de que esse comando está correto e funiona no {os_name} usando o {shell_name}. {explain_text}",
            f"Formato: {format_text}",
            f"Caso a explicação não seja pedida de forma explícita mostre apenas o comando e nenhuma explicação acerca do comando",
            f"Mostre o comando sem o caractere ` ou ´ ou '",
            f"Certifique de usar o formato acima de forma exata",
        ]

        # Retorna uma string contendo as informações do prompt_list separadas por \n\n
        return "\n\n".join(prompt_list)


    def ask(self, wish: str, explain: bool = False):
        prompt= self.build_prompt(wish, self.os_name, self.shell_name, explain=explain)

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

    user = ajudaAi("Linux", "Bash", "Pedro", "api-key")

    print(user.ask("Como baixar e instalar o vscode pelo terminal usando o gerenciador de pacotes flatpak", explain=False))
