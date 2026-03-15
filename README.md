# TEC2026_1_TFTP

Implementação de cliente e servidor TFTP em Python.

## Funcionalidades

- Cliente TFTP
- Servidor TFTP
- Interface CLI
- Transferência de arquivos via UDP

## Estrutura

tftp/ -> lógica do protocolo
cli/ -> interface de linha de comando
tests -> testes

## Executar

Servidor:

```bash
python cli/server_cli.py
```

Cliente:

```bash
python cli/client_cli.py 127.0.0.1 get arquivo.txt
```
