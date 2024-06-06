# zakres obszaru roboczego
MAX_X = 1700.0
MIN_X = 0.0
MAX_Y = 2500.0
MIN_Y = 0.0
MAX_Z = 110.0
MIN_Z = 0.0

# numery portów wirtualnych łącza szeregowego
data_uart_com = 'COM6'      # dla danych
control_uart_com = 'COM7'   # dla sygnałów sterujących

# odległość w milimetrach na jaką przesunie się poszczególna oś dla jednego zadanego impulsu na sterownik
# dla osi x i y oraz dla dwóch impulsów w przypadku osi z
# kolejne elementy odpowiadają odpowiednio [osi x, osi y, osi z]
ACCURACY = [0.0125, 0.0125, 0.01]

# stałe zwiększające czytelność programu
X = 'x'
Y = 'y'
Z = 'z'
FORWARD = 'f'
BACKWARD = 'b'
STILL = '0'
X_FORWARD = 'X'
X_BACKWARD = 'x'
Y_FORWARD = 'Y'
Y_BACKWARD = 'y'
Z_FORWARD = 'Z'
Z_BACKWARD = 'z'

# standardowe wartości poniższych parametrów są wykorzystywane
# jeżeli użytkownik ich sam nie wprowadzi
MARGINES = 0.0
DRILL_DIAMETER = 20.0
INTAKE = 2.0

# stałe określające położenie poszczególnych bloków w widoku użytkownika
MOVE_BUTTONS = [1600, 100]          # przyciski do poruszania
POSITION_LABELS = [1100, 100]       # etykiety informujące o lokalizacji
SET_BUTTONS = [100, 700]            # przyciski do ustawiania INTAKE, Z PLANE oraz DRILL DIAMETER
MAIN_MENU = [470, 50]               # główne menu
START_STOP = [1000, 700]            # przyciski do generacji impulsów, wyświetlania ścieżki
                                    # oraz obsługi wygenerowanej trajektorii

