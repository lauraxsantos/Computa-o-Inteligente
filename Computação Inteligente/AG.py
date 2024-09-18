import random
import math

def populacaoInicial(intervalo1, intervalo2, quantidade=20, dimensoes=30):
    populacao = []
    for c in range(0, quantidade):     
        populacao.append(criarElemento(dimensoes, intervalo1, intervalo2))
    return populacao

def criarElemento(dimensao, intervalo1, intervalo2):
    elemento = []
    for _ in range(0, dimensao):
        elemento.append(random.uniform(intervalo1,intervalo2))
    return elemento

def sphere(vetor):
  resultado = 0
  
  for i in vetor:
    resultado += i**2
  
  return resultado

def rastrigin(vetor):
  resultado = 0
  
  for i in vetor:
    numero = 2*3.1415*i
    p = (numero/180)*math.pi
    resultado+= (i**2) - (10 * math.cos(p)) + 10
    
  return resultado

def rosenbrock(vetor):
  resultado = 0
  
  for i in range(0,(len(vetor)-1)):
    resultado += 100*(vetor[i+1] - vetor[i]**2)**2 + (vetor[i] - 1)**2
    
  return resultado

def fitness(cromossomo, problema):

    if(problema == 'sphere'):
        return sphere(cromossomo)
    elif(problema == 'rastring'): 
        return rastrigin(cromossomo)
    elif(problema == 'rosenbrock'):
        return rosenbrock(cromossomo)
    
def melhor(populacao, problema):
   return min(populacao, key= lambda individual: fitness(individual, problema))


def roleta(populacao, problema = 'sphere'):
    #minimizar
    probs = []
    fitnesses = []
    for cromossomo in populacao:
        fitnesses.append(fitness(cromossomo, problema))

    totalFitness = sum(fitnesses)
    for cromossomo in populacao:
        probs.append((1 / fitness(cromossomo, problema))/ totalFitness)

    return random.choices(populacao, weights=probs, k=1)[0]

def torneio(populacao, problema = 'sphere'):
    probs = []
    fitnesses = []
    for cromossomo in populacao:
        fitnesses.append(fitness(cromossomo, problema))

    totalFitness = sum(fitnesses)
    for cromossomo in populacao:
        probs.append((1 / fitness(cromossomo, problema))/ totalFitness)
    
    selecionados = random.sample(list(zip(populacao, fitnesses)), 2)
    selecionados.sort(key= lambda x: x[1])
    return selecionados[0][0]


def cruzamento(pai, mae, taxaS, cortes=1):
    taxa = random.random()

    if(taxa >= taxaS):
        return [pai, mae]
    
    if(cortes == 2):
        corte1 = random.randint(1, len(pai) - 2)
        corte2 = random.randint(corte1+1, len(pai) - 1)
        filho1 = pai[:corte1] + mae[corte1:corte2] + pai[corte2:] 
        filho2 = mae[:corte1] + pai[corte1:corte2] + mae[corte2:]
    else:
        corte = random.randint(1, len(pai) - 1)
        filho1 = pai[:corte] + mae[corte:]
        filho2 = mae[:corte] + pai[corte:]

    return filho1, filho2



def mutacao(cromossomo, intervaloMin, intervaloMax, taxaS = 0.1):
    for gene in range(len(cromossomo)):  
        if random.random() < taxaS:
            cromossomo[gene] = random.uniform(intervaloMin, intervaloMax)              
    return cromossomo



def algoritmoGenetico(intervaloMin, intervaloMax, cortes=1, selecao = 'Roleta', taxaMutacao = 0.1, taxaCruzamento = 0.7, funcao = 'sphere', quantidadePop = 20, dimensoes = 30, geracoes=20):
    populacao = populacaoInicial(intervaloMin, intervaloMax, quantidadePop, dimensoes)
    melhores = []
    melhorFit = []

    for geracao in range(geracoes):
        novaPop = []
        cruzamentoLista = []
        mutacaoLista = []

        if(selecao == 'Roleta'):
            while len(novaPop) < quantidadePop:         
                novaPop.append(roleta(populacao, funcao))
        elif(selecao == 'Torneio'):
            while len(novaPop) < quantidadePop:         
                novaPop.append(torneio(populacao, funcao))
        
        for c in range(0, len(novaPop), 2):
            pai = novaPop[c]
            mae = novaPop[c + 1]

            filho, filha = cruzamento(pai, mae, taxaCruzamento, cortes)
            cruzamentoLista.append(filha)
            cruzamentoLista.append(filho)
        
        for c in range(len(cruzamentoLista)):
            m = mutacao(cruzamentoLista[c], intervaloMin, intervaloMax, taxaMutacao)
            mutacaoLista.append(m)

        populacao = mutacaoLista
        melhorElemento = melhor(populacao, funcao)
        melhorFitness = fitness(melhorElemento, funcao)

        melhores.append(melhorElemento)
        melhorFit.append(melhorFitness)

        
        print(f'Geração {geracao + 1} - Melhor Fitness: {melhorFitness}')

    return melhorFitness

algoritmoGenetico(-100, 100, 'Torneio', funcao='rastring')

