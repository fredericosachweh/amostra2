Mapa de views e templates
#########################

O mapeamento de urls é dividido em 3 namespaces:

* managers: views relacionadas a operações de gerência, como criar turmas, relacionar professores ou realizar pagamentos.
* teachers: views relacionadas a operações realizadas pelo professor como ver dados estatísticos de turmas, iniciar programa e outros.
* students: views relacionadas a tarefas realizadas pelo aluno, essencialmente resolução de exercícios nas baterias disponíveis para o dia atual.

Gestor / Manager
----------------

* Lista de contratos (manager:contract-list): list view para *client/contract_list.html*

 * Adicionar contrato (manager:contract-create): redirect view para manager:contract-detail
 * Remover contrato (manager:contract-delete)
 * Financeiro
 * Turmas (manager:contract-klasses): list view para *client/klass_list.html*

  * Adicionar turma (manager:klass-create): edit view para *client/klass_create.html*
  * Alterar turma (manager:klass-update)
  * Remover turma (manager:klass-remove)

* Professores

 * Adicionar professor
 * Anexar professor
 * Liberar professor

* Datas sem atividade

Professor / Teacher
-------------------

* Lista de turmas

 * Inicialização de turma (program-create)
 * Detalhes de turma em andamento (program-detail)

  * Lista de exercícios

   * Detalhes de exercício

Aluno / Student
---------------

* Lista de exercícios do dia

 * Iniciar bateria

  * Resolver exercício

 * Fim da bateria
