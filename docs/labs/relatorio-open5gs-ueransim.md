# Relatório de Laboratório — Open5GS + UERANSIM

**Nome:** Henrique Carmine  
**Email:** hc@cesar.school  
**Escola:** Cesar School  
**Professor:** Jonas Augusto Kunzler  
**Disciplina:** Interfaces e Protocolos Open RAN  
**RA:** 25000800  
**Matrícula / ID:** 25000800  
**Turma:** Individual  
**Data:** 09/04/2026  
**Título:** Laboratório Open5GS + UERANSIM — Interfaces e Protocolos

## 1. Resumo

Este relatório documenta a execução do laboratórios de Open5GS e UERANSIM em ambiente containerizado. O objetivo foi subir um 5GC Standalone (Open5GS) em Docker, criar um assinante compatível com o UE do UERANSIM, e verificar a conectividade nas interfaces N2 e N3/N4. O ambiente foi preparado em Fedora 43 com Docker Engine e Docker Compose v2.

## 2. Ambiente

- Sistema operacional: Fedora 43 x86_64
- Docker: 29.4.0, build 9d7ad9f
- Docker Compose: v5.1.2
- Kernel Linux: 6.19.11-200.fc43.x86_64
- Raiz do laboratório: `open5gs-containerized/`

## 3. Roteiro 01 — Core Open5GS

### 3.1 Preparação

O core foi iniciado com sucesso em `open5gs-containerized/core` usando o script:

```bash
./scripts/up_core.sh
```

### 3.2 Estado dos containers do Core

Saída de `docker compose ps` em `core/`:

- `open5gs-amf-containerized` — Up (healthy)
- `open5gs-ausf-containerized` — Up (healthy)
- `open5gs-dn-containerized` — Up
- `open5gs-mongodb-containerized` — Up (healthy)
- `open5gs-nrf-containerized` — Up (healthy)
- `open5gs-nssf-containerized` — Up (healthy)
- `open5gs-pcf-containerized` — Up (healthy)
- `open5gs-scp-containerized` — Up (healthy)
- `open5gs-smf-containerized` — Up (healthy)
- `open5gs-udm-containerized` — Up (healthy)
- `open5gs-udr-containerized` — Up (healthy)
- `open5gs-upf-containerized` — Up (healthy)
- `open5gs-webui-containerized` — Up (unhealthy)

### 3.3 Redes Docker do Core

As sub-redes configuradas e verificadas foram:

- `core_net-sbi`: `10.10.0.0/16`
- `core_net-n2`: `10.20.0.0/16`
- `core_net-n3`: `10.30.0.0/16`

### 3.4 Assinante

O assinante foi adicionado com sucesso usando:

```bash
./scripts/add-subscriber.sh
```

Subscriber adicionado:

- IMSI: `001010000000002`
- MSISDN: `33638060000`

### 3.5 Healthcheck do Core

O script `./scripts/healthcheck.sh` confirmou que os principais NFs do Core estão rodando e que as verificações de conectividade básicas estão corretas. O UERANSIM foi detectado com IP `10.60.0.2` e conectividade ativa.

## 4. Roteiro 02 — UERANSIM

### 4.1 Subida do RAN

O UERANSIM foi iniciado com sucesso em `open5gs-containerized/ueransim` e o container ficou com status `Up` e `healthy`.

### 4.2 Verificação do UE

O UE recebeu o endereço IP:

- `10.60.0.2`

### 4.3 Teste de conectividade entre containers

Foram realizados testes de ping entre containers para confirmar o funcionamento das redes N2, N3 e N4.

#### AMF → gNB (N2)

```bash
docker exec open5gs-amf-containerized sh -c 'ping -c 1 10.20.0.101 2>&1 | cat'
```

Resultado:
- `64 bytes from 10.20.0.101: icmp_seq=1 ttl=64 time=0.045 ms`
- `64 bytes from 10.20.0.101: icmp_seq=1 ttl=64 time=0.043 ms`
- `64 bytes from 10.20.0.101: icmp_seq=1 ttl=64 time=0.042 ms`
- `64 bytes from 10.20.0.101: icmp_seq=1 ttl=64 time=0.044 ms`

#### gNB → AMF (N2)

```bash
docker exec ueransim sh -c 'ping -c 1 10.20.0.11 2>&1 | cat'
```

