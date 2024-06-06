import math
import time
import serial
from constants import *
import numpy as np
import threading


# klasa pomocnicza służąca bardziej jako struktura
class Position:
    x = 0.0
    y = 0.0
    z = 0.0


# klasa reprezentująca kształt prostokąta
# w zależności od podanych przy inicjalizacji parametrów, klasa przelicza je aby ostatecznie
# otrzymać współrzędne dwóch przeciwległych narożników oraz wysokość i szerokość
class Rectangular:
    left_down_corner = [0.0, 0.0]
    up_right_corner = [0.0, 0.0]
    width = 10.0
    height = 10.0
    z = MAX_Z - MARGINES

    def __init__(self, z, left_down_corner=None, up_right_corner=None, width=None, height=None):
        self.z = z

        if left_down_corner is not None and up_right_corner is not None:
            self.left_down_corner = left_down_corner
            self.up_right_corner = up_right_corner
            self.width = up_right_corner[0] - left_down_corner[0]
            self.height = up_right_corner[1] - left_down_corner[1]

        elif left_down_corner is not None and width is not None and height is not None:
            self.left_down_corner = left_down_corner
            self.width = width
            self.height = height
            self.up_right_corner = [left_down_corner[0] + width, left_down_corner[1] + height]

        elif up_right_corner is not None and width is not None and height is not None:
            self.up_right_corner = up_right_corner
            self.width = width
            self.height = height
            self.left_down_corner = [up_right_corner[0] - width, up_right_corner[1] - height]


class Frezarka:

    # VARIABLES DECLARATION
    x = 1700.0      # zestaw współrzędnych narzędzia frezującego
    y = 0.0
    z = 110.0

    move_robot = False
    receive_uart = object
    data_uart = object
    control_uart = object
    more = False
    impulses = []
    current_impuls = 0
    reset = True

    # inicjalizujemy klasy obsługujące komunikację szeregową w zakresie danych oraz
    # sygnałów sterujących, oraz włączamy wątek odbierający dane UART
    def __init__(self, coordinates=None):
        if coordinates is not None:
            self.x = coordinates[0]
            self.y = coordinates[1]
            self.z = coordinates[2]

        try:
            self.data_uart = serial.Serial(control_uart_com, 115200, timeout=0.1)
            self.control_uart = serial.Serial(data_uart_com, 115200, timeout=0.1)
        except:
            print('Nie można podłączyć się do COM6 lub COM7')

        self.receive_uart = threading.Thread(target=self.start_receiving_uart)
        self.receive_uart.start()

    # funckja służąca do odbioru i interpretacji lokalizacji wysyłanej przez mikrokontroler
    def receive_location(self):
        receive = 14
        x_pos = ''
        y_pos = ''
        z_pos = ''

        # odbiór ramki z danymi
        try:
            while receive:
                data = self.control_uart.read()
                if data:
                    data = data.decode()
                    if receive > 10:
                        x_pos += data
                    elif 10 > receive > 5:
                        y_pos += data
                    elif 5 > receive > 0:
                        z_pos += data

                    receive -= 1

            # zamiana odebranych danych na pozycję interpretowalną przez użytkownika
            a = bin(int.from_bytes(x_pos.encode(), 'big'))
            a = a[2:]
            x_pos = int(a, 2)
            self.x = x_pos / 10000

            a = bin(int.from_bytes(y_pos.encode(), 'big'))
            a = a[2:]
            y_pos = int(a, 2)
            self.y = y_pos / 10000

            a = bin(int.from_bytes(z_pos.encode(), 'big'))
            a = a[2:]
            z_pos = int(a, 2)
            self.z = z_pos / 10000
        except:
            print('Problem z UART')  #

    # funkcja uruchomiona w osobnym wątku, służy do nasłuchiwania i odbierania danych UART
    def start_receiving_uart(self):
        try:
            while True:
                data = self.control_uart.read()
                if data:
                    data = data.decode()
                    print(data)
                    if data == 'M':
                        self.more = True
                    elif data == 'x':
                        self.receive_location()
        except:
            print('Problem z UART')

    # funkcja służąca do włączania i wyłączania pompy
    # wysłanie odpowiedniego znaku do mikrokontrolera powoduje odpowiednie przełączanie przekaźników
    def pump_on(self, czy):
        try:
            if czy == True:
                self.control_uart.write('P'.encode())
            elif czy == False:
                self.control_uart.write('p'.encode())
        except:
            print('UART problem')

    # funkcja służąca do włączania i wyłączania falownika
    # wysłanie odpowiedniego znaku do mikrokontrolera powoduje odpowiednie przełączanie przekaźników
    def falownik_on(self, czy):
        try:
            if czy == True:
                self.control_uart.write('B'.encode())
            elif czy == False:
                self.control_uart.write('b'.encode())
        except:
            print('UART problem')

    # funkcja obsługująca realizację zadanej trajektorii poprzez wysyłanie kolejnych
    # paczek z kolejnością impulsów podawanych na sterowniki silników
    def start(self):
        self.move_robot = True

        if self.reset:              # jeżeli zaczynamy realizację od początku
            self.pump_on(True)
            time.sleep(15)
            self.falownik_on(True)
            time.sleep(20)

        # jeżeli nie doszliśmy do końca listy impulsów i mikrokontroler ma
        # miejsce na kolejne dane, to wysyłamy kolejną paczkę danych
        while self.move_robot:
            if self.more and self.current_impuls < len(self.impulses):
                self.more = False
                try:
                    self.data_uart.write((self.impulses[self.current_impuls]).encode())
                except:
                    print('Uart problem')
                self.current_impuls += 1

    # funkcja zatrzymująca ruch frezarki poprzez ustawienie odpowiednich parametrów
    # w programie oraz wysłanie odpowiedniej informacji do mikrokontrolera
    def stop(self):
        self.move_robot = False
        self.reset = False

        try:
            self.control_uart.write('S'.encode())
        except:
            print('Błąd połączenia UART')

    # funkcja pozwalająca na dalszą realizację trajektorii po przerwaniu
    # jej wykonywania przyciskiem STOP
    def resume(self):
        try:
            self.control_uart.write('R'.encode())
        except:
            print('Błąd połączenia UART')

    # zresetowanie realizacji trajektori powoduje wyłączenie falownika oraz pompy
    # a także zresetowanie parametrów do wartości początkowych
    def reset(self):
        self.current_impuls = 0
        try:
            self.control_uart.write('D'.encode())
        except:
            print('Błąd połączenia UART')

        self.falownik_on(False)
        time.sleep(20)
        self.pump_on(False)
        self.reset = True

    # funkcja zwraca obecną pozycję frezarki
    def get_position(self):
        return [self.x, self.y, self.z]

    # funckja pozwala na ustawienie wartości pozycji frezarki
    def set_position(self, position):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]

    # wysłanie do mikrokontrolera znaku przerywającego ruch robota
    # dotyczy sterowania za pomocą przycisków
    def stop_moving(self):
        try:
            self.control_uart.write('ss'.encode())
        except:
            print('Błąd połączenia UART')

    # poniższe trzy funkcje wysyłają do mikrokontrolera sygnały rozpoczynające ruch
    # poszczególnych osi w zadanym kierunku

    def start_moving_x(self, direction):
        if direction == FORWARD:
            self.control_uart.write(X_FORWARD.encode())
        elif direction == BACKWARD:
            self.control_uart.write(X_BACKWARD.encode())


    def start_moving_y(self, direction):
        if direction == FORWARD:
            self.control_uart.write(Y_FORWARD.encode())
        elif direction == BACKWARD:
            self.control_uart.write(Y_BACKWARD.encode())


    def start_moving_z(self, direction):
        if direction == FORWARD:
            self.control_uart.write(Z_FORWARD.encode())
        elif direction == BACKWARD:
            self.control_uart.write(Z_BACKWARD.encode())


