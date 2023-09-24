import random
import math

def poligono_geoplano(n = 1, seed = None, dificultad = 3,debug = False):
    #crear los puntos, asegurándose de que los triángulos tengan área entera.
    #cada vértice irá en uno de 6 puntos del geoplano por lado, cada uno distinto
    vertices = random.sample(list(range(2,9,2)),4)
    enunciado = 'Si la distancia entre puntos consecutivos es una unidad de distancia $u$, '+\
                'calcula el área de la figura sombreada:\n'
    enunciado += '\\begin{center}\n\\begin{tikzpicture}\n\\begin{axis}'+\
                 '[height= 12 cm, width=12 cm, axis line style={draw=none},tick style={draw=none}, xtick=\\empty, ytick=\\empty]\n'+\
                 '\\foreach \\x in {0,1,...,9}{\n\\foreach \\y in {0,1,...,9}{\n'+\
                 '\\addplot[only marks,mark size=2pt] coordinates {(\\x,\\y)};\n}}\n'+\
                 f'\\addplot[name path=plot1,color=black,mark=none] coordinates {{({vertices[0]},0)(9,{vertices[1]})}};\n'+\
                 f'\\addplot[name path=plot2,color=black,mark=none] coordinates {{(9,{vertices[1]})({vertices[2]},9)}};\n'+\
                 f'\\addplot[name path=plot3,color=black,mark=none] coordinates {{({vertices[2]},9)(0,{vertices[3]})}};\n'+\
                 f'\\addplot[name path=plot4,color=black,mark=none] coordinates {{(0,{vertices[3]})({vertices[0]},0)}};\n'+\
                 '\\addplot[color=gray!50] fill between[of = plot1 and plot2];\n'+\
                 '\\addplot[color=gray!50] fill between[of = plot3 and plot4];\n'+\
                 '\\end{axis}\n\\end{tikzpicture}\n\\end{center}'
    solucion = ''
    return enunciado,solucion,vertices
