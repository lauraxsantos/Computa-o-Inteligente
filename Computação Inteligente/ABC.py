import random
import math
import matplotlib.pyplot as plt

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


def ABC(funcao=sphere, c=10, cs=10, limiteMin=-1, limiteMax=1, dimensoes=1, L=2):

    empregadas = cs // 2
    observadoras = cs - empregadas

    alimentacao = [[random.uniform(limiteMin, limiteMax) for _ in range(dimensoes)] for _ in range(empregadas)]
    abandono = [0] * empregadas  
    best_abelha = alimentacao[0]
    best_fitness = funcao(best_abelha)
    
    best_fitnesses = []
    
    for iteracao in range(c):
        for i in range(empregadas):
            new_abelha = [alimentacao[i][j] + random.uniform(-1, 1) for j in range(dimensoes)]
            new_abelha = [min(max(new_abelha[j], limiteMin), limiteMax) for j in range(dimensoes)] # puxar
            new_fitness = funcao(new_abelha)
            
            if new_fitness < funcao(alimentacao[i]):
                alimentacao[i] = new_abelha
                abandono[i] = 0
            else:
                abandono[i] += 1

        fitnesses = [funcao(source) for source in alimentacao]
        probabilidades = [1 / (1 + f) for f in fitnesses]  
        total_prob = sum(probabilidades)
        probabilidades = [p / total_prob for p in probabilidades] 

        for _ in range(observadoras):
            selected_index = random.choices(range(empregadas), probabilidades)[0]
            selected_source = alimentacao[selected_index]
            new_abelha = [selected_source[j] + random.uniform(-0.5, 0.5) for j in range(dimensoes)]
            new_abelha = [min(max(new_abelha[j], limiteMin), limiteMax) for j in range(dimensoes)]
            
            if rastrigin(new_abelha) < rastrigin(selected_source):
                alimentacao[selected_index] = new_abelha
                abandono[selected_index] = 0

        for i in range(empregadas):
            if abandono[i] > L:
                alimentacao[i] = [random.uniform(limiteMin, limiteMax) for _ in range(dimensoes)]
                abandono[i] = 0  

        atual_best_source = alimentacao[fitnesses.index(min(fitnesses))]
        atual_best_fitness = min(fitnesses)
        if atual_best_fitness < best_fitness:
            best_fitness = atual_best_fitness
            best_abelha = atual_best_source

        best_fitnesses.append(best_fitness)
    
    return best_abelha, best_fitness, best_fitnesses

best_solucao, best_fitness, best_fitnesses = ABC()

print("Melhor Solução:", best_solucao)
print("Melhor Fitness:", best_fitness)

plt.plot(best_fitnesses)
plt.title('Desempenho do ABC')
plt.xlabel('Iterações')
plt.ylabel('Melhor Fitness')
plt.grid(True)
plt.show()
