# language: pt-br
Funcionalidade: Categorias em baterias de programas podem ter tags para filtrar exercícios

    Afim de segmentar uma lista consolidada de exercícios
    Como administrador do sistema
    Posso especificar tags para categorias que as suportam

    Cenário: Não escolher tags faz todos os exercícios da categoria serem usados
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que existem categorias previamente cadastradas
        Dados os exercícios de "Adição e subtração em ordem 3 termos" (createadditionexpressions) abaixo:
            | Operação  | Resultado | Termos |
            | -1+4-2    | 1         | 3      |
            | 1+3-3     | 1         | 3      |
            | 1+2-4     | -1        | 3      |
        Dado um programa com uma bateria com 3 exercícios de expressões de adição
        Se eu der início ao programa
        Então seu único dia terá os exercícios abaixo:
            | Exercício |
            | -1+4-2    |
            | 1+3-3     |
            | 1+2-4     |

    Cenário: Se definir uma tag e não houver exercícios suficientes, não pode iniciar
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que existem categorias previamente cadastradas
        Dados os exercícios de "Adição e subtração em ordem 3 termos" (createadditionexpressions) abaixo:
            | Operação  | Resultado | Termos |
            | -1+4-2    | 1         | 3      |
            | 1+3-3     | 1         | 3      |
            | 1+2-4     | -1        | 3      |
        Dado um programa com uma bateria com 3 exercícios de expressões de adição
        Dado que esta bateria filtra a tag "inicio-posit"
        Então não poderei iniciar o programa, precisa de 3 exercícios mas só tem 2

    Cenário: Se definir uma tag e houver exercícios suficientes, poderá iniciar
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que existem categorias previamente cadastradas
        Dados os exercícios de "Adição e subtração em ordem 3 termos" (createadditionexpressions) abaixo:
            | Operação  | Resultado | Termos |
            | -1+4-2    | 1         | 3      |
            | 1+3-3     | 1         | 3      |
            | 1+2-4     | -1        | 3      |
        Dado um programa com uma bateria com 2 exercícios de expressões de adição
        Dado que esta bateria filtra a tag "inicio-posit"
        Se eu der início ao programa
        Então seu único dia terá os exercícios abaixo:
            | Exercício |
            | 1+3-3     |
            | 1+2-4     |

    Cenário: Se definir duas tags e não houver exercícios suficientes, não pode iniciar
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que existem categorias previamente cadastradas
        Dados os exercícios de "Adição e subtração em ordem 3 termos" (createadditionexpressions) abaixo:
            | Operação  | Resultado | Termos |
            | -1+4-2    | 1         | 3      |
            | 1+3-3     | 1         | 3      |
            | 1+2-4     | -1        | 3      |
        Dado um programa com uma bateria com 3 exercícios de expressões de adição
        Dado que esta bateria filtra a tag "inicio-posit, result-posit"
        Então não poderei iniciar o programa, precisa de 3 exercícios mas só tem 1

    Cenário: Se definir duas tags e houver exercícios suficientes, poderá iniciar
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que existem categorias previamente cadastradas
        Dados os exercícios de "Adição e subtração em ordem 3 termos" (createadditionexpressions) abaixo:
            | Operação  | Resultado | Termos |
            | -1+4-2    | 1         | 3      |
            | 1+3-3     | 1         | 3      |
            | 1+2-4     | -1        | 3      |
        Dado um programa com uma bateria com 1 exercícios de expressões de adição
        Dado que esta bateria filtra a tag "inicio-posit, result-posit"
        Se eu der início ao programa
        Então seu único dia terá os exercícios abaixo:
            | Exercício |
            | 1+3-3     |
