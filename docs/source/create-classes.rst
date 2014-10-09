Passos para configurar uma turma
################################

Criação do cliente e do gestor
------------------------------

Antes de tudo, adicione o registro de um cliente e defina qual ou quais os gestores desta nova conta. Para isso, acesse o painel administrativo e adicione um ou mais usuários no menu *Usuários* e adicione um cliente no link *Clientes*.

.. note::

   Uma mesma empresa pode ter diversos gestores, todos tem o mesmo nível hierárquico.

.. warning::

   Por enquanto não há um formulário de cadastro para o usuário aderir ao sistema, o cadastro do usuário é feito manualmente na tela de *usuários*.

Contratos
---------

As turmas usuárias do sistema estarão sempre relacionadas a um contrato do cliente. O contrato delimita detalhes de faturamento como CNPJ ou endereço.

Um mesma empresa pode ter vários contratos caso isso seja necessário para fins de faturamento (por exemplo, uma instituição com diversas unidades com números de CNPJ diferentes).

Adicione um contrato à empresa no painel administrativo, em  *Contratos*, ou na tela de configuração do cliente, no bloco de contratos abaixo dos campos do cliente em si.

O contrato ganha um número randômico automático e poderá ter turmas anexadas a ele, tanto pelo gestor do contrato quanto pela equipe de administração.

Professores e turmas
--------------------

Antes de adicionar novas turmas, precisa adicionar usuários para serem professores. Acesse como gestor do contrato, clique no menu `Professores` e então em adicionar professor.

.. note::

   O professor não é *adicionado* no sentido literal da palavra, ele é apenas relacionado ao cliente. Se um dia for removido do cliente, continuará com sua conta, só perderá sua ligação a tal cliente.

Ao cadastrar o professor, este receberá uma mensagem por e-mail avisando-o sobre sua nova conta de usuário e convidando-o a conhecer o sistema.

Neste momento, ele ainda não tem turmas relacionadas a si. Adicione turmas passando o mouse sobre o botão ações, na tela de contrato, à direita do contrato recém-criado, e clique em `adicionar turma`.

As turmas tem nome, que representará essa turma, e tem um professor, que é uma das opções da lista alimentada anteriormente.

Ao relacionar o professor com uma turma, este será avisado por e-mail e convidado para acessar a página de detalhes da turma.

.. note::

   Turmas tem, por padrão, um limite de 50 alunos. Este limite pode ser reconfigurado através do painel administrativo (pela equipe do Mainiti).

Datas sem atividade
-------------------

O gestor ainda tem a oportunidade de dizer quais as datas que a instituição não quer que o programa aconteça. Isso não é efetivo, o professor pode incluir uma data excluída pela instituição, tal função existe mais para facilitar o contato de gestor e professor neste assunto.

As datas podem ser excluídas de 3 formas:

 1. A equipe de administração pode excluir datas por padrão. Fins de semana são excluídos por padrão de sistema;

 2. O gestor pode excluir datas ou incluir datas excluídas por padrão (como fins de semana);

 3. O professor complementa datas de exclusão para si mesmo na instituição. Ele pode adicionar datas que tenham sido excluídas pela instituição ou por padrão pelo sistema. Na interface, fica denotado que a data está presente mas estava configurada para ser cancelada.

Inicialização da turma
----------------------

Uma vez que o gestor alocou o professor para a turma, após acessar com seu login e senha, o professor deve iniciá-la (clicando no botão *iniciar*).

Numa primeira etapa, ele precisa escolher o programa de exercício a ser aplicado na turma e a data de início do programa.

Neste momento ele terá a oportunidade de marcar datas a serem excluídas, assim como pode fazer o gestor. Como o programa é sempre distribuído linearmente a partir da data de início, as datas excluídas serão puladas.
 
.. warning::

   Da mesma forma que o monitor, o professor pode ter sua configuração de datas excluídas. Ao excluir datas durante a configuração de um programa, essa exclusão será salva como padrão para outros programas.

Ele precisa definir os alunos. Para isso, deve preencher uma caixa de texto onde digita um nome de aluno por linha. O sistema irá gerar uma senha para cada nome e permitir a impressão. O professor poderá recortar e colar na agenda de cada aluno, por exemplo.

.. note::

   Ao fazer a criação dos alunos, por trás dos panos, está criando contas de usuário. Se uma turma passa de um ano para outro, o professor terá que refazer o processo e teríamos várias duplicatas para o mesmo aluno na mesma instituição. Temos que pensar se isso não pode se tornar um problema e achar uma solução para os homônimos.

Identificação do usuário
------------------------

Como o nome não é uma informação particular o suficiente para ser garantidamente única, além do nome e da senha, o acesso do usuário acontece no programa em que foi inserido.

No relatório de senhas, além do nome e senha do aluno, há também um link único através do qual o aluno tem acesso a sua turma. Ao acessar este link, o aluno deve escolher ou informar seu nome e especificar sua senha para então ter acesso aos exercícios.

Uma vez que acessou, o sistema irá salvar um cookie que identifica o aluno e quando ele voltar, não precisará escolher o nome novamente, bastando digitar a senha, embora possa trocar o nome caso necessário.

.. note::

   Esta informação ficará salva tanto quanto for mantido o cache do navegador do aluno em sua máquina. Não há como garantir a persistência.

De posse de sua senha e do link de acesso, ao fazer o login, o aluno verá a lista de baterias de exercício programadas para o dia e poderá realizar suas atividades.
