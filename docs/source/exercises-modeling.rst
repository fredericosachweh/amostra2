Modelagem de exercícios
=======================

Os exercícios são organizados pelas seguintes informações:

* matérias, como matématica ou português;
* assuntos, como adição, subtração ou frações;
* categorias, como adição com resultado em duas casas, mmc, subtração ou
  comparação de frações;

Os exercícios são parametrizados e podem conter várias perguntas e respostas. O
aluno acertará o exercício todas as suas respostas estiverem corretas.

.. note::

   Não há cálculos matemáticos na solução do exercício. A definição de erro e
   acerto é por pura comparação.

Os assuntos e as categorias dirão como será a apresentação gráfica de cada
exercício, isto é, onde serão dispostas as perguntas e onde irão aparecer as
respostas.

Os exercícios, exceto caso especiais especificados na documentação, serão
criados programaticamente, isto é, através de scripts de geração que fazem
parte do sistema.

Programas de exercícios
-----------------------

Programas de exercícios são grupos de exercícios a serem executados
diariamente. São compostos por módulos que por sua vez incluem baterias com
exercícios de uma ou mais categorias.

Para criar um programa, no painel administrativo, acesse *Programas de
exercícios* -> *Programas de exercícios*. Deverá especificar o nome do
programa, sua matéria e descrição.

Não é preciso se preocupar em cadastrar módulos ou qualquer outra informação, a
alimentação do programa se dará através da importação de um arquivo csv que
contém os módulos, baterias e categorias a serem usados.

