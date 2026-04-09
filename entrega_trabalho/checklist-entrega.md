# Checklist de Entrega — Laboratório Open5GS + UERANSIM

## Identificação
- [ ] Nome completo
- [ ] Matrícula / ID
- [ ] Turma
- [ ] Data

## Conteúdo do relatório
- [ ] Resumo dos objetivos e resultados
- [ ] Ambiente usado (SO, Docker, Docker Compose)
- [ ] Passo a passo do Core (Roteiro 01)
- [ ] Passo a passo do UERANSIM (Roteiro 02)
- [ ] Discussão das interfaces N2, N3 e N4
- [ ] Conclusão breve
- [ ] Referências ou observações sobre limitações

## Evidências obrigatórias
- [ ] Saída de `docker --version`
- [ ] Saída de `docker compose version`
- [ ] Saída de `docker compose ps` no `core/`
- [ ] Saída de `docker compose ps` no `ueransim/`
- [ ] Saída de `docker network inspect` para `core_net-sbi`, `core_net-n2` e `core_net-n3`
- [ ] Saída de `./scripts/add-subscriber.sh`
- [ ] Saída de `./scripts/healthcheck.sh`
- [ ] Saída de `./scripts/test_ue_connection.sh`
- [ ] Resultados dos pings entre containers (N2/N3/N4)

## Prints / capturas de tela
- [ ] Print da WebUI do Open5GS em `http://localhost:9999`
- [ ] Print do terminal com as principais evidências
- [ ] Print das verificações do core e do UE

## Anexos
- [ ] Arquivos de logs `.txt` com as saídas principais
- [ ] Prints salvos em `.png` ou `.jpg`
- [ ] Qualquer captura de Wireshark ou PCAP (opcional)

## Conversão para PDF
- [ ] Se possível, gerar PDF a partir do `relatorio-open5gs-ueransim.md`
- [ ] Caso não consiga converter no terminal, exportar pelo editor ou copiar para um processador de texto

## Observação final
- [ ] Verifique se não há senhas ou dados sensíveis nos logs
- [ ] Revise o relatório antes de enviar
- [ ] Se enviar ZIP, inclua relatório + anexos claros