Resultado:
- `64 bytes from 10.20.0.11: icmp_seq=1 ttl=64 time=0.050 ms`
- `64 bytes from 10.20.0.11: icmp_seq=1 ttl=64 time=0.037 ms`
- `64 bytes from 10.20.0.11: icmp_seq=1 ttl=64 time=0.036 ms`
- `64 bytes from 10.20.0.11: icmp_seq=1 ttl=64 time=0.037 ms`

#### gNB → UPF (N3)

```bash
docker exec ueransim sh -c 'ping -c 1 10.30.0.21 2>&1 | cat'
```

Resultado:
- `64 bytes from 10.30.0.21: icmp_seq=1 ttl=64 time=0.039 ms`
- `64 bytes from 10.30.0.21: icmp_seq=1 ttl=64 time=0.036 ms`
- `64 bytes from 10.30.0.21: icmp_seq=1 ttl=64 time=0.056 ms`
- `64 bytes from 10.30.0.21: icmp_seq=1 ttl=64 time=0.039 ms`

#### SMF → UPF (N4)

```bash
docker exec open5gs-smf-containerized sh -c 'ping -c 1 10.40.0.21 2>&1 | cat'
```

Resultado:
- `64 bytes from 10.40.0.21: icmp_seq=1 ttl=64 time=0.052 ms`
- `64 bytes from 10.40.0.21: icmp_seq=1 ttl=64 time=0.046 ms`
- `64 bytes from 10.40.0.21: icmp_seq=1 ttl=64 time=0.038 ms`
- `64 bytes from 10.40.0.21: icmp_seq=1 ttl=64 time=0.056 ms`

## 5. Discussão de protocolos

### N2 vs N3

- **N2** transporta o plano de controle entre gNB e AMF usando NGAP sobre SCTP.
- **N3** transporta o plano de usuário entre gNB e UPF usando GTP-U sobre UDP.

### Papel das redes no laboratório

- `core_net-n2` permite a sinalização NGAP entre AMF e gNB.
- `core_net-n3` permite o transporte de dados do UE até a UPF.
- `core_net-n4` permite a sinalização PFCP entre SMF e UPF, essencial para sessão PDU.

## 6. Observações

- O core está estável e todos os NFs principais estão em estado `healthy`.
- O container `open5gs-webui-containerized` aparece como `unhealthy` no compose; isso pode ser um item a monitorar em relatórios, mas não impede a operação do core nem a conectividade do UE.
- O UE do UERANSIM obteve IP corretamente, o que indica que a sessão PDU foi estabelecida.

## 7. Teste de throughput

Foram realizados testes de throughput entre containers nas interfaces N2 e N3 usando `iperf3`.

### N2 — AMF → gNB

Com o servidor `iperf3` rodando no namespace do container `open5gs-amf-containerized`, o cliente foi executado no namespace do container `ueransim` conectando-se ao IP `10.20.0.11`.

Resultado principal:
- Taxa média observada: **26.2 Gbits/sec**

### N3 — gNB → UPF

Com o servidor `iperf3` rodando no namespace do container `open5gs-upf-containerized`, o cliente foi executado no namespace do container `ueransim` conectando-se ao IP `10.30.0.21`.

Resultado principal:
- Taxa média observada: **23.2 Gbits/sec**

Esses testes confirmam que as redes virtuais entre containers suportam throughput de dezenas de Gbit/s dentro do ambiente Docker.

## 8. Conclusão

O laboratório foi concluído com sucesso. O Open5GS foi inicializado, o assinante foi criado e a conectividade entre core e RAN foi verificada. As interfaces N2, N3 e N4 foram testadas por meio de pings internos e demonstram comunicação válida entre os containers.

## 9. Evidências anexadas

- Saídas de `docker --version`, `docker compose version` e `uname -a`
- Saída de `docker compose ps` em `core/` e em `ueransim/`
- Saídas de `docker network inspect` de `core_net-sbi`, `core_net-n2` e `core_net-n3`
- Saída do script `./scripts/add-subscriber.sh`
- Saída do script `./scripts/healthcheck.sh`
- Resultados dos pings entre containers N2/N3/N4
- Resultados dos testes de throughput em `docs/labs/evidence/throughput-results.txt`

---

*Relatório gerado com base na execução atual do laboratório em Fedora 43.*
