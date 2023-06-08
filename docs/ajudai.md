### Ajudai - Assistente Virtual de SO

#### SINOPSE
ajudai [opções] args...

#### DESCRIÇÃO
Ajudai é um assistente virtual de sistemas operacionais baseados em Unix. Sua função é fornecer suporte aos usuários que desejam aprender mais sobre seus sistemas operacionais, bem como automatizar operações de administração de sistemas.

#### OPÇÕES
##### --connect

Autentica usuário a por meio da chave OpenAI passada como argumento.

##### --disconnect

Desconecta usuário.

##### --new

Cria uma nova conversa, com um nome especificado. Caso o nome especificado como argumento já esteja em uso por outra conversa, o usuário será avisado. Caso nenhum nome seja especificado como argumento, um nome será gerado pelo programa.

##### --rename

Renomeia uma conversa. Nenhum argumento é passado a essa opção, pois ela exibe uma lista enumerada de conversas existentes, e lê um número correspondente, e lê o novo nome da conversa. Caso o número lido seja inválido, outro número é solicitado. Caso o novo nome já esteja em uso por outra conversa, o usuário é informado e o programa termina com erro; caso o novo nome seja o mesmo, o usuário é informado e nenhuma operação é realizada; caso nenhum nome seja lido, o usuário é informado, e o programa termina com erro.

##### --delete

Deleta uma conversa. Nenhum argumento é passado a essa opção, pois ela exibe uma lista enumerada de conversas existentes, e lê um número, e deleta a conversa correspondente. Caso o número lido não corresponda a uma conversa existente, o usuário é informado e outro número é solicitado.

##### --history

Exibe histórico de conversas.

##### --toggle

Alterna para uma conversa. Essa opção permite alternar de uma conversa para outra, informando o identificador da conversa. Cada conversa possui um identificador numérico, que pode ser passado como argumento a essa opção, alternando a conversa em uso. Caso nenhum identificador seja especificado, uma lista enumerada de todas as conversas é exibida, e é lido um número referente a uma conversa para ser ativada.

##### -q, --question

Lê uma entrada textual (geralmente pergunta do usuário), passada como argumento ou não, e retorna a resposta gerada pelo modelo de linguagem. Caso nenhuma entrada textual seja fornecida como argumento a essa opção, um editor de texto padrão é executado, onde o usuário deve escrever seu texto e salvar.

##### -o, --operation

Lê uma instrução em linguagem natural do usuário, passada como argumento ou não, e executa, mediante permissão do usuário, o que for passível de ser executado. Caso nenhuma instrução seja passada como argumento a essa opção, um editor de texto é executado, onde o usuário deve escrever suas instruções e salvar.
