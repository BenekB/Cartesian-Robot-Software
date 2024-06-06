import matplotlib.pyplot as plt
from classes import *
from constants import *


# funkcja do wczytywania zewnętrznych danych z pliku
def read_data(name, path='0'):

    # jeżeli ścieżka dostępu nie została podana, to szukamy w tej samej lokalizacji co skrypt
    if path == '0':
        file = open(name, 'r')
    # w przeciwnym wypadku uwzględniamy ścieżkę dostępu
    else:
        file = open(path + '/' + name)

    data = []
    lines = file.readlines()

    # przekształcamy dane w taki sposób, aby ostrzymać listę trójwymiarowych współrzędnych
    for line in lines:
        coor = line.replace('\n', '')
        splitted = coor.split(';')
        floated = []

        for elem in splitted:
            floated.append(float(elem))

        data.append(floated)

    # dodajemy jeszcze punkty początkowe oraz końcowe i zwracamy instrukcji wywołującej
    data_exceeded = []
    data_exceeded.append([data[0][0], data[0][1], MAX_Z - MARGINES])
    data_exceeded.extend(data)
    data_exceeded.append([data[-1][0], data[-1][1], MAX_Z - MARGINES])

    return data_exceeded


# funkcja służy do obliczenia odległości punktu od prostej
def count_distance(line, point):
    # obliczamy najpierw współczynnik D płaszczyzny prostopadłej
    # do prostej i przechodzącej przez sprawdzany punkt
    D = - line[0][1] * point[0] - line[1][1] * point[1] - line[2][1] * point[2]

    # następnie obliczamy parametr t prostej przedstawionej parametrycznie, dla którego otrzymamy punkt
    # przecięcia obliczonej wcześniej płaszczyzny z tą prostą
    t = - (D + line[0][1] * line[0][0] + line[1][1] * line[1][0] + line[2][1] * line[2][0]) / \
        (line[0][1]**2 + line[1][1]**2 + line[2][1]**2)

    # posiadając parametr t wyznaczamy punkt przecięcia prostej przez płaszczyznę
    new_point = [line[0][0] + line[0][1] * t,
                 line[1][0] + line[1][1] * t,
                 line[2][0] + line[2][1] * t]

    # następnie obliczamy odległość punktu przecięcia płaszczyzny z prostą od punktu sprawdzanego
    distance = math.sqrt((new_point[0] - point[0])**2 + (new_point[1] - point[1])**2 + (new_point[2] - point[2])**2)

    return [distance, line]


# funkcja zamienia informację o odcinku w przestrzeni na listę kroków silników
# pozwalającą takowe przemieszczenie otrzymać
def coord_to_tics(first, second, accuracy=ACCURACY):

    # obliczam odległość od punktu początkowego do docelowego
    dest_distance = math.sqrt((first[0] - second[0])**2 + (first[1] - second[1])**2 + (first[2] - second[2])**2)

    # oraz zamieniam punkty na poszczególne współrzędne
    o_x0 = first[0]
    o_y0 = first[1]
    o_z0 = first[2]
    o_x1 = second[0]
    o_y1 = second[1]
    o_z1 = second[2]

    line = [[o_x0, o_x1-o_x0], [o_y0, o_y1-o_y0], [o_z0, o_z1-o_z0]]    # współczynniki równania parametrycznego prostej
    tick_list = []
    point_to_line_distance = [object, object]
    point_to_point_distance = [object, object]
    finish = False

    # pętla znajdująca kolejne kroki silników
    while not finish:
        distances = []

        # sprawdzam lokalizację robota po wykonaniu ruchu do przodu w osi x
        x0 = o_x0 + accuracy[0]
        y0 = o_y0
        z0 = o_z0
        # wyznaczam lokalizację robota po takim ruchu
        point = [x0, y0, z0]
        # obliczam odległość nowej lokalizacji od prostej łączącej punkt początkowy i końcowy
        point_to_line_distance[0] = count_distance(line, point, second)
        # obliczam odległość nowej lokalizacji od punktu końcowego
        point_to_point_distance[0] = math.sqrt((o_x1 - x0)**2 + (o_y1 - y0)**2 + (o_z1 - z0)**2)

        # analogicznie jak powyżej, tylko ruch odbywa się w przeciwnym kierunku
        x0 = o_x0 - accuracy[0]
        y0 = o_y0
        z0 = o_z0
        point = [x0, y0, z0]
        point_to_line_distance[1] = count_distance(line, point, second)
        point_to_point_distance[1] = math.sqrt((o_x1 - x0)**2 + (o_y1 - y0)**2 + (o_z1 - z0)**2)

        # gdy mamy już dwie możliwe lokalizacje, dla kroku w jedną oraz druga strone w osi x, to sprawdam
        # która z lokalizacji znajduje się bliżej punktu końcowego i ją zapamiętuję w liście "distances"
        if point_to_point_distance[0] < point_to_point_distance[1]:
            distances.append([point_to_line_distance[0], (FORWARD, STILL, STILL), point_to_point_distance[0]])
        else:
            distances.append([point_to_line_distance[1], (BACKWARD, STILL, STILL), point_to_point_distance[1]])

