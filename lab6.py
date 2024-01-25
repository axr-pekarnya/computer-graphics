from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import threading
import math
import sys
import numpy as np

# параметры освещения
light_pos = (0,10, 10) # положение источника света
light_intensity = 0  # интенсивность света
# фоновое освещение - окружающее освещеие, которое всегда будет придавать объекту некоторый оттенок
amb_light = [0.5, 0.4, 0.2]
# диффузное освещение - имитирует воздействие на объект направленного источника света
diff_light = [1.5, 1.0, 0.0, light_intensity]


# вращение
x_rot = 0
y_rot = -40
z_rot = 0

# параметры фигуры
approx = 30  # количество образующих
size = 1
a, b, c = 5, 3, 3


def init():
    glClearColor(0.44, 0.44, 0.7, 0)  # цвет для заднего фона
    glEnable(GL_DEPTH_TEST)  # обновляем буфер глубины
    glDepthFunc(GL_LEQUAL)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, amb_light)  # определяем текущую модель освещения
    glEnable(GL_LIGHTING)  # включаем освещение
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)  # вершины заднего многоугольника зажигаются с помощью параметров
    # заднего материала и имеют обратную норму перед вычислением уравнения освещения


def ellipsoid_layer():
    global a, b, c, approx
    longitude_delta = np.linspace(0, np.pi*2, approx + 1) #долгота
    latitude_delta = np.linspace(np.pi/4, np.pi*3/4, approx + 1) #широта
    vertices = []

    for i in range(approx + 1):
        lat = latitude_delta[i]
        for j in range(approx + 1):
            lon = longitude_delta[j]
            x = a * math.sin(lat) * math.cos(lon)
            y = b * math.sin(lat) * math.sin(lon)
            z = c * math.cos(lat)
            vertices.append([x, y, z]) #создание массива координат вершин
    for i in range(approx + 1): 
        glBegin(GL_TRIANGLE_STRIP) 
        for j in range(approx + 1): # задаем веришны
            glVertex3fv(vertices[j + i * approx]) 
            glVertex3fv(vertices[j + (i + 1) * approx])
        glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(7,7, 7, 0, 0, 0, 0, 0, 2)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glTranslatef(size, size, size)
    init_lighting()
    glRotatef(x_rot, 1, 0, 0)
    glRotatef(y_rot, 0, 0, 1)
    glRotatef(z_rot, 0, 1, 0)

    glPushMatrix()  # сохраняем текущее положение "камеры"
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diff_light)
    ellipsoid_layer()
    glPopMatrix()  # возвращаем сохраненное положение "камеры"
    glutSwapBuffers()  # выводим все нарисованное в памяти на экран


def init_lighting():
    glEnable(GL_LIGHT0)  # инициализация источника света
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)  # положение источника света
    l_dif = (2.0, 2.0, 3.0, light_intensity)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, l_dif)
    l_dir = (light_pos[0], light_pos[1], light_pos[2], 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, l_dir)

    # затухание света
    attenuation = float(100 - light_intensity) / 30.0
    distance = math.sqrt(pow(light_pos[0], 2) + pow(light_pos[1], 2) + pow(light_pos[2], 2))

    linear_attenuation = attenuation / (3.0 * distance)
    quadratic_attenuation = attenuation / (3.0 * distance * distance)
    # glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, constant_attenuation)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, linear_attenuation)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, quadratic_attenuation)


def rescale(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, float(width) / float(height), 1.0, 60.0)  # 1)Поле угла зрения в градусах в направлении y.;
    # 2) Пропорции, определяющие поле представления в направлении x - отношение x/y;
    # 3) расстояние от наблюдателя до ближней плоскости; 4) до дальней плоскости
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1, 0)


def keys(key, x, y):
    global x_rot, y_rot, z_rot, size, approx, light_intensity
    # вращаем на +-5 градусов по оси X
    if key == b'w':
        x_rot += 5  
    if key == b's':
        x_rot -= 5  
    # вращаем на +-5 градусов по оси Y
    if key == b'a':
        y_rot += 5  
    if key == b'd':
        y_rot -= 5  
    # вращаем на +-5 градусов по оси Z
    if key == b'q':
        z_rot += 5  
    if key == b'e':
        z_rot -= 5
    # размер фигуры +-1
    if key == b'=':
        size += 1  
    if key == b'-':
        size -= 1
    # изменение числа образующих на +-1
    if key == b'.':
        approx += 1  
    if key == b',':
        approx -= 1
        approx = max(10, approx)
    # интенсивность света +-5
    if key == b'0':
        light_intensity += 5  
        light_intensity = min(100, light_intensity)
    if key == b'9':
        light_intensity -= 5 
        light_intensity = max(-100, light_intensity)
    glutPostRedisplay()  # помечает, что текущее окно требует повторного отображения



def change_color():
    global amb_light, diff_light, light_intensity
    i = 0.01
    while True:
        diff_light = [np.sin(i * np.pi), np.sin(i +0.02* np.pi), np.sin(i+ 0.13 * np.pi), light_intensity]
        amb_light = [np.sin(i* np.pi), np.sin(i + 0.02 * np.pi), 0.2]
        i = i + 0.01
        glutPostRedisplay()
        time.sleep(0.01)
  
            

def main():
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) 
    glutInitWindowSize(500, 500)
    glutInit(sys.argv)
    glutCreateWindow("lab 6")
    glutDisplayFunc(display)  # функция отрисовки
    glutReshapeFunc(rescale)  # функция масштабирования
    glutKeyboardFunc(keys)  # функция обработки нажатий
    init()
    
    t = threading.Thread(target=change_color)
    t.daemon = True
    t.start()
    glutMainLoop()

main()