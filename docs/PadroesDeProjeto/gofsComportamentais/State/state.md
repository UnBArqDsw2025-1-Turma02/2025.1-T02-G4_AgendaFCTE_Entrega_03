# 📝 State Pattern - Introdução e Metodologia

## 📖 **Introdução**

O State Pattern, ou Padrão de Estado, é um tipo de padrão de projeto comportamental que permite que um objeto mude seu comportamento quando seu estado interno é alterado. Embora esse método delegue um comportamento diferente para cada tipo de estado definido, o objeto irá aparentar mudar de classe quando o padrão é alterado.

Esse padrão é indicado em cenários onde um objeto precise variar comportamento dependendo do estado ou quando existem muitas condições que possam tendenciar o mesmo.


## 🔧 **Metodologia**

### 🏗️ Estrutura Básica
O padrão State é composto por três elementos principais:

1. **Contexto**
   Classe que mantém a referência de estado atual e delega as requisições para o estado atual
   

2. **Interface de Estado**
    Estabelece uma interface comum para todos os estados concretos e declara os métodos que representam as ações disponíveis
   

3. **Estados Concretos**
   Implementa o comportamento determinado a um estado específico




| Versão | Data       | Descrição                                                                                         | Autor                                              | Revisor                                        | Comentário do Revisor                          |
| ------ | ---------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |
| 1.1    | 01/06/2025 | Adição do texto introdutório e de metodologia do State                                      | [João Lucas](https://github.com/joaolucas102) |  |  |