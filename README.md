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