Importação de programas
"""""""""""""""""""""""

A importação do programa se dá através de um arquivo csv. Nele, cada bateria
(que corresponde a um dia) é representada por uma ou mais linhas no arquivo de
importação. A primeira linha de uma bateria deve incluir o dia, o módulo ao
qual pertence e seu nome.

Mais de uma linha pode ser usada para representar a bateria. As linhas
subsequentes devem ter o dia, o módulo e o nome em branco afim de denotar que
trata-se de um complemento ao dia ainda *aberto*.

Estas linhas de uma bateria permitem definir *aplicações de categorias* para
este dia. Tais aplicações dizem de qual categoria utilizar exercícios, qual
quantidade usar, se será usado na ordem sequencial ou aleatória e como serão
filtrados os exercícios encontrados.

Veja abaixo um exemplo de um arquivo de importação:

+-----+-----------+----------------------------+----------------------+--------+------------+---------+---------+---------+---------+
| Dia | Módulo    | Nome                       | Categoria            | Quant. | Ordem      | F1 Inf. | F1 Sup. | F2 Inf. | F2 Sup. |
+=====+===========+============================+======================+========+============+=========+=========+=========+=========+
| 1   | Adição    | De 1+1 até 20+1            | Soma dois andares    | 20     | Aleatório  | 1       | 20      | 1       | 1       |
+-----+-----------+----------------------------+----------------------+--------+------------+---------+---------+---------+---------+
|     |           |                            | Soma dois andares    | 10     | Sequencial | 1       | 20      | 1       | 1       |
+-----+-----------+----------------------------+----------------------+--------+------------+---------+---------+---------+---------+
| 2   | Adição    | De 1+2 até 20+2            | Soma dois andares    | 30     | Sequencial | 1       | 20      | 2       | 2       |
+-----+-----------+----------------------------+----------------------+--------+------------+---------+---------+---------+---------+
| 3   | Subtração | De 1-1 até 30-1            | Subtração            | 40     | Aleatório  | 1       | 30      | 1       | 1       |
+-----+-----------+----------------------------+----------------------+--------+------------+---------+---------+---------+---------+
| 4   | Subtração | Avaliação soma e subtração | Subtração            | 40     | Aleatório  | 1       | 30      | 1       | 1       |
+-----+-----------+----------------------------+----------------------+--------+------------+---------+---------+---------+---------+
|     |           |                            | Soma dois andares    | 20     | Sequencial | 1       | 20      | 1       | 1       |
+-----+-----------+----------------------------+----------------------+--------+------------+---------+---------+---------+---------+
|     |           |                            | Soma três andares    | 20     | Aleatório  |         |         |         |         |
|     |           |                            | resultado duas casas |        |            |         |         |         |         |
+-----+-----------+----------------------------+----------------------+--------+------------+---------+---------+---------+---------+

Determinadas categorias definem variáveis de controle que podem ser usadas para
filtragem de resultados. São duas variáveis numéricas: *filtro 1* e *filtro 2*.

.. note::

   Diferentes tipos de exercício podem usar as variáveis de filtragem de formas
   diversas. Procure ler a documentação de cada tipo de exercício para conhecer
   suas especificações.

Algumas categorias não definem ou não podem definir tais filtros, por exemplo
uma soma de três andares. São três números para filtragem mas por ser um caso
tão específico, provavelmente possa já ser agrupado de forma segmentada, isto
é, teremos algumas categorias de soma com resultado em três casas que serão
usadas para agrupar exercícios de dificuldade similar.

Alguns pontos são importantes:

1. O número do dia existe para seu controle, não será respeitado na hora da
   importação mas é útil para garantir que o número de dias planejados foi
   atendido;
#. O nome do módulo será mostrado para alunos e professores, então tome cuidado
   com a ortografia;
#. O módulo não precisa existir, se especificar um módulo inexistente, ele será
   criado;
#. O professor será capaz de reordenar módulos, desta forma, recomenda-se
   *quebrar* módulos extensos em versões menores (por exemplo, ao invés de 1
   módulo de 15 dias de soma, melhor usar 3 módulos de soma com níveis de
   dificuldade diferentes);
#. O nome da bateria/dia será mostrado para professores. Procure usar nomes
   significativos, este nome será usado para mostrar o conteúdo programático;
#. A categoria **precisa** existir no sistema, se especificar uma categoria
   inexistente, o sistema acusará o erro;
#. Ao criar as categorias, procure usar nomes curtos. Trata-se de uma
   informação interna, não será mostrada a professores ou alunos;
#. Nos campos F1 Inf., F1 Sup., F2 Inf. e F2 Sup., o F significa *filtro* e os
   termos Inf. e Sup. significam limite inferior e limite superior,
   respectivamente;

Para importar, edite ou crie um novo programa: ele precisa existir previamente.
Clique então em *Importar/sobrescrever programa*. Neste momento, será convidado
a escolher um arquivo CSV **separado por vírgulas**.

Desacoplação de exercícios
""""""""""""""""""""""""""

Os exercícios estão desacoplados da programação de baterias. Isto é, você pode
programar todo um período e, caso não existam exercícios de determinada
categoria, os dias previstos para ela estarão em branco, mas a modelagem já
pode ser realizada *a priori*.

Tipos de exercícios
-------------------

Romano para decimal
"""""""""""""""""""

Pede que o aluno *digite o número que corresponde ao símbolo romano N* e
oferece espaço para digitação da resposta decimal.

Na importação do programa, tem uma variável de controle que permite escolher,
para determinada bateria, números entre o limite superior e inferior dela.

Há exercícios de romano para decimal entre o número 1 e o número 100.

Decimal para romano
"""""""""""""""""""

Pede ao aluno que diga a *qual número romano corresponde o número N*. Oferece
uma lista de 5 opções de forma que apenas uma seja a correta.

Cada exercício de *decimal para romano* tem 10 opções de escolha, dadas pelo
intervalo entre a dezena anterior e a próxima ao número N. Suponha que N seja
17, as opções são os números entre 10 e 20, devidamente convertidos em romanos.

Ao abrir um exercício deste tipo, o sistema irá sortear 5 opções dentre as 10
disponíveis, garantindo que uma delas seja a resposta correta. Com isso,
garantimos que dois alunos não veram as mesmas opções nas mesmas ordens.

Na importação do programa, tem uma variável de controle que permitirá escolher,
para determinada bateria, números entre o limite superior e inferior dela.

Há exercícios de decimal para romano entre o número 1 e o número 100.

Soma dois andares
"""""""""""""""""

Oferece a operação de soma *armada* para que o aluno responda cada dígito da
resposta. Opera em apenas 2 andares (por exemplo 25+39, 15+18 ou 2+2).

Na importação do programa, tem 2 variáveis de controle que permitem escolher,
para determinada bateria, números entre o limite superior e inferior para o
primeiro andar e o segundo respectivamente.

Há exercícios de soma de dois andares até 999 no primeiro e no segundo andar.

