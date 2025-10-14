# Guia de Contribuição

Obrigado por considerar contribuir para este projeto! Este documento fornece diretrizes para contribuições.

## Como Contribuir

### Reportando Bugs

Se você encontrar um bug, por favor abra uma issue incluindo:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. comportamento atual
- Versão do Python e das dependências
- Sistema operacional

### Sugerindo Melhorias

Sugestões de melhorias são bem-vindas! Por favor:
- Descreva claramente a melhoria proposta
- Explique por que seria útil
- Forneça exemplos de uso, se possível

### Pull Requests

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Faça suas alterações
4. Execute os testes (`uv run pytest`)
5. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
6. Push para a branch (`git push origin feature/MinhaFeature`)
7. Abra um Pull Request

## Padrões de Código

### Estilo Python

Este projeto segue as convenções PEP 8. Use as ferramentas de formatação:

```bash
# Formatar código
uv run black src/ tests/ examples/

# Verificar linting
uv run ruff check src/ tests/ examples/
```

### Documentação

- Use docstrings no formato NumPy/SciPy
- Documente todos os parâmetros e retornos
- Inclua exemplos quando apropriado

Exemplo:
```python
def minha_funcao(param1, param2):
    """
    Breve descrição da função
    
    Parameters
    ----------
    param1 : tipo
        Descrição do param1
    param2 : tipo
        Descrição do param2
        
    Returns
    -------
    tipo
        Descrição do retorno
        
    Examples
    --------
    >>> minha_funcao(1, 2)
    3
    """
    return param1 + param2
```

### Testes

- Escreva testes para novas funcionalidades
- Mantenha cobertura de testes alta
- Use pytest para testes

```bash
# Executar todos os testes
uv run pytest

# Executar com cobertura
uv run pytest --cov=src/projeto_pesquisa_ebm
```

### Commits

Use mensagens de commit claras e descritivas:

- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para mudanças na documentação
- `test:` para adição/modificação de testes
- `refactor:` para refatorações
- `style:` para mudanças de formatação

Exemplos:
```
feat: adiciona função para calcular potência
fix: corrige cálculo de velocidade em calculate_velocity
docs: atualiza README com exemplos de uso
test: adiciona testes para MassSpringDamperModel
```

## Estrutura de Arquivos

Ao adicionar novos arquivos, siga a estrutura:

```
src/projeto_pesquisa_ebm/  # Código fonte
tests/                      # Testes
examples/                   # Exemplos de uso
notebooks/                  # Notebooks Marimo
docs/                       # Documentação adicional
```

## Notebooks Marimo

Ao criar ou modificar notebooks:

1. Use células pequenas e focadas
2. Documente o propósito de cada célula
3. Inclua visualizações quando apropriado
4. Teste o notebook completo antes de commitar

```bash
# Executar notebook
uv run marimo edit notebooks/seu_notebook.py

# Executar como script para testar
uv run marimo run notebooks/seu_notebook.py
```

## Dependências

Ao adicionar novas dependências:

1. Use `uv pip install <pacote>`
2. Atualize `pyproject.toml` se necessário
3. Documente o uso da nova dependência
4. Considere se é uma dependência principal ou de desenvolvimento

```bash
# Adicionar dependência principal
uv pip install <pacote>

# Adicionar dependência de desenvolvimento
uv pip install --dev <pacote>
```

## Processo de Review

Pull requests serão revisados considerando:

1. **Funcionalidade**: O código faz o que deveria?
2. **Testes**: Há testes adequados?
3. **Documentação**: O código está bem documentado?
4. **Estilo**: Segue os padrões do projeto?
5. **Compatibilidade**: Não quebra funcionalidades existentes?

## Dúvidas?

Se tiver dúvidas sobre como contribuir:
- Abra uma issue com a tag `question`
- Entre em contato com os mantenedores
- Consulte a documentação existente

## Código de Conduta

- Seja respeitoso e profissional
- Aceite críticas construtivas
- Foque no que é melhor para o projeto
- Mostre empatia com outros contribuidores

Obrigado por contribuir! 🎉

