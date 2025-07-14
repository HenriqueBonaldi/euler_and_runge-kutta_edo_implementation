import numpy as np
import math
import matplotlib.pyplot as plt
#from google.colab import files

#PVI
#(0,2)

#vetores que armazenam apenas o y(4)
y4Quarta= np.array([0 for i in range(8)], dtype=float)
y4Segunda= np.array([0 for i in range(8)], dtype=float)

#vetores para reorganizar os valores obtidos a fim de apresentalos em ordem decrescente de passo, 
y4BQuarta= np.array([0 for i in range(8)], dtype=float)
y4BSegunda= np.array([0 for i in range(8)], dtype=float)

erro4 = np.array([0 for i in range(8)], dtype=float)
erro2 = np.array([0 for i in range(8)], dtype=float)

EC4 = np.array([0 for i in range(8)], dtype=float)
EC2 = np.array([0 for i in range(8)], dtype=float)

passoOrganizado = np.array([0 for i in range(8)], dtype=float)

yQuartaA = np.array([0 for i in range(9)], dtype=float)
yQuartaA[0]=2
ySegundaA = np.array([0 for i in range(9)], dtype=float)
ySegundaA[0]=2

#vetor de passo
passo = np.array([0 for i in range(8)], dtype=float)
passo[0]=0.5
passo[1]=2
passo[2]=1
passo[3]=0.8
passo[4]=0.4
passo[5]=0.2
passo[6]=0.1
passo[7]=0.01

#numero de armazenamentos dos valores de y dado por 4/passo[i]+1
indexParameter= np.array([0 for i in range(8)], dtype=int)
indexParameter[0]=9
indexParameter[1]=3
indexParameter[2]=5
indexParameter[3]=6
indexParameter[4]=11
indexParameter[5]=21
indexParameter[6]=41
indexParameter[7]=401

k=0.0
k1=0.0
k2=0.0
k3=0.0
k4=0.0

def f(xi=float,yi=float):
  k=4*pow(math.e,(0.8*xi))-0.5*yi
  return k

#iterando passos
for i in range(8):

  #indexParameter= int(4/passo[i]+1) fonte de erro: solucao, vetor de indices
  index=indexParameter[i]

  #vetores para armazenar temporariamente todos os valores de y(x)
  yQuarta = np.array([0 for j in range(index)], dtype=float)
  yQuarta[0]=2
  ySegunda = np.array([0 for j in range(index)], dtype=float)
  ySegunda[0]=2

  #metodo quarta ordem
  xParameter=0 #indice para controlar elementos de vetores
  x=0.0
  #while (x<4): fonte de erro
  while (x<(4-passo[i]+0.0001)):
    
    #garante o indice correto do vetor Y para indexacao com base no valor X que esta sendo analisado: x=0 -> y[0] // x=3.5 -> y[7] passo = 0.5 // x=3.5 -> y[35] passo = 0.1 

    k1=f(x,yQuarta[xParameter])
    k2=f((x+passo[i]/2),(yQuarta[xParameter]+passo[i]*0.5*k1))
    k3=f((x+passo[i]/2),(yQuarta[xParameter]+passo[i]*0.5*k2))
    k4=f((x+passo[i]),(yQuarta[xParameter]+passo[i]*k3))

    yQuarta[xParameter+1]=yQuarta[xParameter]+(1/6)*(k1+2*k2+2*k3+k4)*passo[i]
    
    x+=passo[i]

    if (i==0): #se o passo == 0.5, vamos guardar todos os valores para fazer os graficos da letra A
      yQuartaA[xParameter+1]=yQuarta[xParameter+1]
      y4Quarta[i]=yQuarta[xParameter+1]

    xParameter+=1

  #final do loop while quarta ordem - armazenar y(4)
  y4Quarta[i]=yQuarta[xParameter]  


  #metodo euler aperfeicoado
  xParameter=0
  x=0.0
  while (x<(4-passo[i]+0.0001)):

    k1=f(x,ySegunda[xParameter])
    k2=f((x+passo[i]),(ySegunda[xParameter]+passo[i]*k1))

    ySegunda[xParameter+1]=ySegunda[xParameter]+passo[i]*0.5*(k1+k2)

    x+=passo[i]

    if (i==0): #se o passo == 0.5, vamos guardar todos os valores para fazer os graficos
      ySegundaA[xParameter+1]=ySegunda[xParameter+1]
      y4Segunda[i]=ySegunda[xParameter+1]

    xParameter+=1

  #final do loop while segunda ordem - armazenar y(4)  
  y4Segunda[i]=ySegunda[xParameter]

print("Quarta Ordem - letra a -> y(x) para construcao de grafico")
print(yQuartaA)

print("Euler Aperfeicoado - letra a -> y(x) para construcao de grafico")
print(ySegundaA)

for i in range (3):
  y4BQuarta[i]=y4Quarta[i+1]
  y4BSegunda[i]=y4Segunda[i+1]
for i in range (4):
  y4BQuarta[i+4]=y4Quarta[i+4]
  y4BSegunda[i+4]=y4Segunda[i+4]
y4BQuarta[3]=y4Quarta[0]
y4BSegunda[3]=y4Segunda[0]

for i in range (3):
  passoOrganizado[i]=passo[i+1]
for i in range (4):
  passoOrganizado[i+4]=passo[i+4]
passoOrganizado[3]=passo[0]


print("Quarta Ordem - letra b")
print(y4BQuarta)

print("Euler Aperfeicoado - letra b")
print(y4BSegunda)

for k in range (8):
  erro4[k]=abs((75.33896-y4BQuarta[k])/75.33896)
  erro2[k]=abs((75.33896-y4BSegunda[k])/75.33896)

  EC4[k]=4*4/passoOrganizado[k]
  EC2[k]=2*4/passoOrganizado[k]
  
print("Erro Ordem 4 = ",erro4)
print("Esforco Computacional 4 = ",EC4)
print("Erro Ordem 2 = ",erro2)
print("Esforco Computacional 2 = ",EC2)


eixoH = np.linspace(0,4,9)

a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
plt.plot(eixoH, yQuartaA, 'r-', label = 'R-K Quarta Ordem')
plt.plot(eixoH, ySegundaA, 'b-', label = 'R-K Segunda Ordem')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Solucao EDO - 1 Ordem')
fig.savefig('EDO.png')
#files.download('EDO.png')
plt.show()

eixoH = np.linspace(0,2,8)

a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
plt.plot(passoOrganizado, erro4, 'r-', label = 'R-K Quarta Ordem')
plt.plot(passoOrganizado, erro2, 'b-', label = 'R-K Segunda Ordem')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Passo')
plt.ylabel('Erro')
plt.title('Erro x Passo')
fig.savefig('ErroPasso.png')
#files.download('ErroPasso.png')
plt.show()

a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
plt.plot(passoOrganizado, EC4, 'r-', label = 'R-K Quarta Ordem')
plt.plot(passoOrganizado, EC2, 'b-', label = 'R-K Segunda Ordem')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel('Passo')
plt.ylabel('Esforco Computacional')
plt.title('Esforco Computacional x Passo')
fig.savefig('EsforcoPasso.png')
#files.download('EsforcoPasso.png')
plt.show()