# generator służy do wyznaczania kolejnych punktów trajektorii na podstawie
# wybranych figur i zadanych parametrów
class Generator:

    # zmienne generatora potrzebne do niektórych kształtów
    # mają wartości domyślne, ale każdy z nich można zmienić w GUI
    plane_z = MAX_Z - MARGINES
    intake = INTAKE
    drill_diameter = DRILL_DIAMETER

    # lista wygenerowanych punktów
    generated_points = []


    def __init__(self):
        pass

    # ustawianie wartości płaszczyzny z dla realizacji figur 2D
    def set_plane(self, z_value):
        self.plane_z = z_value

    # ustawianie wartości wżeru dla funkcji wyrównującej powierzchnię
    def set_intake(self, intake_value):
        self.intake = intake_value

# poniższe funkcje na podstawie zadanych parametrów zwracają listę punktów, które
# połączone liniami prostymi tworzą pożądany kształt

    def line2D(self, point_1, point_2):
        points = []
        points.append([point_1[0], point_1[1], MAX_Z - MARGINES])
        points.append([point_1[0], point_1[1], self.plane_z])
        points.append([point_2[0], point_2[1], self.plane_z])
        points.append([point_2[0], point_2[1], MAX_Z - MARGINES])
        print(points)

        return points

    def line3D(self, point_1, point_2):
        points = []
        points.append([point_1[0], point_1[1], MAX_Z - MARGINES])
        points.append([point_1[0], point_1[1], point_1[2]])
        points.append([point_2[0], point_2[1], point_2[2]])
        points.append([point_2[0], point_2[1], MAX_Z - MARGINES])

        return points

    def rectangular2D(self, left_down_corner=None, up_right_corner=None, height=None, width=None):
        points = []

        if left_down_corner is not None and up_right_corner is not None:
            points.append([left_down_corner[0], left_down_corner[1], MAX_Z - MARGINES])
            points.append([left_down_corner[0], left_down_corner[1], self.plane_z])
            points.append([left_down_corner[0], up_right_corner[1], self.plane_z])
            points.append([up_right_corner[0], up_right_corner[1], self.plane_z])
            points.append([up_right_corner[0], left_down_corner[1], self.plane_z])
            points.append([left_down_corner[0], left_down_corner[1], self.plane_z])
            points.append([left_down_corner[0], left_down_corner[1], MAX_Z - MARGINES])

        elif left_down_corner is not None and height is not None and width is not None:
            points.append([left_down_corner[0], left_down_corner[1], MAX_Z - MARGINES])
            points.append([left_down_corner[0], left_down_corner[1], self.plane_z])
            points.append([left_down_corner[0], left_down_corner[1] + height, self.plane_z])
            points.append([left_down_corner[0] + width, left_down_corner[1] + height, self.plane_z])
            points.append([left_down_corner[0] + width, left_down_corner[1], self.plane_z])
            points.append([left_down_corner[0], left_down_corner[1], self.plane_z])
            points.append([left_down_corner[0], left_down_corner[1], MAX_Z - MARGINES])

        elif up_right_corner is not None and height is not None and width is not None:
            points.append([up_right_corner[0], up_right_corner[1], MAX_Z - MARGINES])
            points.append([up_right_corner[0], up_right_corner[1], self.plane_z])
            points.append([up_right_corner[0], up_right_corner[1] - height, self.plane_z])
            points.append([up_right_corner[0] - width, up_right_corner[1] - height, self.plane_z])
            points.append([up_right_corner[0] - width, up_right_corner[1], self.plane_z])
            points.append([up_right_corner[0], up_right_corner[1], self.plane_z])
            points.append([up_right_corner[0], up_right_corner[1], MAX_Z - MARGINES])

        return points

    def circle2D(self, center, radius, accuracy=0.1):
        points = []
        t = np.arange(0, 2 * math.pi, accuracy / radius)

        points.append([center[0] + radius * math.cos(t[0]), center[1] + radius * math.sin(t[0]), MAX_Z - MARGINES])

        for i in range(0, len(t), 1):
            points.append([center[0] + radius * math.cos(t[i]), center[1] + radius * math.sin(t[i]), self.plane_z])

        points.append([center[0] + radius * math.cos(t[-1]), center[1] + radius * math.sin(t[-1]), MAX_Z - MARGINES])

        return points

    # funkcja generująca punkty do wyrównywania powierzchni
    def flatten_surface(self, rect_1, z_of_surface, intake_=None, drill_diameter_=None):
        points = []
        finish_1 = False

        if intake_ is not None:
            intake = intake_
        else:
            intake = self.intake

        if drill_diameter_ is not None:
            drill_diameter = drill_diameter_
        else:
            drill_diameter = self.drill_diameter

        points.append([rect_1.left_down_corner[0], rect_1.left_down_corner[1], MAX_Z - MARGINES])
        points.append([rect_1.left_down_corner[0], rect_1.left_down_corner[1], rect_1.z])

        actual_x = rect_1.left_down_corner[0]
        actual_y = rect_1.left_down_corner[1]
        actual_z = rect_1.z
        width = rect_1.width

        while not finish_1:
            finish_2 = False

            # najpierw przejeżdżamy całą powierzchnię od krawędzi do krawędzi, przesuwając się o
            # wartość średnicy frezu pomniejszoną o pół milimera
            while not finish_2:
                actual_x += width
                points.append([actual_x, actual_y, actual_z])
                actual_y += drill_diameter - 0.5
                points.append([actual_x, actual_y, actual_z])
                actual_x -= width
                points.append([actual_x, actual_y, actual_z])
                actual_y += drill_diameter - 0.5
                points.append([actual_x, actual_y, actual_z])

                if actual_y - drill_diameter + 0.5 >= rect_1.up_right_corner[1]:
                    finish_2 = True

            points.append([actual_x, actual_y, MAX_Z - MARGINES])

            # jeżeli jeszcze nie osiągnęliśmy zadanej wysokości płaszczyzny, to przejeżdżamy do punktu
            # startowego i wykonujemy ten sam ruch, ale dla współrzędnej z pomniejszonej o
            # wartość wżeru (intake)
            if actual_z > z_of_surface:
                actual_x = rect_1.left_down_corner[0]
                actual_y = rect_1.left_down_corner[1]
                points.append([actual_x, actual_y, MAX_Z - MARGINES])

                if actual_z - intake > z_of_surface:
                    actual_z -= intake
                elif actual_z - intake <= z_of_surface:
                    actual_z = z_of_surface

                points.append([actual_x, actual_y, actual_z])

            else:
                finish_1 = True

        return points

