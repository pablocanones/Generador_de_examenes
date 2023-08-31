import random
from operator import mul
from functools import reduce
import math
import datetime
'''
n = cantidad de apartados en el ejercicio
seed = semilla aleatoria
dificultad = de 1 a 5
'''

'''
ejercicio para calcular el mínimo común múltiplo y el máximo común divisor de 2 números
n: Cantidad de apartados.
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5
debug: para ver la factorización de los números

La función genera dos números con unos cuantos factores y otros no comunes.
La cantidad de no comunes puede ser cero
Puede usar tantos 2, 3, 5 como quiera pero sólo un 7, 11, 13
La dificultad incrementa la cantidad de primos disponibles y la cantidad de factores en los números.
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
        solucion += f'$.\n\nMCD$({num1},{num2})'
        primero = True
        if len(comunes)>0:
            solucion+=' = '
        if len(comunes)==1:
            solucion+=f'{comunes[0]}$.\n\n'
        else:
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
            solucion += f' ={math.gcd(num1,num2)}$.\n\n'
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
    return enunciado,solucion,generados

'''
ejercicio para calcular el mínimo común múltiplo y el máximo común divisor de 3 números
n: Cantidad de apartados.
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5
debug: para ver la factorización de los números

La función genera tres números con unos cuantos factores y otros no comunes.
La cantidad de no comunes puede ser cero
Puede usar tantos 2, 3, 5 como quiera pero sólo un 7, 11, 13
La dificultad incrementa la cantidad de primos disponibles y la cantidad de factores en los números.
'''
def mcd_mcm_3(n = 1, seed = None, dificultad = 3,debug = False):
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
        #factores comunes a los tres
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
        no_comun3 = []
        #posibilidad de desviación en la cantidad de factores en uno de los números
        desviacion = random.randint(0,1)
        
        while min(len(no_comun1)-desviacion,len(no_comun2),len(no_comun3)) < max_factor:
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
            elif p in no_comun3 and len(no_comun3)< max_factor:
                no_comun3.append(p)
            #si no ha salido para ninguno
            elif p not in no_comun1 and p not in no_comun2 and p not in no_comun3:
                #dárselo al que tiene menos longitud
                if len(no_comun1) <= min(len(no_comun2),len(no_comun3)):
                    no_comun1.append(p)
                elif len(no_comun2) <= min(len(no_comun1),len(no_comun3)):
                    no_comun2.append(p)
                else:
                    no_comun3.append(p)

        #fabricar los dos números
        if len(comunes) == 0 :
            num1 = reduce(mul, no_comun1)
            num2 = reduce(mul, no_comun2)
            num3 = reduce(mul, no_comun3)
        else:
            num1 = reduce(mul, comunes)*reduce(mul, no_comun1)
            num2 = reduce(mul, comunes)*reduce(mul, no_comun2)
            num3 = reduce(mul, comunes)*reduce(mul, no_comun3)
        #comprobar que no se han generado los mismos de antes
        resumen = sorted([num1,num2,num3])
        if resumen in generados:
            continue
        else:
            generados.append(resumen)
            apartado+=1

        #fabricar el enunciado
        enunciado += f'\\task $({num1},{num2},{num3})$.\n'
        
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
        #tercer número
        factor3 = no_comun3 + comunes
        solucion += f'$.\n\n ${num3}='
        primero = True
        for i in primos:
            k = factor3.count(i)
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
        solucion += f'$.\n\nMCD$({num1},{num2},{num3})'
        primero = True
        if len(comunes)>0:
            solucion+=' = '
        
        if len(comunes)==1:
            solucion+=f'{comunes[0]}$.\n\n'
        else:
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
            solucion += f'={math.gcd(num1,num2,num3)}$.\n\n'
        solucion += f'mcm$({num1},{num2},{num3}) = '
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
        solucion += f' = {math.lcm(num1,num2,num3)}$.\n'
        if debug:
            print(f'{num1} {factor1}, {num2} {factor2}, {num3} {factor3}. MCD: {math.gcd(num1,num2,num3)}, mcm: {math.lcm(num1,num2,num3)}')
     
    enunciado += '\\end{tasks}'
    solucion += '\\end{tasks}'
    return enunciado,solucion,generados

'''
problema de mínimos comunes múltiplos
fijo: si se desea que todos los problemas usen el mismo enunciado (toma el día como generador)
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5
debug: para ver la factorización de los números

