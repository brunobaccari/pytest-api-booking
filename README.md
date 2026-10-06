# Restful Booker — Python e pytest

[English version](README.en.md)

Testes HTTP contra **https://restful-booker.herokuapp.com**. O foco é contrato, persistência e autorização sobre reservas criadas pela própria execução.

## Instalação

Python 3.12 ou superior. Crie um ambiente com `python -m venv .venv` e ative com `.venv\Scripts\activate` no Windows ou `source .venv/bin/activate` no Linux/macOS.

```bash
cp .env.example .env
python -m pip install -r requirements.txt
python -m pytest -q --junitxml=results/junit.xml
```

Não há servidor local. A comunicação usa `urllib` da biblioteca padrão.

## Cenários

- Criação seguida de consulta com comparação do contrato completo e tipos.
- Atualização total e parcial, conferindo persistência e campos preservados.
- Busca pelo nome exclusivo da reserva e confirmação do ID retornado.
- PUT e DELETE sem autenticação retornam 403 e não alteram a reserva.
- Exclusão autenticada seguida de consulta 404.
- Credenciais inválidas não retornam token.

## Dados e limpeza

`tests/conftest.py` prepara autenticação e reservas com nomes exclusivos. `tests/test_bookings.py` contém as verificações. Cada cenário apaga apenas a reserva que criou, inclusive quando o teste falha. A autenticação usa `admin/password123`, par público de demonstração documentado pelo serviço.

Esta API usa códigos próprios: criação e atualização retornam 200; exclusão retorna 201; login inválido retorna 200 com `reason`. Os testes seguem o contrato observado, sem trocar essas expectativas por convenções genéricas de REST.

## Relatórios

JUnit em `results/junit.xml`, publicado pelo CI. [Execuções e artifacts no Actions](https://github.com/brunobaccari/pytest-api-booking/actions). Referências: [documentação da API](https://restful-booker.herokuapp.com/apidoc/index.html) e [exemplo oficial do Robot Framework para o serviço](https://docs.robotframework.org/docs/examples/restfulbooker).

Ambiente público compartilhado; mudanças externas podem afetar os testes. Não há carga, mocks, servidor local ou promessa de validação completa de regras de preço. A versão anterior de cálculo local foi substituída por estes testes hospedados.

## Configuração do ambiente

Copie `.env.example` para `.env` (`Copy-Item .env.example .env` no PowerShell ou `cp .env.example .env` no Linux/macOS). As variáveis do processo têm prioridade. `.env` não é versionado. URLs e credenciais ficam nessa configuração; os valores esperados dos testes permanecem nos cenários.

As contas do exemplo são públicas e exclusivas de demonstração. Para outro ambiente, injete credenciais via secrets do CI e confirme também o contrato e os dados esperados antes de executar.

## Resultados no GitHub Actions

No GitHub, abra **Actions → Tests → execução → Summary** para ver status e contagens. Em **Artifacts**, baixe `results`: contém `junit.xml`. Os relatórios são enviados mesmo se os testes falharem e ficam disponíveis por 30 dias.

## Critério de bloqueio e triagem

A prioridade é autorização e integridade de dados: PUT, PATCH e DELETE são testados sem token e com token inválido. Cada recusa precisa manter a reserva idêntica; conferir apenas HTTP 403 não basta. A limpeza verifica GET 404 depois da exclusão, inclusive quando o serviço devolve 405 para uma reserva já removida.

Alteração não autorizada, perda de campos, reserva restante após limpeza ou relatório ausente bloqueiam a execução. Erro de rede/indisponibilidade do ambiente público é falha de ambiente, não aprovação nem defeito comprovado do produto. Investigue a primeira resposta e a consulta posterior da reserva própria; não repita a suíte até ficar verde nem apague reservas de terceiros. Não há teste de autorização entre contas: o serviço de demonstração compartilha credenciais administrativas.

Datas de commits deste portfólio foram reorganizadas retroativamente; as execuções do Actions mantêm suas datas reais.
