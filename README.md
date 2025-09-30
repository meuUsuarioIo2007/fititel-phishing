# Bruce Phishing

## ⚠️ Aviso Ético e Legal ⚠️

Este projeto foi criado **estritamente para fins educacionais** e de pesquisa em segurança da informação. As ferramentas aqui contidas demonstram como ataques de phishing podem ser realizados, com o objetivo de ajudar estudantes e profissionais a entender e se defender contra essas ameaças.

**É estritamente proibido usar este projeto para atividades ilegais.** O uso indevido destas ferramentas contra sistemas ou indivíduos sem consentimento prévio e explícito é crime. O autor não se responsabiliza por qualquer uso malicioso ou dano causado por este projeto.

---

## Sobre o Projeto

Este repositório, desenvolvido por Laurindo Abel Afonso para a Feira de Inovação Tecnológica do ITEL (FITITEL), contém um framework simples com templates de phishing para diversas plataformas populares, criado para demonstrar um ataque de engenharia social.

### Funcionalidades

*   Templates de phishing para Amazon, Apple, Facebook, Instagram, Microsoft, Starbucks, Twitch e X.
*   Servidor backend em Python para servir as páginas e capturar as credenciais.
*   As credenciais capturadas são salvas no arquivo `logins.txt`.

---

## Como Usar

### Pré-requisitos

*   Python 3.x

### Executando o Servidor de Phishing

1.  Navegue até o diretório do projeto.
2.  Execute o servidor:
    ```bash
    python server.py
    ```
3.  Abra seu navegador e acesse `http://127.0.0.1:8080/<NOME_DO_SITE>.html` (ex: `http://127.0.0.1:8080/Facebook.html`).
4.  As credenciais inseridas serão salvas no arquivo `logins.txt`.

---

## Objetivo Educacional

Este projeto serve para ilustrar de forma prática:
*   O quão fácil é replicar a aparência de sites conhecidos.
*   Como as informações de um formulário são enviadas e capturadas por um servidor malicioso.
*   Os perigos de clicar em links suspeitos e inserir dados confidenciais.

## Licença

Distribuído sob a licença MIT.