Soma dois andares (decimal)
"""""""""""""""""""""""""""

Oferece a operação de soma *armada* em dois andares com números decimais
devidamente alinhados (por exemplo 2,5+1,1 ou 2,453+3,412).

Geração
'''''''

Os exercícios de soma decimal são gerados até um limite inteiro entre 0,1 e um
décimo do limite. Por exemplo, se o limite é 100, para duas casas decimais,
serão gerados exercícios cujos primeiro e segundo andar estão entre 0,01 e 99,99.

Na geração será necessário dizer quantas casas decimais se trabalhar e isso
impactará no número de exercícios. Limite 100 para exercícios de 1 casa gera
algo próximo de 1 milhão de exercícios, já com duas casas decimais, serão
gerados cerca de 10 milhões de exercícios.

.. note::

   Não serão gerados exercícios terminados com zero (por exemplo, 1,10 ou
   2,350).

Importação
''''''''''

Na importação do programa, 2 variáveis de controle que permitem escolher,
para determinada bateria, números entre o limite superior e inferior para o
primeiro e segundo andar respectivamente.

Além dos limites, será necessário especificar uma tag que identifica o número
de casas decimais, na forma *N-casas* (por exemplo, *2-casas*, *3-casas* ou
*4-casas*).

Isto é necessário para poder dirimir ambiguidades, afinal, *1.05+3.01* pode
pertencer ao mesmo intervalo que *1.051+3.011*.

Subtração dois andares
""""""""""""""""""""""

Oferece a operação de *subtração* para que o aluno responda cada dígito da
resposta. Opera em apenas 2 andares (por exemplo 25-19, 18-13 ou 2-1).

Na importação do programa, tem 2 variáveis de controle que permitem escolher,
para determinada bateria, números entre o limite superior e inferior para o
primeiro andar e o segundo respectivamente.

Há exercícios de subtração de dois andares até 9.999 no primeiro e/ou no
segundo andar, nunca com resultados negativos.

Adição e subtração na ordem em que elas aparecem
""""""""""""""""""""""""""""""""""""""""""""""""

Oferece *expressões* de soma e subtração com 3 ou mais termos num layout que
força o aluno a resolver etapa por etapa, na sequencia em que os dígitos
aparecem na conta.

Na importação do programa, tem 2 variáveis de controle que dizem o menor termo e
o maior termo da expressão, respectivamente. Isso permite escolher exercícios
com base nos termos, por exemplo:

* Exercícios cujo menor termo esteja entre 10 e 20 e cujo maior termo esteja
  também entre 10 e 20 (por exemplo 10+17-13 ou 14+14-14). Sempre aparecerão
  dezenas entre 10 e 20 nos termos.
* Exercícios cujo menor termo enteja entre 1 e 10 e cujo maior termo esteja
  entre 10 e 20 (por exemplo 1+17-15, 12+9-3). Sempre aparecerá um termo menor
  que 10 e outro termo maior que 10 e menor que 20.

.. note::

   Não serão gerados exercícios iniciados por zero ou que tenham mais de uma
   ocorrência de zero na conta.

Tags de expressões de adição e subtração
''''''''''''''''''''''''''''''''''''''''

Os resultados, tanto parciais quanto final, podem ser negativos. Caso exista
algum resultado negativo, os exercícios serão marcados com a tag
*result-negat*, do contrário, serão marcados com a tag *result-posit*. Se na
importação não se especificar uma tag de filtragem, os dois tipos serão
oferecidos como opção para randomização.

Além disso, caso a operação comece com um número negativo (por exemplo -1+3-2),
o exercício será identificado com a tag *inicio-negat*, do contrário, será
marcado com a tag *inicio-posit*.

Expressões de multiplicação e divisão
"""""""""""""""""""""""""""""""""""""

Oferece *expressões* que envolvem multiplicação, divisão, subtração e adição
num layout que força o aluno a resolver primeiro as multiplicações e divisões e
depois as somas e subtrações.

Na importação do programa há duas variáveis de controle que dizem o menor termo
e o maior termo da empressão, respectivamente. Isso permite escolher exercícios
com base nos termos, por exemplo:

* Exercícios cujo menor termo esteja entre 10 e 20 e cujo maior termo esteja
  também entre 10 e 20 (por exemplo 2*10+16/4). Sempre aparecerão
  dezenas entre 10 e 20 nos termos.
* Exercícios cujo menor termo enteja entre 1 e 10 e cujo maior termo esteja
  entre 10 e 20 (por exemplo 2*9+18/3). Sempre aparecerá um termo menor
  que 10 e outro termo maior que 10 e menor que 20.

.. note::

   Não serão gerados exercícios cuja multiplicação ou divisão resultem em
   números decimais e não serão gerados exercícios cuja divisão se dê por zero
   (que é uma indeterminação).

Tags de expressões de multiplicação e divisão
'''''''''''''''''''''''''''''''''''''''''''''

