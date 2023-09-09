import random
from operator import mul
from functools import reduce
import math
from copy import deepcopy

def operacion_derecha(expresion,i):
    while i<len(expresion) and expresion[i] not in ['+','-','*',':','(']:
            i += 1
    if i==len(expresion):
        return None
    else:
        return expresion[i]

def operacion_izquierda(expresion,i):
    while i>=0 and expresion[i] not in ['+','-','*',':',')']:
            i -= 1
    if i<0:
        return None
    else:
        return expresion[i]

#función para maquetar los paréntesis y poner los puntos de multiplicación
def traduccion_latex(expresion):
    #Recorrer la expresión y añadir paréntesis alrededor de los negativos y quitar multiplicaciones innecesarias
    p = 0
    while p <len(expresion):
        if type(expresion[p]) == int and expresion[p]<0:
            if expresion[p-1] != '(':
                expresion[p:p] = ['(',expresion.pop(p),')']
                p += 2
        elif expresion[p] == '*' and ( expresion[p+1] == '(' or expresion[p-1] == ')'):
            del expresion[p]
            p -= 1
        p += 1

    #orden de los paréntesis
    paren_i = ['(','[','\\big(','\\big[','\\bigg(','\\bigg[','\\Big(','\\Big[','\\Bigg(','\\Bigg[']
    paren_d = [')',']','\\big)','\\big]','\\bigg)','\\bigg]','\\Big)','\\Big]','\\Bigg)','\\Bigg]']

    #calcular la profundidad máxima de los paréntesis:
    profundidad = 0
    prof_max = 0
    j = 0
    for i in range(len(expresion)):
        if expresion[i] =='(':
            profundidad += 1
            if profundidad > prof_max:
                prof_max = profundidad
        elif expresion[i] == ')':
            profundidad -= 1
        elif expresion[i] == '*':
            expresion[i] = '\\cdot '
        
        #si se ha encontrado un juego de paréntesis que abre y cierra del todo
        if profundidad == 0 and prof_max > 0:
            #cambiar los paréntesis de ese juego
            for k in range(j,i+1):
                if expresion[k] =='(':
                    profundidad += 1
                    expresion[k] = paren_i[prof_max-profundidad] 
                elif expresion[k] == ')':
                    expresion[k] = paren_d[prof_max-profundidad]
                    profundidad -= 1
            j = i+1
            prof_max = 0

    return expresion

