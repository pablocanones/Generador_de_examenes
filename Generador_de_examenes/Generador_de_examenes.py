import os
import Enteros
import codecs

class Documento():
    def __init__(self,nombre):
        self.nombre = nombre
        with open('preambulo.txt','r') as data:
            self.contenido = data.read()
            self.solucion = self.contenido
        self.contenido += '\n\\begin{document}\n'
        self.solucion += '\n\\begin{document}\n'

    def cerrar(self):
        self.contenido += '\n\\end{document}'
        self.solucion += '\n\\end{document}'
        with codecs.open(f'{self.nombre}.tex','w','utf-8') as data:
            data.write(self.contenido)
        with codecs.open(f'{self.nombre}_solucion.tex','w','utf-8') as data:
            data.write(self.solucion)

    def ejercicio(self,funcion,n = 1, seed = None, dificultad = 3, debug = False):
        self.contenido += '\n\\begin{ejercicio}'
        self.solucion += '\n\\begin{ejercicio}'
        enunciado,solucion,resumen = eval(funcion)(n,seed,dificultad,debug)
        self.contenido += enunciado
        self.solucion += solucion
        self.contenido += '\n\\end{ejercicio}'
        self.solucion += '\n\\end{ejercicio}'

    def problema(self,funcion,fijo = False, seed = None, dificultad = 3, debug = False):
        self.contenido += '\n\\begin{ejercicio}'
        self.solucion += '\n\\begin{ejercicio}'
        enunciado,solucion,resumen = eval(funcion)(fijo,seed,dificultad,debug)
        self.contenido += enunciado
        self.solucion += solucion
        self.contenido += '\n\\end{ejercicio}'
        self.solucion += '\n\\end{ejercicio}'

    def compilar(self,debug = False):
        os.system(f'pdflatex {self.nombre}.tex')
        os.system(f'pdflatex {self.nombre}_solucion.tex')
        
        if not debug:
            #recolector de basura
            for fichero in os.listdir():
                if self.nombre in fichero:
                    if fichero[-3:] in ['tex','aux','log','out']:
                        os.remove(fichero)
   
def demo():
    doc = Documento('demo')
    doc.ejercicio('Enteros.orden_operaciones',n=8)
    doc.problema('Enteros.numeros_recta')
    doc.ejercicio('Enteros.factorizar',n=4)
    doc.ejercicio('Enteros.divisores',n=4)
    doc.ejercicio('Enteros.divisibilidad',n=4)
    doc.ejercicio('Enteros.divisibilidad_vf')
    doc.ejercicio('Enteros.mcd_mcm',n=4)
    doc.ejercicio('Enteros.mcd_mcm_3',n=2)
    doc.problema('Enteros.multiplo_comun')
    doc.problema('Enteros.divisor_comun')
    doc.problema('Enteros.mcd_mcm_inverso')
    doc.problema('Enteros.Problema_mcm')
    doc.problema('Enteros.Problema_mcd')
    doc.cerrar()
    doc.compilar()

if __name__ == '__main__':
    '''
    doc = Documento('prueba')
    for i in range(3):
        #doc.problema('Enteros.Problema_recta',debug=True)
        doc.ejercicio('Enteros.divisibilidad_vf')
    doc.cerrar()
    doc.compilar()
    '''
    #print(Enteros.orden_operaciones(n=8,debug=True,dificultad=3))
    #print(Enteros.simplificar(['(', 6,'+',4,')','*',5]))

    demo()