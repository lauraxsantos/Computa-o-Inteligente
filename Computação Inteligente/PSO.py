import math
import random
import matplotlib.pyplot as plt
import numpy as np

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


class Particula:
    def __init__(self, dimensoes, limiteMax, limteMin):
        self.posicao = [random.uniform(limteMin, limiteMax) for _ in range(dimensoes)]
        self.velocidade = [random.uniform(-1, 1) for _ in range(dimensoes)]
        self.pbest_posicao = self.posicao.copy()
        self.pbest_valor = float('inf')

    def atualizar_pbest(self, funcao_fitness):
       fitness = funcao_fitness(self.posicao)
       if fitness < self.pbest_valor:
          self.pbest_valor = fitness
          self.pbest_posicao = self.posicao.copy()

    def movimentacao(self):
       self.posicao = [self.posicao[i] + self.velocidade[i] for i in range(len(self.posicao))]

def PSO(funcao, num_particulas, dimensoes, iteracoes, limiteMin, limiteMax, cooperacao, fatorInercia, c1, c2, wMin = 1, wMax = 1):
    gbest_valor = float('inf')
    gbest_posicao = []
    lbest_posicao = []
    enxame = []
    inercia = []
    cognitivo = []
    social = []       
    melhores = []

    for _ in range(dimensoes):
      gbest_posicao.append(random.uniform(limiteMin, limiteMax))
    
    for _ in range(num_particulas):
        enxame.append(Particula(dimensoes, limiteMin, limiteMax))
    
    for particula in (enxame):
       lbest_posicao.append(particula.posicao.copy())
    
    for iteracao in range(iteracoes):
       if(fatorInercia == 'constante'):
            w = 1
       elif (fatorInercia == 'decaimento'):
            w = (wMax - wMin) *((iteracoes - iteracao)/iteracoes) + wMin

       for particula in enxame:
          particula.atualizar_pbest(funcao)

          if cooperacao == 'global':
             if particula.pbest_valor < gbest_valor:
                gbest_valor = particula.pbest_valor
                gbest_posicao = particula.pbest_posicao.copy()
        
       for particula in enxame:
          for i in range(dimensoes):
             inercia.append(w * particula.velocidade[i])
             cognitivo.append(c1 * random.random() * particula.pbest_posicao[i] - particula.posicao[i])
          
          if cooperacao == 'global':
             social= [c2 * random.random() * (gbest_posicao[i] - particula.posicao[i]) for i in range(dimensoes)]
          else:
             if i > 0:
                 left = enxame[i-1]
             else:
                 left = enxame[-1] 

             if i < len(enxame) - 1:
                 right = enxame[i + 1]
             else:
                 right = enxame[0]

             if left.pbest_valor < particula.pbest_valor:
              lbest_posicao[i] = left.pbest_posicao.copy()
             if right.pbest_valor < particula.pbest_valor:
              lbest_posicao[i] = right.pbest_posicao.copy()

             social = [c2 * random.random() * (lbest_posicao[i][d] - particula.posicao[d]) for d in range(dimensoes)]
          particula.velocidade = [inercia[i] + cognitivo[i] + social[i] for i in range(dimensoes)]

          particula.movimentacao()

       if cooperacao == 'local':
           best_lbest_valor = min([p.pbest_valor for p in enxame])
         #   print(f"Iteração {iteracao + 1}: Melhor valor local (Lbest) = {best_lbest_valor}")
           melhores.append(best_lbest_valor)
       else:
         #   print(f"Iteração {iteracao + 1}: Melhor valor global (Gbest) = {gbest_valor}")
           melhores.append(gbest_valor)
    return melhores[-1]

def plot():
   cenario1 = []
   cenario2 = []
   cenario3 = []
   for c in range(30):
      cenario1.append(PSO(rastrigin, 20, 2, 100, -5.12, 5.12, 'global', 'decaimento', 1, 0.8,))
   for c in range(30):
      cenario2.append(PSO(rastrigin, 20, 2, 100, -5.12, 5.12, 'global', 'decaimento', 1, 0.8,))
   for c in range(30):
      cenario3.append(PSO(rastrigin, 20, 2, 100, -5.12, 5.12, 'global', 'decaimento', 1, 0.8,))

   dados = [cenario1, cenario2, cenario3]

   # Criando o boxplot
   plt.figure(figsize=(8, 6))
   plt.boxplot(dados, labels=['Cenário 1', 'Cenário 2', 'Cenário 3'])

   # Adicionando título e rótulos aos eixos
   plt.title('Boxplot de Execuções em Diferentes Cenários', fontsize=14)
   plt.xlabel('Cenários', fontsize=12)
   plt.ylabel('Valores das Execuções', fontsize=12)

   # Mostrando o gráfico
   plt.show()
# PSO(rastrigin, 20, 2, 100, -5.12, 5.12, 'local', 'decaimento', 1, 0.8,)
             
plot()
          