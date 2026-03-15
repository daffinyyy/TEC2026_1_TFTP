# Projeto TFTP (Trivial File Transfer Protocol) -- Atividade 002

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Protocol](https://img.shields.io/badge/Protocol-TFTP-green)
![Architecture](https://img.shields.io/badge/Architecture-C4%20Model-orange)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

Este projeto consiste na implementação de um **cliente e servidor TFTP
desenvolvidos em Python**, seguindo as especificações da **RFC 1350**.

O sistema permite realizar **transferências de arquivos utilizando
comunicação UDP**, implementando o fluxo de mensagens do protocolo
**TFTP (RRQ, WRQ, DATA, ACK e ERROR)**.

A arquitetura do sistema foi modelada utilizando o **modelo C4 de
arquitetura de software**, especificamente no **nível 3 (Component
Diagram)**.

------------------------------------------------------------------------

# 📑 Índice

-   Arquitetura do Sistema
-   Componentes do Sistema
-   Fluxo de Comunicação
-   Tecnologias Utilizadas
-   Estrutura do Projeto
-   Como Executar
-   Testes
-   Referências

------------------------------------------------------------------------

# 🏗️ Arquitetura do Sistema (Modelo C4 - Nível 3)

```{=html}
<p align="center">
```
`<img src="docs/c4-diagram.png" width="800"/>`{=html}
```{=html}
</p>
```
O diagrama acima apresenta a arquitetura de componentes do sistema TFTP,
mostrando a separação entre cliente, servidor e armazenamento.

------------------------------------------------------------------------

# 🧩 Componentes do Sistema

  Componente           Tipo                 Responsabilidade
  -------------------- -------------------- ------------------------------------------
  Interface CLI        Cliente              Recebe comandos `get` e `put` do usuário
  TFTP Client Module   Cliente              Implementa a lógica do protocolo TFTP
  UDP Socket           Cliente / Servidor   Gerencia comunicação via UDP
  Request Handler      Servidor             Processa requisições RRQ e WRQ
  File Manager         Servidor             Gerencia leitura e escrita de arquivos
  Filesystem           Armazenamento        Armazena arquivos transferidos

------------------------------------------------------------------------

# 🔄 Fluxo de Comunicação do Protocolo

O fluxo básico do protocolo TFTP ocorre da seguinte forma:

1.  O cliente envia uma requisição **RRQ** (download) ou **WRQ**
    (upload) para o servidor na **porta UDP 69**.
2.  O servidor responde utilizando **uma porta efêmera** para a
    transferência.
3.  A transferência ocorre através da troca de pacotes:
    -   **DATA**
    -   **ACK**
    -   **ERROR**
4.  Os dados recebidos são armazenados no **filesystem do servidor**.

------------------------------------------------------------------------

# 🛠️ Tecnologias e Padrões Utilizados

## Linguagem

-   Python 3

## Bibliotecas utilizadas

-   argparse -- construção da interface de linha de comando (CLI)
-   socket -- comunicação via UDP
-   os / io -- manipulação de arquivos no sistema operacional

## Padrões de Código

-   Código desenvolvido seguindo a **PEP 8**

## Controle de Versão

-   Git
-   Integração de código através de **Pull Requests**

------------------------------------------------------------------------

# 📂 Estrutura do Projeto

    tftp-project/
    │
    ├── tftp/
    │   └── lógica do protocolo TFTP
    │
    ├── cli/
    │   ├── client_cli.py
    │   └── server_cli.py
    │
    ├── tests/
    │   └── testes do sistema
    │
    ├── docs/
    │   └── c4-tftp-diagram.png
    │
    └── README.md

------------------------------------------------------------------------

# 🚀 Como Executar o Projeto

## Iniciar o servidor

``` bash
python cli/server_cli.py
```

## Executar o cliente

### Baixar arquivo do servidor

``` bash
python cli/client_cli.py 127.0.0.1 get arquivo.txt
```

### Enviar arquivo para o servidor

``` bash
python cli/client_cli.py 127.0.0.1 put arquivo.txt
```

### Estrutura do comando

    python cli/client_cli.py <ip_servidor> <comando> <arquivo>

Exemplo:

    python cli/client_cli.py 127.0.0.1 get arquivo.txt

------------------------------------------------------------------------

# 🧪 Testes Realizados

Os testes foram realizados utilizando clientes TFTP padrão para validar
a interoperabilidade do protocolo.

### Windows

Cliente TFTP nativo:

    tftp

### Linux / macOS

Cliente TFTP via terminal:

    tftp

Durante os testes foi verificada a correta troca de pacotes:

-   RRQ
-   WRQ
-   DATA
-   ACK
-   ERROR

------------------------------------------------------------------------

# 🔗 Referências

-   https://en.wikipedia.org/wiki/Trivial_File_Transfer_Protocol
-   https://datatracker.ietf.org/doc/html/rfc1350
-   https://www.geeksforgeeks.org/git/git-pull-request/