La función genera un problema sobre mínimo común múltiplo con distintos enunciados
Puede usar tantos 2, 3 como quiera pero sólo un 5, 7, 11, 13
'''
def Problema_mcm(fijo = False, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
      
    primos = [2,3,5,7,11,13]
    #basado en el nivel de dificultad, creamos un conjunto de primos disponibles
    primos = primos[:max(2,int(len(primos)*math.log(dificultad,5)))]

    #cantidad de factores totales
    max_factor = 6*dificultad//5
    #cantidad de factores comunes
    max_comunes = max_factor-1
    #restar la cantidad de comunes
    max_factor -= max(1,max_comunes)
    #factores comunes a los dos
    comunes = []
    primo_grande = False
    while len(comunes) < max_comunes:
        p = random.choice(primos)
        #sólo permitir un primo mayor o igual a 5
        if p in primos[2:]:
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
        #sólo permitir un primo mayor o igual a 5
        if p in primos[2:]:
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

    #fabricar el enunciado
    n_enunciados = 5
    if fijo:
        tipo = datetime.date.today().toordinal() % n_enunciados
    else:
        tipo = random.randint(0,n_enunciados-1)

    if tipo == 0:
        enunciado = 'Alicia y Bob están corriendo un circuito circular por la montaña. '+\
                    'Han salido los dos a la vez pero cada uno corre a una velocidad distinta. '+\
                    f'Alicia da una vuelta al circuito cada {num1} minutos, mientras que Bob da '+\
                    f'una vuelta cada {num2} minutos. '+\
                    '¿Cuánto tiempo pasarás hasta que los dos vuelvan a encontrarse en la línea de salida?'
        solucion = 'Alicia y Bob tardan tiempos distintos en dar una vuelta pero, si corren el tiempo suficiente, '+\
                   'en algún momento volverán a pasar por la línea de salida al mismo tiempo. Necesitamos encontrar '+\
                   f'un número que sea múltiplo a la vez de {num1} y de {num2}. Ese número es el mínimo común múltiplo.\n\n'
    elif tipo == 1:
        enunciado = 'Dos satélites orbitan alrededor de la Tierra, de vez en cuando, los dos satélites pasan al mismo '+\
                    'tiempo sobre España pero cada uno tiene una velocidad distinta. '+\
                    f'El satélite A completa una vuelta a la Tierra cada {num1} horas, mientras que el satélite B '+\
                    f'tarda {num2} horas en completar la órbita. '+\
                    '¿Cada cuánto tiempo tenemos a los dos satélites sobre España?'
        solucion = 'Cada satélite tarda un tiempo distinto en completar la órbita pero, si dan las suficientes vueltas, '+\
                   'en algún momento volverán a pasar por España al mismo tiempo. Necesitamos encontrar '+\
                   f'un número que sea múltiplo a la vez de {num1} y de {num2}. Ese número es el mínimo común múltiplo.\n\n'
    elif tipo == 2:
        enunciado = 'Alicia y Bob están realizando un tratamiento médico que requiere visitas periódicas a la consulta. '+\
                    'Empezaron el tratamiento al mismo tiempo pero cada uno tiene un periodo de visitas distinto. '+\
                    f'Alicia tiene revisiones médicas cada {num1} días, mientras que Bob tiene revisiones '+\
                    f'cada {num2} días. '+\
                    '¿Cada cuántos días se encuentran Alicia y Bob en la consulta del médico?'
        solucion = 'Alicia y Bob tardan tiempos distintos en volver a la consulta pero, si pasa el tiempo suficiente, '+\
                   'en algún momento coincidirán en la consulta. Necesitamos encontrar '+\
                   f'un número que sea múltiplo a la vez de {num1} y de {num2}. Ese número es el mínimo común múltiplo.\n\n'
    elif tipo == 3:
        enunciado = 'Alicia y Bob realizan la colada en el mismo local de lavadoras. '+\
                    'Empezaron a ir a este local al mismo tiempo pero cada uno hace la colada con una frecuencia distinta. '+\
                    f'Alicia hace la colada cada {num1} días, mientras que Bob hace la colada '+\
                    f'cada {num2} días. '+\
                    '¿Cada cuántos días se encuentran Alicia y Bob en el local de lavadoras?'
        solucion = 'Alicia y Bob tardan tiempos distintos en hacer la colada pero, si pasa el tiempo suficiente, '+\
                   'en algún momento coincidirán en el local de lavadoras. Necesitamos encontrar '+\
                   f'un número que sea múltiplo a la vez de {num1} y de {num2}. Ese número es el mínimo común múltiplo.\n\n'
    elif tipo == 4:
        enunciado = 'Cierta máquina de una fábrica utiliza unas piezas que se desgastan con frecuencia y deben ser cambiadas. '+\
                    'Las piezas fueron instaladas el mismo día pero cada una se rompe con una frecuencia distinta. '+\
                    f'La pieza A se rompe cada {num1} días, mientras que la pieza B se rompe '+\
                    f'cada {num2} días. '+\
                    '¿Cada cuántos días hay que cambiar las dos piezas a la vez?'
        solucion = 'Las dos piezas se rompen con frecuencias distintas pero, si pasa el tiempo suficiente, '+\
                   'en algún momento coincidirán el momento de rotura. Necesitamos encontrar '+\
                   f'un número que sea múltiplo a la vez de {num1} y de {num2}. Ese número es el mínimo común múltiplo.\n\n'

    #primer número
    factor1 = no_comun1 + comunes
    solucion += f'De un lado tenemos ${num1}='
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
    solucion += f'$ y de otro tenemos ${num2}='
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
    solucion += f'$. Entonces, mcm$({num1},{num2}) = '
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
    solucion += f' = {math.lcm(num1,num2)}$.\n\n'

    if tipo == 0:
        solucion += f'Alicia y Bob se encontrarán tras ${math.lcm(num1,num2)}$ minutos.'
    elif tipo == 1:
        solucion += f'Los satélites se encontrarán sobre España tras ${math.lcm(num1,num2)}$ horas.'
    elif tipo == 2:
        solucion += f'Alicia y Bob se encontrarán tras ${math.lcm(num1,num2)}$ días.'
    elif tipo == 3:
        solucion += f'Alicia y Bob se encontrarán tras ${math.lcm(num1,num2)}$ días.'
    elif tipo == 4:
        solucion += f'Las dos piezas se romperán a la vez tras ${math.lcm(num1,num2)}$ días.'

    if debug:
        print(f'{num1} {factor1}, {num2} {factor2}. MCD: {math.gcd(num1,num2)}, mcm: {math.lcm(num1,num2)}')
     
    return enunciado,solucion,[num1,num2]

'''
ejercicio para calcular b dado a, mcm(a,b) y mcd(a,b)
n: Cantidad de apartados.
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5
debug: para ver la factorización de los números

