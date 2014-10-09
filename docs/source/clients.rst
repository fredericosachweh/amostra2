Clientes
========

.. _clientes_status:

Status de clientes
------------------

O cliente pode assumir um dos status abaixo:

* Suspect: empresa recém importada ou com nenhum histórico de relacionamento;
* Prospect: empresa tem alguma tarefa de followup relacionada a si ou alguma
  demonstração, indicando que passou pela análise de um vendedor;
* Lead: empresa que tem apenas uma parcela de pagamento e esta está pendente,
  indicando que acabou de recebê-la de um vendedor ou acabou de finalizar o
  processo de compras pós-demonstração;
* Ativo: empresa com turmas não finalizadas que estão em contratos em dia. Se
  o contrato está pendente por uma única parcela, é lead. Se não há pagamentos
  gerados, não fechou a compra então é prospect. Se tem mais de uma parcela,
  sendo alguma pendente, é congelado, se não tem pendências mas as turmas
  encerraram, é inativo;
* Congelado: empresa com turmas não finalizadas que estão em contratos com mais
  de uma parcela, sendo um ou mais pendentes;
* Inativo: empresa que teve turmas e pagamentos mas, no momento, nenhuma de
  suas turmas estão ativas, embora não tenha formalmente cancelado as
  atividades (tem o mesmo peso de um lead);
* Suspenso: empresa pede suspensão temporária das atividades;
* Cancelado: empresa pede cancelamento dos serviços prestados;
* Removido: empresa é removido pela administração do Mainiti por não haver
  interesse nele como cliente;
