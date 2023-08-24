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

    def ejercicio(self,funcion,n = 1, seed = None, dificultad = 3):
        enunciado,solucion = eval(funcion)(n,seed,dificultad)
        self.contenido += enunciado
        self.solucion += solucion

    def compilar(self):
        os.system(f'pdflatex {self.nombre}.tex')
        os.system(f'pdflatex {self.nombre}_solucion.tex')
        
        #recolector de basura
        for fichero in os.listdir():
            if self.nombre in fichero:
                if fichero[-3:] in ['tex','aux','log','out']:
                    os.remove(fichero)

if __name__ == '__main__':
    doc = Documento('prueba')
    doc.ejercicio('Enteros.mcd_mcm',n=4)
    doc.cerrar()
    doc.compilar()
