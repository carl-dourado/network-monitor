# network-monitor

Esse repo nasceu porque as vezes eu queria saber se o basico da rede estava vivo antes de abrir varias abas e testar tudo na mao.

Ele checa tres coisas simples: `ping`, DNS e HTTP. Depois mostra o resultado numa pagina local e tambem em JSON.

Nao e um Zabbix, Prometheus ou coisa desse tamanho. E um monitor pequeno para treinar Python, HTTP local e diagnostico basico.

## o que tem aqui

- `monitor.py`: servidor local em Python
- checagem de ping
- checagem de DNS
- checagem HTTP
- pagina HTML gerada pelo proprio script
- endpoint JSON em `/api/status`
- zero dependencia externa de Python

## rodando

```bash
python monitor.py
```

Depois abre:

```text
http://127.0.0.1:5176
```

Tambem da para ver o JSON direto:

```text
http://127.0.0.1:5176/api/status
```

Se quiser mudar host ou porta:

```bash
python monitor.py --host 127.0.0.1 --port 5177
```

## o que eu treinei

- `http.server`
- servidor local com `ThreadingHTTPServer`
- resposta HTML e JSON no mesmo script
- `socket.getaddrinfo` para DNS
- `urllib.request` para HTTP
- uso do `ping` do sistema via Python

## limites

- nao tem autenticacao
- nao guarda historico
- nao tenta reiniciar servicos
- nao substitui monitoramento de verdade
- o HTML e gerado direto no Python para manter tudo em um arquivo

## o que falta

- permitir configurar alvos por argumento ou arquivo simples
- adicionar intervalo de atualizacao na pagina
- separar melhor HTML/CSS se o projeto crescer
- testar os checks sem depender de rede real
- mostrar tempo de resposta com mais detalhe

## nota

Esse repo e mais um exercicio de Python padrao do que uma ferramenta completa. A parte interessante foi juntar `ping`, DNS, HTTP e um servidor local pequeno sem framework.