Caso haja a ocorrência de exercícios com operações de multiplicação ou divisão
em que o primeiro termo seja zero (0/2 ou 0*2 por exemplo), o exercício será
identificado com a tag *com-zero*, do contrário, será identificado com a
tag *sem-zero*.

Caso a operação envolva apenas multiplicação, somas e subtrações, terá a tag
*sem-divisao*, do contrário, terá a tag *com-divisao*.

Caso o primeiro termo seja um número negativo, haverá a tag *inicio-negat*, do
contrário, haverá a tag *inicio-posit*.

Caso as operações de soma e subtração retornem resultados positivos, haverá uma
tag *result-posit*, do contrário, haverá a tag *result-negat*.

Caso não especifique uma tag na hora de filtrar a categoria num programa, ambos
os casos serão oferecidos.

Mínimo múltiplo comum
"""""""""""""""""""""

Oferece exercícios de MMC (mínimo múltiplo comum) em layout idêntico ao
praticado manualmente em cadernos, por exemplo.

Na importação do programa há duas variáveis de controle que dizem o menor termo
e o maior termo da empressão, respectivamente. Isso permite escolher exercícios
com base nos termos, por exemplo:

* Exercícios cujo menor termo esteja entre 10 e 20 e cujo maior termo esteja
  também entre 10 e 20 (por exemplo MMC(10,18,20) ou MMC(10,15,17)). Sempre
  aparecerão dezenas entre 10 e 20 nos termos.
* Exercícios cujo menor termo enteja entre 1 e 10 e cujo maior termo esteja
  entre 10 e 20 (por exemplo MMC(5,10,15) ou MMC(2,4,18)). Sempre aparecerá um
  termo menor que 10 e outro termo maior que 10 e menor que 20.

.. note::

   Não existirão exercícios com termos menores que 2, não faz sentido aplicar
   um MMC com o número 1 ou 0 entre os termos.

Tags de mínimo multiplo comum
'''''''''''''''''''''''''''''

O número de termos, diferente de outros casos, não é segmentado por categoria,
a categoria MMC envolve exercícios com 2, 3 ou 4 termos. Para segmentar a
aplicação da categoria, especifique uma tag como 2-terms, 3-terms ou 4-terms.

Área de quadradinhos
""""""""""""""""""""

Oferece exercícios nos quais haverá uma malha quadrada com alguns quadrados
hachurados. Cada quadrado tem uma área especificada em uma unidade derivada do
metro e o aluno deverá contar a quantidade de quadrados para dizer a área da
figura.

Na importação do programa, há duas variáveis de controle. A primeira diz a área
máxima a ser calculada, a segunda diz a área máxima de cada quadradinho do
desenho.

Perímetro de quadradinhos
"""""""""""""""""""""""""

Oferece exercícios nos quais haverá uma malha quadrada com alguns quadrados
hachurados. Cada quadrado tem uma área especificada em uma unidade derivada do
metro e o aluno deverá contar a quantidade de lados destacados para dizer o
perímetro da figura.

Na importação do programa, há duas variáveis de controle. A primeira diz o
perímetro máximo a ser calculado, a segunda diz a área máxima de cada
quadradinho do desenho.

.. note::

   No caso de perímetros, a área é dada numa sequência de quadrados perfeitos
   (1, 4, 9, etc). Assim o lado de cada quadrado que compõe a imagem é inteiro.

Volume de poliedros
"""""""""""""""""""

Oferece exercícios nos quais são dadas 3 dimensões (largura, altura e
profundidade) afim de calcular o volume do prisma retangular composto por elas.

Na importação do programa há duas variáveis de controle: a primeira entre quais
valores estará a maior dimensão dada e a segunda diz entre quais valores está a
menor dimensão.

.. note::

   O layout deste tipo de exercício sofrerá melhorias: incluirá uma imagem
   representativa do prisma retangular.

Comparação de frações
"""""""""""""""""""""

Oferece exercícios nos quais são dadas 2 frações e pergunta-se se elas são
equivalentes ou qual delas é maior ou menor que a outra.

Na importação do programa há duas variáveis de controle: a primeira diz o valor
mínimo aceito para numerador ou denominador das frações e a segunda controla o
valor máximo.

Frações equivalentes
""""""""""""""""""""