#función para simplificar una expresión algebraica
def simplificar(expresion):
    #primero simplificar cambios de signo
    flag = False
    for i in range(len(expresion)):
        if expresion[i] == '-' and type(expresion[i+1])==int and expresion[i+1]<0:
            expresion[i] = '+'
            expresion[i+1] *= -1
            flag = True
        elif expresion[i] == '+' and type(expresion[i+1])==int and expresion[i+1]<0:
            expresion[i] = '-'
            expresion[i+1] *= -1
            flag = True
    if flag:
        return expresion
    #después buscar el paréntesis más profundo
    i = 0
    for j in range(len(expresion)):
        if expresion[j] =='(':
            i = j+1
        elif expresion[j] == ')':
            break
    #el fragmento expresion[i:j+1] sólo son números operaciones
    #en este fragmento, buscar la operación más prioritaria
    try:
        k = expresion.index('*',i,j)
        if j-i == 3:
            expresion[k-2:k+3] = [ expresion[k-1] * expresion[k+1] ]
        else:
            expresion[k-1:k+2] = [ expresion[k-1] * expresion[k+1] ]
        return expresion
    except ValueError:
        pass

    try:
        k = expresion.index(':',i,j)
        if j-i == 3:
            expresion[k-2:k+3] = [ expresion[k-1] // expresion[k+1] ]
        else:
            expresion[k-1:k+2] = [ expresion[k-1] // expresion[k+1] ]
        return expresion
    except ValueError:
        pass

    try:
        k = expresion.index('+',i,j)
        if j-i == 3:
            expresion[k-2:k+3] = [ expresion[k-1] + expresion[k+1] ]
        else:
            expresion[k-1:k+2] = [ expresion[k-1] + expresion[k+1] ]
        return expresion
    except ValueError:
        pass

    k = expresion.index('-',i,j)
    if j-i == 3:
        expresion[k-2:k+3] = [ expresion[k-1] - expresion[k+1] ]
    else:
        expresion[k-1:k+2] = [ expresion[k-1] - expresion[k+1] ]
    return expresion


'''
Ejercicio para practicar el orden de las operaciones
n: Cantidad de apartados.
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5
'''
def orden_operaciones(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    enunciado = 'Simplifica las siguientes expresiones:\n'
    solucion = enunciado
    enunciado += '\\begin{tasks}\n'
    solucion += '\\begin{tasks}\n'
    generados = []
    apartado = 0
    while apartado < n:
        #Elegir un número al azar para empezar
        expresion = [(1 if random.random()>dificultad/15 else -1) * random.randint(6,4*dificultad+4)]
        for k in range(dificultad+3):
            #elegir aleatoriamente un número de la expresion
            while True:
                p = random.randint(0,len(expresion)-1)
                if type(expresion[p]) == int:
                    break
            #tomar el número
            i = expresion[p]
            #Elegir una operación
            #si i es primo, no se puede expresar como multiplicación
            if len([d for d in range(2,i) if i%d==0]) == 0:
                if abs(i) > 20: #si es demasiado grande
                    op = '+'
                elif abs(i) <= 3: #si es demasiado pequeño
                    op = random.choice(['-',':',':'])
                else:
                    op = random.choice(['+','-',':',':'])
            else:
                if abs(i) > 20: #si es demasiado grande
                    op = random.choice(['+','*','*'])
                elif abs(i) <= 3: #si es demasiado pequeño
                    op = random.choice(['-',':',':'])
                else:
                    op = random.choice(['+','-','*','*','*',':',':'])

            #expresar i como la operación de dos números
            if op == '+':
                j = random.randint(2,i-2) if i>0 else random.randint(i+2,-2)
                #distinguir cuándo hay que poner paréntesis
                if operacion_izquierda(expresion,p) in ['+','(',None] and operacion_derecha(expresion,p) in ['+','-',')',None]:
                    operacion =[i-j,'+',j]
                else:
                    operacion =['(',i-j,'+',j,')']
            elif op == '-':
                j = random.randint(2,7) if i>0 else random.randint(-7,-2)
                #distinguir cuándo hay que poner paréntesis
                if operacion_izquierda(expresion,p) in ['+','(',None] and operacion_derecha(expresion,p) in ['+','-',')',None]:
                    operacion =[i+j,'-',j]
                else:
                    operacion =['(',i+j,'-',j,')']
            elif op == '*':
                #escoger un divisor aleatorio
                j = (1 if random.random()>dificultad/15 else -1) * random.choice([d for d in range(2,i) if i%d==0])
                #distinguir cuándo hay que poner paréntesis
                if operacion_izquierda(expresion,p) in ['+','-','*','(',None]:
                    operacion = [i//j,'*',j]
                else:
                    operacion = ['(',i//j,'*',j,')']
            else:#op == ':'
                j = (1 if random.random()>dificultad/15 else -1) * random.randint(2,max(3,dificultad+1))
                if operacion_izquierda(expresion,p) in ['+','-','(',None] and operacion_derecha(expresion,p) in ['+','-',')',None]:
                    operacion = [i*j,':',j] 
                else:
                    operacion = ['(',i*j,':',j,')']
            #sustituir número por su expresión
            del expresion[p]
            expresion[p:p] = operacion
            if debug:
                salida = ''.join(list(map(str,expresion)))
                print(salida)
        
        enunciado += '\\task $'+''.join(list(map(str,traduccion_latex(expresion[:]))))+'$.\n'
        solucion += '\\task $ '+''.join(list(map(str,traduccion_latex(expresion[:]))))+'$\n\n'

        while len(expresion) > 1:
            expresion = simplificar(expresion)
            solucion += '$ =' + ''.join(list(map(str,traduccion_latex(expresion[:]))))+'$\n\n'

        apartado+=1
    enunciado += '\\end{tasks}'
    solucion += '\\end{tasks}'
    return enunciado,solucion,None

'''
Ejercicio para localizar números sobre una recta
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5. Apenas tiene influencia
'''
def numeros_recta(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    #elegir la separación entre las marcas
    sep = random.randint(2,max(2,dificultad*2-1))
    #elegir el número de marcas que aparecen en la recta
    marcas = random.randint(10,15)
    #elegir la posición de los dos números y las 4 letras
    while True:
        posiciones = random.sample(list(range(marcas//2)), 3)+\
                     random.sample(list(range(marcas//2,marcas)), 3)
        #asegurarse de que los dos números están lo bastante separados
        if posiciones[5]-posiciones[0] >= 5:
            break
    #elegir los valores de los dos datos
    d1 = random.randint(-(posiciones[5]-posiciones[0])*sep//2,-3)
    d2 = d1+(posiciones[5]-posiciones[0])*sep
    datos = [d1,'A','B','C','D',d2]
    if debug:
        print(posiciones)
        print(datos)

    enunciado = '\n\n\\noindent \\begin{tikzpicture}\n\\begin{axis} [height = 7em, width=1.12\\textwidth, axis line style={draw=none}, '+\
                 'tick style={draw=none}, xtick=\\empty, ytick=\\empty, xmin=-0.02, xmax=1.02]'
    enunciado += f'\n\\addplot [domain= 0:1, samples={marcas}, mark=|]{{0}};'
    for i in range(6):
        enunciado += f'\n\\node at (axis cs: {posiciones[i]/(marcas-1)} ,0) [anchor=north] {{ {datos[i]} }};'
    enunciado += '\n\\end{axis}\n\\end{tikzpicture}'
    solucion = enunciado
    enunciado = 'Si las marcas de la recta están igualmente espaciadas, ¿qué números se corresponden con las letras A, B, C, D?' + enunciado

    solucion = 'Lo primero que debemos averiguar es cuánto miden la distancia entre marcas. Para eso utilizamos los dos números dados.\n\n ' + solucion
    solucion += f'\n\nLos números dados {datos[0]} y {datos[5]} están separados {posiciones[5]-posiciones[0]} marcas y su diferencia real es '+\
                f'${datos[5]}-({datos[0]})={datos[5]-datos[0]}$. Entonces, si {posiciones[5]-posiciones[0]} marcas cubren '+\
                f'una distancia de {datos[5]-datos[0]}, el espacio entre dos marcas mide ${datos[5]-datos[0]}:{posiciones[5]-posiciones[0]} = {sep}$.'
    solucion += '\n\nCon esto podemos sacar el valor de las cuatro letras:\n\\begin{itemize}'
    for i in range(1,5):
        solucion += f'\n\\item {datos[i]} está a {abs(posiciones[i]-posiciones[5])} marca'
        if abs(posiciones[i]-posiciones[5])>1:
            solucion += 's'
        solucion += ' hacia la '
        if posiciones[i]-posiciones[5]>0:
            solucion += 'derecha '
        else:
            solucion += 'izquierda '
        solucion += f'de {datos[5]}. Como la distancia entre dos marcas es {sep}, '
        solucion += f'{datos[i]} $= {datos[5]} '
        if posiciones[i]-posiciones[5]>0:
            solucion += ' + '
        solucion += f'{posiciones[i]-posiciones[5]}\cdot {sep}={datos[5]} '
        if posiciones[i]-posiciones[5]>0:
            solucion += ' + '
        solucion += f'{(posiciones[i]-posiciones[5])*sep} = {datos[5]+(posiciones[i]-posiciones[5])*sep}$.'
    solucion+= '\n\\end{itemize}'
    return enunciado,solucion,None

'''
Ejercicio donde se da la suma de i a j y se pide la suma de i+1 a j+1
'''
def suma_enteros(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    i = random.randint(7,23)
    j = random.randint(74,95)
    enunciado = f'Si la suma de todos los números naturales entre {i} y {j} es {int((i+j)*(j-i+1)/2)}, ¿cuánto vale la suma de '+\
                f'todos los números naturales entre {i+1} y {j+1}? Piensa una estrategia que te evite sumar todos los números.'
    solucion = f'Sabemos cuánto vale la suma de todos los números naturales entre {i} y {j}. Si nos planteamos la suma de '+\
               f'todos los números naturales entre {i+1} y {j+1} es como si cogiésemos la de {i} a {j} y sumásemos 1 a cada número. '+\
               f'Entonces, el resultado será {int((i+j)*(j-i+1)/2)} más 1 por cada número entre {i} y {j}, contando los dos.\n\n'+\
               f'La cantidad de números entre {i} y {j} es ${j}-{i}+1={j-i+1}$. Entonces, la suma de todos los números naturales entre {i+1} y {j+1} es '+\
               f'${int((i+j)*(j-i+1)/2)}+{j-i+1}={int((i+j+2)*(j-i+1)/2)}$.'
    return enunciado,solucion,None
'''
ejercicio para factorizar un número
n: Cantidad de apartados.
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5
debug: para ver la factorización de los números

La función genera un número a factorizar.
Puede usar tantos 2, 3, 5 como quiera pero sólo un 7, 11, 13
La dificultad incrementa la cantidad de primos disponibles y la cantidad de factores en los números.
'''
def factorizar(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    enunciado = 'Factoriza los siguientes números:\n'
    solucion = enunciado
    enunciado += '\\begin{tasks}(4)\n'
    solucion += '\\begin{tasks}\n'
    
    
    primos = [2,3,5,7,11,13]
    #basado en el nivel de dificultad, creamos un conjunto de primos disponibles
    primos = primos[:max(2,int(len(primos)*math.log(dificultad,5)))]
    generados = []
    apartado = 0
    while apartado < n:
        #cantidad de factores totales
        max_factor = 10*dificultad//5
        #factores no comunes
        factores = []
        
        while len(factores) < max_factor:
            p = random.choice(primos)
            #permitir un sólo 7, 11, 13
            if p in primos[3:] and p in factores:
                continue
            else:
                factores.append(p)

        #fabricar el número
        num = reduce(mul,factores)
        
        #comprobar que no se han generado los mismos de antes
        if num in generados:
            continue
        else:
            generados.append(num)
            apartado+=1

        #fabricar el enunciado
        enunciado += f'\\task ${num}$.\n'
        
        #fabricar solución
        solucion += f'\\task ${num}='
        primero = True
        for i in primos:
            k = factores.count(i)
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
        if debug:
            print(f'{num} {factores}')
     
    enunciado += '\\end{tasks}'
    solucion += '\\end{tasks}'
    return enunciado,solucion,generados


'''
ejercicio para encontrar todos los divisores de un número
n: Cantidad de apartados.
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5
debug: para ver la factorización de los números

La función genera un número a factorizar.
Puede usar tantos 2, 3, 5 como quiera pero sólo un 7, 11, 13
La dificultad incrementa la cantidad de primos disponibles y la cantidad de factores en los números.
'''
def divisores(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    enunciado = 'Encuentra todos los divisores de los siguientes números:\n'
    solucion = 'Vamos por orden desde 1 buscando todos los divisores:\n'
    enunciado += '\\begin{tasks}(4)\n'
    solucion += '\\begin{tasks}\n'

    primos = [2,3,5,7,11,13]
    #basado en el nivel de dificultad, creamos un conjunto de primos disponibles
    primos = primos[:max(2,int(len(primos)*math.log(dificultad,5)))]
    generados = []
    apartado = 0
    while apartado < n:
        #cantidad de factores totales
        max_factor = 7*dificultad//5
        #factores no comunes
        factores = []
        
        while len(factores) < max_factor:
            p = random.choice(primos)
            #permitir un sólo 7, 11, 13
            if p in primos[3:] and p in factores:
                continue
            else:
                factores.append(p)

        #fabricar el número
        num = reduce(mul,factores)
        
        #comprobar que no se han generado los mismos de antes
        if num in generados:
            continue
        else:
            generados.append(num)
            apartado+=1

        #fabricar el enunciado
        enunciado += f'\\task ${num}$.\n'
        
        #fabricar solución
        solucion += f'\\task $\\begin{{aligned}}[t] {num} &='
        primero = True
        divisores = []
        for i in range(1,int(math.sqrt(num))+1):
            if num%i == 0:
                if primero:
                    primero = False
                else:
                    solucion += '\\\\ \n&='
                solucion += f' {i} \\cdot {num//i}'
                divisores.insert(len(divisores)//2,num//i)
                if i not in divisores:
                    divisores.insert(len(divisores)//2,i)
        solucion += f'\n\\end{{aligned}}$\n\nDivisores de ${num}=\\{{'
        primero = True
        for i in divisores:
            if primero:
                primero = False
            else:
                solucion += ', '
            solucion += f'{i}'
        solucion += '\\}$.\n'
        if debug:
            print(f'{num}')
     
    enunciado += '\\end{tasks}'
    solucion += '\\end{tasks}'
    return enunciado,solucion,generados

'''
ejercicio para completar un número y que sea múltiplo de 2 y 3 simultaneamente
n: Cantidad de apartados.
seed: semilla para la generación aleatoria
'''
def divisibilidad(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    enunciado = 'Completa la cifra de las unidades en cada número para que sea múltiplo de 2 y 3 simultaneamente.\n'
    solucion = enunciado
    enunciado += 'Si hay más de una solución, pon todas.\n'
    enunciado += '\\begin{tasks}(4)\n'
    solucion += '\\begin{tasks}(2)\n'
    generados = []
    apartado = 0
    while apartado < n:
        #generar un número de dos cifras
        num = random.randint(10,99)
        #comprobar que no se han generado los mismos de antes
        if num in generados:
            continue
        else:
            generados.append(num)
            apartado+=1

        #fabricar el enunciado
        enunciado += f'\\task ${num}\\_$.\n'
        
        #fabricar solución
        solucion += '\\task $'
        primero = True
        #las unidades pares hacen el múltiplo de 2
        for i in [0,2,4,6,8]:
            #comprobar si el número es múltiplo de 3
            if (num*10+i)%3 ==0:
                if primero:
                    primero = False
                else:
                    solucion += '\\text{ y }'
                solucion += f' {num*10+i}'
        solucion += '$.\n'
        if debug:
            print(f'{num}')
     
    enunciado += '\\end{tasks}'
    solucion += '\\end{tasks}'
    return enunciado,solucion,generados

'''
ejercicio de pregutas de verdadero o falso sobre divisibilidad
seed: semilla para la generación aleatoria
debug: para ver la factorización de los números

'''
def divisibilidad_vf(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    enunciado = 'Contesta si las siguientes afirmaciones son verdaderas o falsas. Razona tu respuesta:\n'
    solucion = 'Razonemos si las afirmaciones son verdaderas o falsas:\n'
    enunciado += '\\begin{tasks}\n'
    solucion += '\\begin{tasks}\n'
    
    #las preguntas utilizan divisibilidad entre 2,3,4 y 5
    divisores = [2,3,4,5]
    random.shuffle(divisores)
    #tipo de afirmación
    tipos = [0,1,2]
    random.shuffle(tipos)
    tipos.append(random.randint(0,2))
    for i in range(4):
        #formulación de la afirmación
        verdadero = random.randint(0,1) == 0
        #múltiplo
        multip = random.randint(700,2000)*divisores[i]
        #desviación para no tener múltiplo
        if not verdadero:
            multip += random.randint(1,divisores[i]-1)

        #fabricar enunciado
        if tipos[i] == 0:
            enunciado += f'\\task El número {divisores[i]} divide a {multip}.\n'
        elif tipos[i] == 1:
            enunciado += f'\\task El número {divisores[i]} es divisor de {multip}.\n'
        else: #tipos[i] == 2:
            enunciado += f'\\task El número {multip} es múltiplo de {divisores[i]}.\n'
            
        def suma_digitos(n):
            suma = 0
            for i in range(int(math.log10(n))+1):
                suma += (n//10**i)%10
            return suma
        
        if verdadero:
            if divisores[i] == 2:
                solucion += '\\task \\textbf{{Verdadero}}. Un número es divisible entre 2 si acaba en 0, 2, 4, 6 u 8. '+\
                            f'{multip} acaba en {multip%10}, entonces {multip} es múltiplo 2.\n'
            elif divisores[i] == 3:
                solucion += '\\task \\textbf{{Verdadero}}. Un número es divisible entre 3 si la suma de sus cifras es múltiplo de 3. '+\
                            f'La suma de las cifras de {multip} es {suma_digitos(multip)}, que es múltiplo de 3. Entonces {multip} es múltiplo 3.\n'
            elif divisores[i] == 4:
                solucion += '\\task \\textbf{{Verdadero}}. Un número es divisible entre 4 si sus dos últimas cifras son múltiplo de 4. '+\
                            f'{multip} acaba en {multip%100}, que es múltiplo de 4. Entonces {multip} es múltiplo 4.\n'
            else: #i == 5:
                solucion += '\\task \\textbf{{Verdadero}}. Un número es divisible entre 5 si acaba en 0 o 5. '+\
                            f'{multip} acaba en {multip%10}, entonces {multip} es múltiplo 5.\n'
        else: #not verdadero:
            if divisores[i] == 2:
                solucion += '\\task \\textbf{{Falso}}. Un número es divisible entre 2 si acaba en 0, 2, 4, 6 u 8. '+\
                            f'{multip} acaba en {multip%10}, entonces {multip} no es múltiplo de 2.\n'
            elif divisores[i] == 3:
                solucion += '\\task \\textbf{{Falso}}. Un número es divisible entre 3 si la suma de sus cifras es múltiplo de 3. '+\
                            f'La suma de las cifras de {multip} es {suma_digitos(multip)}, que no es múltiplo de 3. Entonces {multip} no es múltiplo de 3.\n'
            elif divisores[i] == 4:
                solucion += '\\task \\textbf{{Falso}}. Un número es divisible entre 4 si sus dos últimas cifras son múltiplo de 4. '+\
                            f'{multip} acaba en {multip%100}, que no es múltiplo de 4. Entonces {multip} no es múltiplo de 4.\n'
            else: #i == 5:
                solucion += '\\task \\textbf{{Falso}}. Un número es divisible entre 5 si acaba en 0 o 5. '+\
                            f'{multip} acaba en {multip%10}, entonces {multip} no es múltiplo de 5.\n'

    enunciado += '\\end{tasks}'
    solucion += '\\end{tasks}'
    return enunciado,solucion,None
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
        
        while min(len(no_comun1),len(no_comun2)) < max_factor:
            p = random.choice(primos)
            #sólo permitir un primo mayor o igual a 7
            if p in primos[3:]:
                if primo_grande:#si hay un primo grande en los comunes
                    continue
                primo_grande = True
            #si el factor ya ha salido y los números no son demasiado grandes
            if p in no_comun1 and len(no_comun1)< max_factor:
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
        
        while min(len(no_comun1),len(no_comun2),len(no_comun3)) < max_factor:
            p = random.choice(primos)
            #sólo permitir un primo mayor o igual a 7
            if p in primos[3:]:
                if primo_grande:#si hay un primo grande en los comunes
                    continue
                primo_grande = True
            #si el factor ya ha salido y los números no son demasiado grandes
            if p in no_comun1 and len(no_comun1)< max_factor:
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
        todos = comunes + no_comun1+no_comun2+no_comun3
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
ejercicio para enconrar un número múltiplo del mcm de tres números
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5
debug: para ver la factorización de los números

La función genera tres números con unos cuantos factores y otros no comunes.
La cantidad de no comunes puede ser cero
Puede usar tantos 2, 3, 5 como quiera pero sólo un 7, 11, 13
La dificultad incrementa la cantidad de primos disponibles y la cantidad de factores en los números.
'''
def multiplo_comun(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
            
    primos = [2,3,5,7,11,13]
    #basado en el nivel de dificultad, creamos un conjunto de primos disponibles
    primos = primos[:max(2,int(len(primos)*math.log(dificultad,5)))]
    #cantidad de factores totales
    max_factor = 4*dificultad//5
    #cantidad de factores comunes
    max_comunes = math.ceil(random.randint(1,(max_factor-1)*3)/3)
    #restar la cantidad de comunes
    max_factor -= max(1,max_comunes)
    #factores comunes a los dos
    comunes = []
    primo_grande = False
    while len(comunes) < max_comunes:
        #permitir todos menos los dos últimos primos disponible
        p = random.choice(primos[:-2])
        #sólo permitir un primo mayor o igual a 5
        if p in primos[2:]:
            primo_grande = True
        comunes.append(p)
    #factores no comunes
    no_comun1 = []
    no_comun2 = []
        
    while min(len(no_comun1),len(no_comun2)) < max_factor:
        #permitir todos menos los dos últimos primos disponible
        p = random.choice(primos[:-2])
        #sólo permitir un primo mayor o igual a 5
        if p in primos[2:]:
            if primo_grande:#si hay un primo grande en los comunes
                continue
            primo_grande = True

        #si el factor ya ha salido y los números no son demasiado grandes
        if p in no_comun1 and len(no_comun1)< max_factor:
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

    #generamos el tercero
    no_comun3 = []
    while len(no_comun3) < max_factor:
        #usar primos mayores o iguales a 5
        p = random.choice(primos[2:])
        if p in comunes or p in no_comun1 or p in no_comun2:
            continue
        no_comun3.append(p)

    #fabricar los dos números
    num1 = reduce(mul, comunes)*reduce(mul, no_comun1)
    num2 = reduce(mul, comunes)*reduce(mul, no_comun2)
    num3 = reduce(mul,no_comun3)
    
    #fabricar múltiplo a encontrar
    num = random.randint(3,8)*math.lcm(num1,num2,num3)
    #fabricar cotas redondeadas a la decena
    cot_inf = (num-math.lcm(num1,num2,num3)//2)//10*10
    cot_sup = (num+math.lcm(num1,num2,num3)//2)//10*10

    #fabricar el enunciado
    enunciado = f'De cierto número desconocido sabemos que está entre {cot_inf} y {cot_sup}. '+\
                 f'Además, sabemos que es divisible entre {num1}, {num2} y {num3}. Halla este número.'
    solucion = f'Que sepamos que el número buscado es divisble entre {num1}, {num2} y {num3} nos indica '+\
                'que es un múltiplo común a los tres. Seguramente no sea el mínimo común múltiplo pero empecemos por calcularlo.\n\n'+\
                '\\begin{itemize}\n'
        
    #fabricar solución
    #primer número
    factor1 = comunes + no_comun1
    solucion += f'\\item ${num1}='
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
    factor2 = comunes + no_comun2
    solucion += f'$.\n\\item ${num2}='
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
    factor3 = no_comun3
    solucion += f'$.\n\\item ${num3}'
    if len(no_comun3) == 1:
        solucion += '$ es primo'
    else:
        solucion += '='
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
        solucion+='$'
    #solución
    solucion += f'.\n\\item mcm$({num1},{num2},{num3}) = '
    todos = comunes + no_comun1 + no_comun2 + no_comun3
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
    solucion += f' = {math.lcm(num1,num2,num3)}$.\n\\end{{itemize}}\n'
    solucion += f'El número {math.lcm(num1,num2,num3)} está por debajo de {cot_inf} '+\
                f'pero debe haber un múltiplo suyo por encima de {cot_inf} y por debajo de {cot_sup}. '+\
                f'Podríamos encontrarlo calculando múltiplos sucesivos de {math.lcm(num1,num2,num3)} pero vamos a hacerlo mejor.\n\n'+\
                f'Si dividimos {cot_sup} entre {math.lcm(num1,num2,num3)} nos sale cociente '+\
                f'{cot_sup//math.lcm(num1,num2,num3)} y resto {cot_sup%math.lcm(num1,num2,num3)}. Nos interesa el cociente. '+\
                f'Con él sabemos que el número más cercano a {cot_sup} por debajo que es múltiplo de {math.lcm(num1,num2,num3)} es '+\
                f'${cot_sup//math.lcm(num1,num2,num3)}\cdot {math.lcm(num1,num2,num3)}={cot_sup//math.lcm(num1,num2,num3)*math.lcm(num1,num2,num3)}$. '+\
                f'Este número está entre {cot_inf} y {cot_sup} y es múltiplo de {num1}, {num2} y {num3}.\n\n'+\
                f'Las otras posibles opciones sería coger {num} y sumarle o restarle {math.lcm(num1,num2,num3)}, para encontrar otros múltiplos de '+\
                f'{num1}, {num2} y {num3}. Pero la opción de restar da {num-math.lcm(num1,num2,num3)}, por debajo de {cot_inf}, '+\
                f'y la de sumar da {num+math.lcm(num1,num2,num3)}, por encima de {cot_sup}.\n\n'+\
                f'Entonces, el número buscado es {num}.'
    if debug:
        print(f'{num1} {factor1}, {num2} {factor2}, {num3} {factor3}. mcm: {math.lcm(num1,num2,num3)}')
     
    return enunciado,solucion,sorted([num1,num2,num3,num])

def divisor_comun(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    
    primos = [2,3,5,7,11,13]
    #basado en el nivel de dificultad, creamos un conjunto de primos disponibles
    primos = primos[:max(2,int(len(primos)*math.log(dificultad,5)))]


    #cantidad de factores comunes
    max_comunes = 5*dificultad//5
    #cantidad de factores no comunes
    max_factor = 4*dificultad//5
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
        
    while min(len(no_comun1),len(no_comun2),len(no_comun3)) < max_factor:
        p = random.choice(primos)
        #si el factor ya ha salido y los números no son demasiado grandes
        if p in no_comun1 and len(no_comun1)< max_factor:
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
    num1 = reduce(mul, comunes)*reduce(mul, no_comun1)
    num2 = reduce(mul, comunes)*reduce(mul, no_comun2)
    num3 = reduce(mul, comunes)*reduce(mul, no_comun3)
    #fabricar el número buscado
    num = reduce(mul, random.sample(comunes,len(comunes)-max(1,len(comunes)//2)))
    lista_div = [d for d in range(2,math.gcd(num1,num2,num3)+1) if math.gcd(num1,num2,num3)%d==0]
    #fabricar cotas
    cot_inf = lista_div[lista_div.index(num)-1]+1
    cot_sup = lista_div[lista_div.index(num)+1]-1

     #fabricar el enunciado
    enunciado = f'De cierto número desconocido sabemos que es menor o igual que {cot_inf} y mayor o igual que {cot_sup}. '+\
                 f'Además, sabemos que es divisor entre {num1}, {num2} y {num3}. Halla este número.'
    solucion = f'Que sepamos que el número buscado es divisor entre {num1}, {num2} y {num3} nos indica '+\
                'que es un divisor común a los tres. Seguramente no sea el máximo común divisor pero empecemos por calcularlo.\n\n'+\
                '\\begin{itemize}\n'
        
    #fabricar solución
    #primer número
    factor1 = no_comun1 + comunes
    solucion += f'\\item ${num1}='
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
    solucion += f'$.\n\\item ${num2}='
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
    solucion += f'$.\n\\item ${num3}='
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
    solucion += f'$.\n\\item MCD$({num1},{num2},{num3}) = '
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
    solucion += f'={math.gcd(num1,num2,num3)}$.\n\\end{{itemize}}\n'
    solucion += f'El número {math.gcd(num1,num2,num3)} está por encima de {cot_sup} '+\
                f'pero debe haber un divisor suyo menor o igual que {cot_inf} y mayor o igual que {cot_sup}. '+\
                f'Para encontrarlo, vamos a enumerar todos los divisores del máximo común divisor.\n\n'
    #fabricar solución
    solucion += f'$\\begin{{aligned}}[t] {math.gcd(num1,num2,num3)} &='
    primero = True
    divisores = []
    for i in range(1,int(math.sqrt(math.gcd(num1,num2,num3)))+1):
        if math.gcd(num1,num2,num3)%i == 0:
            if primero:
                primero = False
            else:
                solucion += '\\\\ \n&='
            solucion += f' {i} \\cdot {math.gcd(num1,num2,num3)//i}'
            divisores.insert(len(divisores)//2,math.gcd(num1,num2,num3)//i)
            if i not in divisores:
                divisores.insert(len(divisores)//2,i)
    solucion += f'\n\\end{{aligned}}$\n\nDivisores de ${math.gcd(num1,num2,num3)}=\\{{'
    primero = True
    for i in divisores:
        if primero:
            primero = False
        else:
            solucion += ', '
        solucion += f'{i}'
    solucion += '\\}$.\n\n'
    solucion += f'El único divisor común de {num1}, {num2} y {num3} entre {cot_inf} y {cot_sup} es {num}. Ése es el número buscado.'

    if debug:
        print(f'{num1} {factor1}, {num2} {factor2}, {num3} {factor3}. MCD: {math.gcd(num1,num2,num3)}, mcm: {math.lcm(num1,num2,num3)}')

    return enunciado,solucion,sorted([num1,num2,num3,num])

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
        tipo = 0
    else:
        tipo = random.randint(1,n_enunciados-1)

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
    enunciado += '\n\nArgumenta adecuadamente por qué tu solución es correcta.'

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
     
    return enunciado,solucion,sorted([num1,num2])

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
def mcd_mcm_inverso(n = 1, seed = None, dificultad = 3,debug = False):
    if seed:
        random.seed(seed)
    
    primos = [2,3,5,7,11,13]
    #basado en el nivel de dificultad, creamos un conjunto de primos disponibles
    primos = primos[:max(2,int(len(primos)*math.log(dificultad,5)))]

    #cantidad de factores totales
    max_factor = 6*dificultad//5
    #cantidad de factores comunes
    max_comunes = math.ceil(random.randint(0,(max_factor-2)*3)/3)
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
        
    while min(len(no_comun1),len(no_comun2)) < max_factor:
        p = random.choice(primos)
        #sólo permitir un primo mayor o igual a 7
        if p in primos[3:]:
            if primo_grande:#si hay un primo grande en los comunes
                continue
            primo_grande = True
        #sólo permitir un 5
        if p == 5 and (p in no_comun1 or p in no_comun2 or p in comunes):
            continue
        #si el factor ya ha salido y los números no son demasiado grandes
        if p in no_comun1 and len(no_comun1)< max_factor:
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
            f'De estos dos números sabemos que MCD$(a,b)={math.gcd(num1,num2)}$ '+\
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
    solucion += f'\\item MCD$(a,b) = {math.gcd(num1,num2)}'
    primero = True
    if len(comunes)>1:
        solucion+=' = '
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
    solucion += f'\\item mcm$({num1},{num2}) = {math.lcm(num1,num2)} = '
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
    solucion += '$.\n\\end{itemize}\n'

    solucion += 'De los factores del mínimo común múltiplo, los que pertenecen a $a$ son $'
    todos = comunes + no_comun1
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
    solucion += '$. Los factores que no hemos contado más los del máximo común divisor son los factores de $b$. '

    #segundo número
    factor2 = no_comun2 + comunes
    solucion += f'Entonces $b='
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
    solucion += f'={num2}$.\n\n'

    solucion += 'Otra manera de encontrar $b$ es usar la propiedad $\\text{MCD}(a,b)\\cdot\\text{mcm}(a,b)=a\\cdot b$. Entonces '+\
                '\n$$b = \\frac{{ \\text{MCD}(a,b) \\cdot \\text{mcm}(a,b) }}{{ a }}='+\
                f'\\frac{{ {math.gcd(num1,num2)} \\cdot {math.lcm(num1,num2)} }}{{ {num1} }}'+\
                f'=\\frac{{ {num1*num2} }}{{ {num1} }} = {num2}.$$\n'
    if debug:
        print(f'{num1} {factor1}, {num2} {factor2}. MCD: {math.gcd(num1,num2)}, mcm: {math.lcm(num1,num2)}')

    return enunciado,solucion,sorted([num1,num2])

'''
problema de mínimos comunes múltiplos
fijo: si se desea que todos los problemas usen el mismo enunciado (toma el día como generador)
seed: semilla para la generación aleatoria
dificultad: entre 1 y 5
debug: para ver la factorización de los números

La función genera un problema sobre mínimo común múltiplo con distintos enunciados
Puede usar tantos 2, 3 como quiera pero sólo un 5, 7, 11, 13
'''
def Problema_mcd(fijo = False, seed = None, dificultad = 3,debug = False):
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
        tipo = 0
    else:
        tipo = random.randint(1,n_enunciados-1)

    if tipo == 0:
        enunciado = 'Estamos colocando baldosas en una habitación de dimensiones '+\
                    f'{num1} por {num2} metros. Si queremos coger las baldosas cuadradas lo más grandes posibles, '+\
                    '¿qué tamaño de baldosa debemos coger?'
        solucion = 'El tamaño de la baldosa tiene que satisfacer que, cuando pongamos suficientes a lo largo y a lo ancho, '+\
                   'cubra de pared a pared de la habitación. Esto es, debe ser un divisor de la longitud de ambas paredes. '+\
                   'Necesitamos encontrar un número que sea divisor de '+\
                   f'{num1} y de {num2} y además lo más grande posible. Ese número es el máximo común divisor.\n\n'
    elif tipo == 1:
        enunciado = f'Tenemos {num1} lápices y {num2} rotuladores. Con ellos queremos hacer paquetes, '+\
                    'cada uno con o bien lápices o bien rotuladores, de tal manera que cada paquete tenga el mismo '+\
                    'número de objetos, esta cantidad sea máxima y no nos queden objetos sueltos. '+\
                    '¿Cuántos lápices o rotuladores hay que poner en cada paquete?'
        solucion = 'La cantidad de objetos en los paquetes tiene que satisfacer que usemos todos los objetos, con lo que la cantidad '+\
                    'debe ser un divisor del número de objetos. Además, esta cantidad tiene que ser la misma en todos. '+\
                   'Entonces, necesitamos encontrar un número que sea divisor de '+\
                   f'{num1} y de {num2} y además lo más grande posible. Ese número es el máximo común divisor.\n\n'
    elif tipo == 2:
        enunciado = f'Tenemos dos cuerdas, una de {num1} metros y otra de {num2} metros. '+\
                    'Queremos cortarlas en trozos de manera que todos los trozos sean iguales y midan lo más largo posible. '+\
                    '¿Cuánto tienen que medir estos trozos?'
        solucion = 'La longitud de los trozos tiene que satisfacer que cubramos con ellos las dos longitudes de las cuerdas, '+\
                   'esto es, debe ser un divisor de la longitud de ambas cuerdas. '+\
                   'Necesitamos encontrar un número que sea divisor de '+\
                   f'{num1} y de {num2} y además lo más grande posible. Ese número es el máximo común divisor.\n\n'
    elif tipo == 3:
        enunciado = f'Un ebanista quiere cortar una plancha de {num1} dm de largo y {num2} de ancho, en '+\
                    'cuadrados lo más grandes posibles y cuyo lado sea un número entero de decímetros'+\
                    '¿Cuánto debe ser la longitud del lado?'
        solucion = 'La longitud del lado debe satisfacer que, cuando pongamos suficientes a lo largo y a lo ancho, '+\
                   'cubra la plancha entera. Esto es, debe ser un divisor de de ambas longitudes. '+\
                   'Necesitamos encontrar un número que sea divisor de '+\
                   f'{num1} y de {num2} y además lo más grande posible. Ese número es el máximo común divisor.\n\n'
    elif tipo == 4:
        enunciado = f'Tenemos {num1} bolas blancas y {num2} bolas negras. Queremos hacer montones de bolas del mismo color '+\
                    'de manera que todos los montones sean iguales y tengan la mayor cantidad de bolas posible posible. '+\
                    '¿Cuántas bolas deben tener los montones?'
        solucion = 'La cantidad de bolas en los montones debe satisfacer que usemos todas, con lo que la cantidad '+\
                   'debe ser un divisor del número de bolas. Además, esta cantidad debe ser la misma en todos '+\
                   'Entonces, necesitamos encontrar un número que sea divisor de '+\
                   f'{num1} y de {num2} y además lo más grande posible. Ese número es el máximo común divisor.\n\n'
    enunciado += '\n\nArgumenta adecuadamente por qué tu solución es correcta.'

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
    solucion += f'$. Entonces, MCD$({num1},{num2}) = '
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
    solucion += f' = {math.gcd(num1,num2)}$.\n\n'

    if tipo == 0:
        solucion += f'El tamaño de las baldosas debe ser ${math.gcd(num1,num2)}$ por ${math.gcd(num1,num2)}$ metros.'
    elif tipo == 1:
        solucion += f'Cada paquete debe tener ${math.gcd(num1,num2)}$ lápices o bolígrafos.'
    elif tipo == 2:
        solucion += f'Cada trozo debe medir ${math.gcd(num1,num2)}$ metros.'
    elif tipo == 3:
        solucion += f'La longitud del lado debe ser ${math.gcd(num1,num2)}$ decímetros.'
    elif tipo == 4:
        solucion += f'Cada montón debe tener ${math.gcd(num1,num2)}$ bolas.'

    if debug:
        print(f'{num1} {factor1}, {num2} {factor2}. MCD: {math.gcd(num1,num2)}, mcm: {math.lcm(num1,num2)}')
     
    return enunciado,solucion,sorted([num1,num2])