import random
from operator import mul
from functools import reduce
import math
'''
n = cantidad de apartados en el ejercicio
seed = semilla aleatoria
dificultad = de 1 a 5
'''


#ejercicio para calcular el mínimo común múltiplo y el máximo común divisor

'''
ORDENAR LOS NÚMEROS PARA IDENTIFICAR REPETIDOS
'''



def mcd_mcm(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    enunciado = 'Calcula el mínimo común múltiplo y el máximo común divisor'+\
                ' de los siguientes números:\n'
    solucion = enunciado
    enunciado += '\\begin{tasks}(3)\n'
    solucion += '\\begin{tasks}\n'
    
    
    primos = [2,3,5,7,11,13]
    #basado en el nivel de dificultad, creamos un conjunto de primos disponibles
    primos = primos[:max(2,int(len(primos)*math.log(dificultad,5)))]
    generados = []
    apartado = 0
    while apartado < n:
        #cantidad de factores totales
        max_factor = 6*dificultad//5
        #cantidad de factores comunes
        max_comunes = math.ceil(random.randint(0,(max_factor-1)*3)/3)
        #restar la cantidad de comunes
        max_factor -= max(1,max_comunes)
        #factores comunes a los dos
        comunes = []
        primo_grande = False
        while len(comunes) < max_comunes:
            p = random.choice(primos)
            #sólo permitir un primo mayor o igual a 7
            if p in primos[3:]:
                primo_grande = True
                if p in comunes:
                    continue
            else:
                comunes.append(p)
        #factores no comunes
        no_comun1 = []
        no_comun2 = []
        #posibilidad de desviación en la cantidad de factores en uno de los números
        desviacion = random.randint(0,1)
        
        while min(len(no_comun1)-desviacion,len(no_comun2)) < max_factor:
            p = random.choice(primos)
            #sólo permitir un primo mayor o igual a 7
            if p in primos[3:]:
                if primo_grande:#si hay un primo grande en los comunes
                    continue
                primo_grande = True
            #si el factor ya ha salido y los números no son demasiado grandes
            if p in no_comun1 and len(no_comun1)-desviacion< max_factor:
                no_comun1.append(p)
            elif p in no_comun2 and len(no_comun2)< max_factor:
                no_comun2.append(p)
            #si no ha salido para ninguno
            elif p not in no_comun1 and p not in no_comun2:
                #dárselo al que tiene menos longitud
                if len(no_comun1)<=len(no_comun2):
                    no_comun1.append(p)
                else:
                    no_comun2.append(p)

        #fabricar los dos números
        if len(comunes) == 0 :
            num1 = reduce(mul, no_comun1)
            num2 = reduce(mul, no_comun2)
        else:
            num1 = reduce(mul, comunes)*reduce(mul, no_comun1)
            num2 = reduce(mul, comunes)*reduce(mul, no_comun2)
        #comprobar que no se han generado los mismos de antes
        resumen = sorted([num1,num2])
        if resumen in generados:
            continue
        else:
            generados.append(resumen)
            apartado+=1

        #fabricar el enunciado
        enunciado += f'\\task $({num1},{num2})$.\n'
        
        #fabricar solución
        #primer número
        factor1 = no_comun1 + comunes
        solucion += f'\\task ${num1}='
        primero = True
        for i in primos:
            k = factor1.count(i)
            if k > 0:
                if primero:
                    primero = False
                else:
                    solucion += ' \cdot'
                if k == 1:
                    solucion += f' {i}'
                else:
                    solucion += f' {i}^{k}'
        #segundo número
        factor2 = no_comun2 + comunes
        solucion += f'$.\n\n ${num2}='
        primero = True
        for i in primos:
            k = factor2.count(i)
            if k > 0:
                if primero:
                    primero = False
                else:
                    solucion += ' \cdot'
                if k == 1:
                    solucion += f' {i}'
                else:
                    solucion += f' {i}^{k}'
        #solución
        solucion += f'$.\n\nmcd$({num1},{num2}) = '
        primero = True
        for i in primos:
            k = comunes.count(i)
            if k > 0:
                if primero:
                    primero = False
                else:
                    solucion += ' \cdot'
                if k == 1:
                    solucion += f' {i}'
                else:
                    solucion += f' {i}^{k}'
        solucion += f'={math.gcd(num1,num2)}$.\n\n'
        solucion += f'mcm$({num1},{num2}) = '
        todos = comunes + no_comun1+no_comun2
        primero = True
        for i in primos:
            k = todos.count(i)
            if k > 0:
                if primero:
                    primero = False
                else:
                    solucion += ' \cdot'
                if k == 1:
                    solucion += f' {i}'
                else:
                    solucion += f' {i}^{k}'        
        solucion += f' = {math.lcm(num1,num2)}$.\n'
        if debug:
            print(f'{num1} {factor1}, {num2} {factor2}. MCD: {math.gcd(num1,num2)}, mcm: {math.lcm(num1,num2)}')
     
    enunciado += '\\end{tasks}'
    solucion += '\\end{tasks}'
    return enunciado,solucion