import math
import random

#objeto cidade
class ponto:
    def __init__(self, id, x, y):
        self.x = float(x)
        self.y = float(y)
        self.id = int(id)

example = [
    (1, 37.0, 52.0),
    (2, 49.0, 49.0),
    (3, 52.0, 64.0),
    (4, 20.0, 26.0),
    (5, 40.0, 30.0),
    (6, 21.0, 47.0),
    (7, 17.0, 63.0),
    (8, 31.0, 62.0),
    (9, 52.0, 33.0),
    (10, 51.0, 21.0),
    (11, 42.0, 41.0),
    (12, 31.0, 32.0),
    (13, 5.0, 25.0),
    (14, 12.0, 42.0),
    (15, 36.0, 16.0),
    (16, 52.0, 41.0),
    (17, 27.0, 23.0),
    (18, 17.0, 33.0),
    (19, 13.0, 13.0),
    (20, 57.0, 58.0),
    (21, 62.0, 42.0),
    (22, 42.0, 57.0),
    (23, 16.0, 57.0),
    (24, 8.0, 52.0),
    (25, 7.0, 38.0),
    (26, 27.0, 68.0),
    (27, 30.0, 48.0),
    (28, 43.0, 67.0),
    (29, 58.0, 48.0),
    (30, 58.0, 27.0),
    (31, 37.0, 69.0),
    (32, 38.0, 46.0),
    (33, 46.0, 10.0),
    (34, 61.0, 33.0),
    (35, 62.0, 63.0),
    (36, 63.0, 69.0),
    (37, 32.0, 22.0),
    (38, 45.0, 35.0),
    (39, 59.0, 15.0),
    (40, 5.0, 6.0),
    (41, 10.0, 17.0),
    (42, 21.0, 10.0),
    (43, 5.0, 64.0),
    (44, 30.0, 15.0),
    (45, 39.0, 10.0),
    (46, 32.0, 39.0),
    (47, 25.0, 32.0),
    (48, 25.0, 55.0),
    (49, 48.0, 28.0),
    (50, 56.0, 37.0),
    (51, 30.0, 40.0)
]

def gerador_de_lista_de_objetos_pontos(lista):
    data = []
    for item in lista:
        id, x, y = item
        data.append(ponto(id=id, x=x, y=y))
    return data

#fitness de uma lista de pontos (consideramos a ordem dos pontos na lista como a ordem de conexao entre cada um)
def fitness(lista_de_pontos_no_mapa):
    
    custo_total = 0.0
    num_pontos = len(lista_de_pontos_no_mapa)
    
    for i in range(1, num_pontos):
        ponto_atual = lista_de_pontos_no_mapa[i-1]
        proximo_ponto = lista_de_pontos_no_mapa[(i)]
        custo_total += calcular_distancia(ponto_atual, proximo_ponto)
    custo_total += calcular_distancia(lista_de_pontos_no_mapa[len(lista_de_pontos_no_mapa)-1], lista_de_pontos_no_mapa[0])
        
    return custo_total

def calcular_distancia(p1, p2):
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

#elitismo (recebe uma lista de mapas, ou seja, a posicao 0 conterá uma lista de pontos). Por isso utilizamos a funcao fitness para calculo de custo em cada iteracao
# exemplo de estrutura que sera recebida: (ponto = objeto)
# [
#    [ponto, ponto, ponto...],
#    [ponto, ponto, ponto...],
#    [ponto, ponto, ponto...]
#    ...
#]
def selecao(lista_de_direcoes):
    custo = 9999999999999999999999999999.00
    selecionado = []
    for i in (lista_de_direcoes):
        parametro = fitness(i)
        if parametro < custo:
            selecionado = i
            custo = parametro
    return selecionado

#retorna um caminho (lista de pontos) aleatorio
def selecao_torneio(lista_de_direcoes):
    return lista_de_direcoes[random.randint(0, len(lista_de_direcoes))-1]

#escolhe os dois melhores
def selecao_dois_melhores(lista_de_direcoes):
    lista_de_direcoes_auxiliar = lista_de_direcoes.copy()

    selecionado1 = selecao(lista_de_direcoes_auxiliar)
    lista_de_direcoes_auxiliar.remove(selecionado1)

    selecionado2 = selecao(lista_de_direcoes_auxiliar)
    lista_de_direcoes_auxiliar.remove(selecionado2)
    
    return selecionado1, selecionado2

#recebe uma lista de objetos e retorna uma nova ordem (lembrando que essa ordem esta ligada ao CAMINHO que esta sendo percorrido)
#exemplo de recebimento:
# [ponto, ponto, ponto...]
def geracao_de_caminho_randomico(lista_de_pontos):
    nova_ordem = lista_de_pontos[:]  # Cria uma cópia da lista original
    random.shuffle(nova_ordem)  # Embaralha a nova lista
    return nova_ordem