La función genera dos números con unos cuantos factores y otros no comunes.
La cantidad de no comunes puede ser cero
Puede usar tantos 2, 3, 5 como quiera pero sólo un 7, 11, 13
La dificultad incrementa la cantidad de primos disponibles y la cantidad de factores en los números.
'''
def mcd_mcm(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    
    primos = [2,3,5,7,11,13]
    #basado en el nivel de dificultad, creamos un conjunto de primos disponibles
    primos = primos[:max(2,int(len(primos)*math.log(dificultad,5)))]

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
    
    #fabricar el enunciado
    enunciado = f'Tenemos un número $a={num1}$ y uno $b$ desconocido. '+\
            f'De estos dos números sabemos que MCD$(a,b)={math.gcd(num1,num2)}$ y '+\
            f'y que que mcm$(a,b)={math.lcm(num1,num2)}$. Calcula el valor de $b$.'

    #fabricar solución
    solucion = 'Para encontrar $b$ vamos a factorizar $a$, MCD$(a,b)$ y mcm$(a,b)$.\n\\begin{itemize}\n'
    #primer número
    factor1 = no_comun1 + comunes
    solucion += f'\\item $a={num1}='
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
    solucion += '$.\n'
    #mcd
    solucion += f'\\item MCD$(a,b) = {math.gcd(num1,num2)} = '
    primero = True
    if len(comunes)==0:
        solucion+='1'
    if len(comunes)==1:
        solucion+=f'{comunes[0]}'
    else:
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
    solucion += '$.\n'
    #mcm
    solucion += f'\\item mcm$({num1},{num2}) = '
    todos = comunes + no_comun1 + no_comun2
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
    solucion += f' = {math.lcm(num1,num2)}$.\n\\end{{itemize}}\n'

    solucion += 

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
    solucion += f'$.\n\nmcd$({num1},{num2})'
    primero = True
    if len(comunes)>0:
        solucion+=' = '
    if len(comunes)==1:
        solucion+=f'{comunes[0]}$.\n\n'
    else:
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
        solucion += f' ={math.gcd(num1,num2)}$.\n\n'
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

    solucion += 'Otra manera de encontrar $b$ es usar la propiedad $\text{MCD}(a,b)\cdot\text{mcm}(a,b)=a\cdot b. Entonces '+\
                '$$b = \frac\text{MCD}(a,b)\cdot\text{mcm}(a,b)}{a}='+\
                f'\frac{{ {math.gcd(num1,num2)} \cdot {math.lcm(num1,num2)} }}{{ {num1} }}'+\
                f'=\frac{{ {num1*num2} }}{{ {num1} }} = {num1}.$$'
    if debug:
        print(f'{num1} {factor1}, {num2} {factor2}. MCD: {math.gcd(num1,num2)}, mcm: {math.lcm(num1,num2)}')
     
    enunciado += '\\end{tasks}'
    solucion += '\\end{tasks}'
    return enunciado,solucion,generados