Oferece exercícios nos quais são dadas 2 frações, uma delas sem denominador. O
objetivo do aluno é dizer qual é este denominador de forma que as duas frações
sejam equivalentes.

Na importação do programa há duas variáveis de controle: a primeira diz o valor
mínimo aceito para numerador ou denominador das frações e a segunda controla o
valor máximo.

Frações irredutíveis
""""""""""""""""""""

Oferece exercícios nos quais é dada 1 fração e em que o aluno deve dizer a
simplificação irredutível correspondente a tal fração.

Na importação do programa há duas variáveis de controle: a primeira diz o valor
mínimo aceito para numerador ou denominador das frações e a segunda controla o
valor máximo.

Escolha da fração irredutível
"""""""""""""""""""""""""""""

Diferente do tipo de exercício *Frações irredutíveis*, ao invés de pedir a
fração exata que seja a simplificação da fração data, oferece-se 5 frações
sendo uma delas a correta. O aluno deve escolher o resultado correto.

Na importação do programa há duas variáveis de controle: a primeira diz o valor
mínimo aceito para numerador ou denominador das frações e a segunda controla o
valor máximo.

Fração de porcentagem
"""""""""""""""""""""

É dada uma grade de 10x10 com parte desta grade preenchida. O aluno deverá
contar o número de quadrados e indicar qual a fração correspondente a tal
porcentagem gráfica.

Fração para porcentagem
"""""""""""""""""""""""

Exercício de múltipla escolha com uma única alternativa correta. Dada uma
fração, o aluno deverá dizer a porcentagem correspondente.

Porcentagem para fração
"""""""""""""""""""""""

Exercício contrário ao de *Fração para porcentagem*. Nele, o aluno tem uma
porcentagem e deve dizer a fração correspondente.

Adição e subtração de frações de mesma base
"""""""""""""""""""""""""""""""""""""""""""

Oferece operações de soma ou subtração de frações, tendo estas a mesma base,
num layout adequado para resposta.

Tem 2 variáveis de controle. A primeira controla o valor máximo do dividendo de
cada fração e a segunda controla o valor da base.

Assim se o filtro 1 está entre 5 e 15 e o filtro2 entre 10 e 12, verá frações
como 5/10, 5/12 mas não 5/9 ou 4/12...

Sequencia de execução de exercício
----------------------------------

Como é sabido, cada exercício pode ter diversas respostas (como uma conta de
soma, que tem os dígitos da resposta e do apoio). Estes campos serão mostrados
conforme alimentados (de forma a oferecer um preenchimento guiado).

Para que isso seja possível, cada tipo de resposta precisa informar o próximo
tipo de resposta da sequencia. Este mapeamento será transcrito em atributos
`tabindex` nos campos de preenchimento. Este atributo é constante do protocolo
HTML e será respeitado pelos navegadores quando usa-se a tecla TAB ou
SHIFT+TAB.

Por exemplo, numa soma, o campo de resultado (que representa os dígitos da
resposta) sabe que o próximo campo é o apoio e o apoio sabe que o próximo é o
resultado.

.. _auditoria:

Auditoria de programas
----------------------

Em algumas situações, mais do que executar alguns exercícios específicos, é
útil executar um programa como um todo afim de poder descobrir se ele está
modelado adequadamente, se os dias tem níveis de dificuldade consistentes entre
outros.

Para realizar uma auditoria, no painel administrativo, crie um cliente e seja
gerente deste cliente.

Após isso, ainda no painel administrativo, na seção de **contratos**, crie um
contrato e crie uma turma neste contrato. Seja professor e aluno dela.

Por fim, inicie a turma através do painel administrativo criando uma nova
**aplicação de programa** para ela. Só poderá criar aplicação de programas para
turmas que estejam em instituições das quais é gerente, por isso é importante
ter feito este passo anteriormente.

Não há necessidade de indicar a sequencia de módulos do programa, basta indicar
turma, programa e data de fim, que deve ser uma data futura longínqua o
suficiente para o programa caber no período especificado.

Salve e continue editando. Após isso, clique no botão *Auditoria*, presente no
canto superior direito da tela. Verá então uma lista de dias previstos no
programa e poderá clicar no link em cada linha da coluna exercícios para
responder os exercícios aquele dia.

.. note::

   Uma vez exauridos os exercícios de um dia, ele estará encerrado e não poderá
   ser refeito, a não ser que uma nova aplicação de programa seja criada.