#mutacao tipo SWAP
def mutate(lista_de_pontos):
    # Seleciona aleatoriamente um índice válido na lista
    indice_aleatorio = random.randint(0, len(lista_de_pontos) - 1)
    
    # Seleciona aleatoriamente outro índice diferente do primeiro
    novo_indice_aleatorio = random.randint(0, len(lista_de_pontos) - 1)
    while novo_indice_aleatorio == indice_aleatorio:
        novo_indice_aleatorio = random.randint(0, len(lista_de_pontos) - 1)
    
    # Troca os pontos de posição
    lista_de_pontos[indice_aleatorio], lista_de_pontos[novo_indice_aleatorio] = lista_de_pontos[novo_indice_aleatorio], lista_de_pontos[indice_aleatorio]

    return lista_de_pontos
    #retorna [ponto, ponto, ponto...]

#cruzamento tipo single-point -> reproducao -> recebe duas listas de pontos, e partir disso gera um filho (a escolha do corte é randomica)
def crossover(lista_de_pontos1, lista_de_pontos2):
    nova_lista = []
    random_number = random.randint(0, len(lista_de_pontos2))
    for i in range(random_number):
        nova_lista.append(lista_de_pontos1[i])

    for i in range(random_number, len(lista_de_pontos2)):
        nova_lista.append(lista_de_pontos2[i])

    return nova_lista

#cruzamento tipo double-point 
def crossover_doublepoint(lista_de_pontos1, lista_de_pontos2):
    nova_lista = []
    
    # Seleciona aleatoriamente dois pontos de corte
    corte1 = random.randint(0, len(lista_de_pontos1) - 1)
    corte2 = random.randint(corte1 + 1, len(lista_de_pontos1))

    # Troca os segmentos entre os dois pontos de corte
    nova_lista.extend(lista_de_pontos1[:corte1])
    nova_lista.extend(lista_de_pontos2[corte1:corte2])
    nova_lista.extend(lista_de_pontos1[corte2:])
    
    return nova_lista
    
#cruzamento tipo random, utilizando set para nao ter pontos duplicados
def crossover_custom(lista_de_pontos1, lista_de_pontos2):
    nova_lista = []
    nova_lista = set(nova_lista)

    random_number = random.randint(1, 50)

    for i in range(0, random_number):
        nova_lista.add(lista_de_pontos1[i])

    for i in range(0, len(lista_de_pontos2)):
        if nova_lista.__contains__(lista_de_pontos2[i]):
            continue
        else:
            nova_lista.add(lista_de_pontos2[i])

    nova_lista = list(nova_lista)
    return nova_lista

def crossover_perfect(lista_de_pontos1, lista_de_pontos2):
    offspring = []

    # Step 1: Choose initial city randomly
    initial_city = random.choice(lista_de_pontos1)
    offspring.append(initial_city)

    visited_cities = set([initial_city.id])

    while len(offspring) < len(lista_de_pontos1):
        current_city = offspring[-1]
        index1 = lista_de_pontos1.index(current_city)
        index2 = lista_de_pontos2.index(current_city)

        # Find the nearest unvisited city
        min_distance = float('inf')
        nearest_city = None
        for index, lista_de_pontos in [(index1, lista_de_pontos1), (index2, lista_de_pontos2)]:
            for i in range(1, len(lista_de_pontos)):
                next_city = lista_de_pontos[(index + i) % len(lista_de_pontos)]
                if next_city.id not in visited_cities:
                    distance = calcular_distancia(current_city, next_city)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_city = next_city

        # Add the nearest unvisited city to offspring
        offspring.append(nearest_city)
        visited_cities.add(nearest_city.id)

    return offspring


def distinct_check(lista_de_pontos, valor_soma):
    soma = 0

    for i in range(len(lista_de_pontos)):
        soma += lista_de_pontos[i].id
    
    if soma == valor_soma:
        return True
    return False

def fitness_threshold(fn_fitness, fn_thres, population):
    if not fn_thres:
        return None

    fittest_individual = max(population, key=fn_fitness)
    if fn_fitness(fittest_individual) >= fn_thres:
        return fittest_individual

    return None

def algoritmo_genetico_completo(caminhos_randomicos_quantidade, numero_geracoes, rate_de_mutacao, data, fn_thres=None):
    # Antes de tudo, vamos criar uma lista com objetos pontos, que foi a lista teste passada. 
    # O parametro 'data' é exatamente uma lista de pontos (NAO objetos)
    data_sample = gerador_de_lista_de_objetos_pontos(data)

    # Criar uma lista de tamanho caminhos_randomicos_quantidade, contendo listas de pontos, baseado no sample que temos
    data_population = []
    for i in range(caminhos_randomicos_quantidade):
        data_population.append(geracao_de_caminho_randomico(data_sample))

    for i in range(numero_geracoes):
        new_population = []

        for i in range(caminhos_randomicos_quantidade):
            pai = selecao(data_population)
            mae = selecao(data_population)
            crianca = crossover_perfect(pai, mae)

            if random.random() <= rate_de_mutacao: 
                crianca = mutate(crianca)
            
            new_population.append(crianca)

        data_population = new_population

        fittest_individual = fitness_threshold(fitness, fn_thres, data_population)

        if fittest_individual:
            return fittest_individual
        
    return max(data_population, key=fitness)

melhor_solucao = algoritmo_genetico_completo(100, 1000, 0.2, example)

print(fitness(melhor_solucao))
print(distinct_check(melhor_solucao, 1326))