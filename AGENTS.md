# Instruções para agentes no AppEventos

## Organização de `src`

- Use `src/main.py` para montar o FastAPI, registrar roteadores e publicar os arquivos estáticos. O ponto de entrada é `src.main:app`.
- Centralize configurações da aplicação em `src/config.py` e parâmetros de conexão ao PostgreSQL em `src/infra/postgres.py`.
- Use `src/web/routers/` para declarar endpoints, receber parâmetros HTTP, chamar a operação correspondente e montar a resposta. Mantenha templates em `src/web/templates/`, agrupando telas e layouts relacionados.
- Coloque CSS, JavaScript, imagens e fontes em `src/web/static/`. Nos templates, gere URLs de recursos com `url_for('static', path=...)` e informe o caminho relativo a esse diretório.
- Organize as regras por funcionalidade. Use `src/modules/eventos/` para o cadastro e a localização de eventos e `src/modules/fiscais/` para os fiscais e o acesso corporativo. Nomeie cada módulo pela operação que realiza, como `municipio_por_coordenadas.py`.
- Mantenha validação de negócio e processamento nas funcionalidades. Mantenha formulários HTTP, templates e mapeamento de erros em respostas na camada web. Use `src/modules/sessao/` para sessão HTTP, cookies e contexto do perfil do cabeçalho.
- Mantenha as gravações relacionadas na mesma unidade de trabalho do `DbHandler`. Use `src/infra/` para a infraestrutura compartilhada de PostgreSQL e logging. O cliente da malha municipal do Ibama fica em `src/utils/api_municipios.py`.
- Use imports absolutos a partir de `src`. Ao mover módulos, atualize os imports, os pontos de substituição nos testes e as referências a arquivos nos templates.
- Execute `uv run pytest -q` na raiz para validar mudanças. Consulte o [README](README.md) para o mapa de arquivos e o comando de execução.

## Documentação de código

- Escreva a documentação em português, preservando os nomes de funções, parâmetros, tipos e APIs.
- Documente módulos, classes, funções e métodos públicos de Python ao criá-los ou alterar seu contrato.
- Use docstrings com aspas triplas. Comece com uma frase curta que descreva a responsabilidade. Após uma linha em branco, explique regras de negócio, efeitos colaterais ou decisões relevantes quando houver.
- Use as seções `Args:` e `Returns:`, nessa ordem. Em `Args:`, escreva `nome (tipo): descrição`. Omita `self` e `cls` e use `None.` quando não houver argumentos. Em `Returns:`, informe o tipo e o significado do retorno, incluindo o que representam valores vazios ou opcionais. Use `None.` quando a função apenas produzir efeitos colaterais.
- Acrescente `Raises:` depois de `Returns:` quando o contrato incluir exceções relevantes para o chamador. Descreva em que condição cada exceção é levantada.
- Em JavaScript, use JSDoc para funções que precisam de documentação e comente variáveis de escopo do arquivo quando sua responsabilidade ou seu ciclo de vida não estiver claro.
- Use comentários próximos ao código para explicar decisões, restrições de integrações e detalhes difíceis de inferir. Evite repetir o que a expressão já diz.
- Em tarefas de documentação, preserve o comportamento do código.

Exemplo de docstring Python

```python
def normalizar_nome(nome: str) -> str:
    """Remove espaços das extremidades de um nome.

    Args:
        nome (str): Nome recebido do formulário.

    Returns:
        str: Nome sem espaços nas extremidades. Pode ser vazio.
    """
    return nome.strip()
```
