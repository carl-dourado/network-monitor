# network-monitor

Monitor local simples para ver se o basico esta vivo.

Ele checa ping, DNS e HTTP e abre uma pagina pequena no navegador. Fiz para rodar na minha maquina, sem conta, sem banco, sem dependencia.

## uso

```bash
python monitor.py
```

Depois abre:

```text
http://127.0.0.1:5176
```

Tambem tem JSON:

```text
http://127.0.0.1:5176/api/status
```

## notas

- feito para uso local
- usa bibliotecas padrao do Python
- o ping depende do comando `ping` do sistema

## limites

- nao tem autenticacao
- nao guarda historico
- nao tenta reiniciar servicos
- nao substitui monitoramento de verdade
- o HTML e gerado direto no Python para manter tudo em um arquivo

## coisas para melhorar depois

- permitir configurar alvos por argumento ou arquivo simples
- adicionar intervalo de atualizacao na pagina
- separar melhor HTML/CSS se o projeto crescer
- testar os checks sem depender de rede real

## anotacoes de aprendizado

Esse repo e mais um exercicio de Python padrao do que uma ferramenta completa. A parte interessante foi juntar `ping`, DNS, HTTP e um servidor local pequeno sem framework.