#--------------------------------------------------------------------------------------------------------------------

        # jak wyżej, tylko dla osi y
        x0 = o_x0
        y0 = o_y0 + accuracy[1]
        z0 = o_z0
        point = [x0, y0, z0]
        point_to_line_distance[0] = count_distance(line, point, second)
        point_to_point_distance[0] = math.sqrt((o_x1 - x0)**2 + (o_y1 - y0)**2 + (o_z1 - z0)**2)

        x0 = o_x0
        y0 = o_y0 - accuracy[1]
        z0 = o_z0
        point = [x0, y0, z0]
        point_to_line_distance[1] = count_distance(line, point, second)
        point_to_point_distance[1] = math.sqrt((o_x1 - x0)**2 + (o_y1 - y0)**2 + (o_z1 - z0)**2)

        if point_to_point_distance[0] < point_to_point_distance[1]:
            distances.append([point_to_line_distance[0], (STILL, FORWARD, STILL), point_to_point_distance[0]])
        else:
            distances.append([point_to_line_distance[1], (STILL, BACKWARD, STILL), point_to_point_distance[1]])

#--------------------------------------------------------------------------------------------------------------------

        # jak wyżej, tylko dla osi z
        x0 = o_x0
        y0 = o_y0
        z0 = o_z0 + accuracy[2]
        point = [x0, y0, z0]
        point_to_line_distance[0] = count_distance(line, point, second)
        point_to_point_distance[0] = math.sqrt((o_x1 - x0)**2 + (o_y1 - y0)**2 + (o_z1 - z0)**2)

        x0 = o_x0
        y0 = o_y0
        z0 = o_z0 - accuracy[2]
        point = [x0, y0, z0]
        point_to_line_distance[1] = count_distance(line, point, second)
        point_to_point_distance[1] = math.sqrt((o_x1 - x0)**2 + (o_y1 - y0)**2 + (o_z1 - z0)**2)

        if point_to_point_distance[0] < point_to_point_distance[1]:
            distances.append([point_to_line_distance[0], (STILL, STILL, FORWARD), point_to_point_distance[0]])
        else:
            distances.append([point_to_line_distance[1], (STILL, STILL, BACKWARD), point_to_point_distance[1]])


        min_dist = distances[0][0][0]
        index = 0

        # sprawdzam który z trzech wyznaczonych punktów jest najbliżej prostej przechodzącej przez
        # punkt początkowy oraz końcowy
        # zapamiętuję jego indeks w tablicy
        for i in range(1, len(distances), 1):
            if distances[i][0][0] < min_dist:
                min_dist = distances[i][0][0]
                index = i

        # sprawdzam warunek dotarcia do punktu końcowego, czyli czy w tej iteracji pętli udało się znaleźć
        # punkt o mniejszej odległości do punktu końcowego niż w poprzedniej iteracji
        if distances[index][2] < dest_distance:
            # jeżeli tak, to wpisuję ten impuls na listę
            tick_list.append(distances[index][1])

            x_tick = distances[index][1][0]
            y_tick = distances[index][1][1]
            z_tick = distances[index][1][2]

            line = distances[index][0][1].copy()

            # w zależności od tego w jakiej osi w którym kierunku nastąpił krok silnika,
            # odpowiednia współrzędna jest zmieniana
            if x_tick == FORWARD:
                o_x0 = o_x0 + accuracy[0]
            elif x_tick == BACKWARD:
                o_x0 = o_x0 - accuracy[0]

            if y_tick == FORWARD:
                o_y0 = o_y0 + accuracy[1]
            elif y_tick == BACKWARD:
                o_y0 = o_y0 - accuracy[1]

            # podział kroków w osi z jest większy niż w pozostałych osiach, więc dodaję
            # podwójny krok w tej osi, aby osiągnąć ostatecznie pożądany efekt
            if z_tick == FORWARD:
                o_z0 = o_z0 + accuracy[2]
                tick_list.append(distances[index][1])
            elif z_tick == BACKWARD:
                o_z0 = o_z0 - accuracy[2]
                tick_list.append(distances[index][1])

            dest_distance = distances[index][2]

        else:
            finish = True

    return tick_list, [o_x0, o_y0, o_z0]


# generuje ścieżkę od zadanego punktu startowego poprzez kolejne punkty z listy data
def generate_impuls(data, start_position):
    pos = Position()
    pos.x = start_position[0]
    pos.y = start_position[1]
    pos.z = start_position[2]

    tick_list = []
    first = [pos.x, pos.y, pos.z]       # rzeczywisty punkt początkowy

    # wywołuję funkcję coord_to_tics dla kolejnych punktów z listy data oraz łączę w jedną całość
    # otrzymane listy kroków silników
    for i in range(0, len(data), 1):
        if first != data[i]:
            ticks, first = coord_to_tics(first, data[i])
            tick_list.extend(ticks)

    return tick_list


# rysuje ścieżkę narzędzia wygenerowaną przez program oraz ścieżkę zadaną (pożądaną)
def plot_toolpath(desired_path, tool_ticks, start_position, accuracy=ACCURACY):
    # desired_path - kolejne punkty tworzące trajektorię pożądaną
    # tool_ticks - lista ruchów silnika krokowego
    x_start = []
    y_start = []
    z_start = []

    desired_x = []
    desired_y = []
    desired_z = []

    x_start.append(start_position[0])
    y_start.append(start_position[1])
    z_start.append(start_position[2])

    # zamieniam listę kroków na kolejne punkty w przestrzeni osiągane przez końcówkę roboczą
    for i in range(0, len(tool_ticks), 1):
        if tool_ticks[i][0] == FORWARD:
            x_start.append(x_start[-1] + accuracy[0])
            y_start.append(y_start[-1])
            z_start.append(z_start[-1])
        elif tool_ticks[i][0] == BACKWARD:
            x_start.append(x_start[-1] - accuracy[0])
            y_start.append(y_start[-1])
            z_start.append(z_start[-1])
        elif tool_ticks[i][1] == FORWARD:
            x_start.append(x_start[-1])
            y_start.append(y_start[-1] + accuracy[1])
            z_start.append(z_start[-1])
        elif tool_ticks[i][1] == BACKWARD:
            x_start.append(x_start[-1])
            y_start.append(y_start[-1] - accuracy[1])
            z_start.append(z_start[-1])
        elif tool_ticks[i][2] == FORWARD:
            x_start.append(x_start[-1])
            y_start.append(y_start[-1])
            z_start.append(z_start[-1] + accuracy[2])
        elif tool_ticks[i][2] == BACKWARD:
            x_start.append(x_start[-1])
            y_start.append(y_start[-1])
            z_start.append(z_start[-1] - accuracy[2])

    for i in range(0, len(desired_path), 1):
        desired_x.append(desired_path[i][0])
        desired_y.append(desired_path[i][1])
        desired_z.append(desired_path[i][2])

    # rysuję wykresy ścieżki pożądanej i wygenerowanej na podstawie impulsów
    ax = plt.axes(projection='3d')
    ax.set_xlim([0, 2000])
    ax.set_ylim([0, 2000])
    ax.set_zlim([0, 2000])
    ax.plot3D(x_start, y_start, z_start)
    ax.plot3D(desired_x, desired_y, desired_z)

    plt.show()

