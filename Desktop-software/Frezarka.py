import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMenu, QLineEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from constants import *
from classes import *
from functions import *


class MainWindow(QMainWindow):
    # BUTTONS
    pybutton = object  # Choose option button
    button_1 = object  # x+ button
    button_2 = object  # x- button
    button_3 = object  # y- button
    button_4 = object  # y+ button
    button_5 = object  # z- button
    button_6 = object  # z+ button
    button_7 = object  # set intake button
    button_8 = object  # sez z-plane button
    button_9 = object  # set drill diameter button
    button_10 = object  # generate new path button
    button_11 = object  # add to existing path
    button_12 = object  # stop
    button_13 = object  # resume
    button_14 = object  # reset
    button_15 = object  # start
    button_16 = object  # generate tics
    button_17 = object  # simulate path

    # TEXT EDIT FIELDS
    text_edit_1 = object  # set intake field
    text_edit_2 = object  # set plane z field
    text_edit_3 = object  # ser drill diameter field
    text_edit_4 = object  # first point, x value
    text_edit_5 = object  # first point, y value
    text_edit_6 = object  # first point, z value
    text_edit_7 = object  # second point, x value
    text_edit_8 = object  # second point, y value
    text_edit_9 = object  # second point, z value
    text_edit_10 = object  # height value and radius value
    text_edit_11 = object  # width value
    text_edit_12 = object  # start z field
    text_edit_13 = object  # end z field
    text_edit_14 = object  # path to file field
    text_edit_15 = object  # file name field

    # LABELS
    label_1 = object  # 'position x: ' of frezarka
    label_2 = object  # 'position y: ' of frezarka
    label_3 = object  # 'position z: ' of frezarka
    label_4 = object  # 'start point: ' of line2D and 3D
    label_5 = object  # 'end point: ' of line2D and 3D
    label_6 = object  # 'x coordinate' field to fulfill
    label_7 = object  # 'y coordinate' field to fulfill
    label_8 = object  # 'z coordinate' field to fulfill
    label_9 = object  # 'left-down corner: ' of rectangular2D
    label_10 = object  # 'right-up corner: ' of rectangular2D
    label_11 = object  # 'height: ' of rectangular2D
    label_12 = object  # 'width: ' of rectangular2D
    label_13 = object  # 'center of circle: ' label
    label_14 = object  # 'radius: ' of circle label
    label_15 = object  # 'start z: ' of plane - flatten surface
    label_16 = object  # 'end z: ' of plane - flatten surface
    label_17 = object  # 'Ścieżka dostępu: ' while importing toolpath
    label_18 = object  # 'Nazwa pliku: ' while importing toolpath

    # MENU OF SHAPES OBJECTS
    shapes_menu = object  # rolled menu with options of shapes
    shapes_menu_line2d = object
    shapes_menu_line3d = object
    shapes_menu_rectangular2d = object
    shapes_menu_circle2d = object
    shapes_menu_flatten_surface = object
    shape_menu_import_file = object

    # OTHERS
    frezarka = object
    generator = object

    timer_1 = object  # timer due to refresh frezarka's position

    console = object  # pole tekstowe do komunikacji z użytkownikiem
    displayed_text = ''
    generated_ticks = []
    tics_to_send = []
    current_tick = 0
    stop = False
    move_ticks_thread = object

    def __init__(self):
        super().__init__()

        # OTHERS
        self.frezarka = Frezarka()
        self.generator = Generator()

        self.setWindowTitle("My App")
        self.setFixedSize(1920, 1080)

        self.console = QLabel(self)
        self.console.resize(500, 200)
        self.console.setText('Tutaj będą informacje od programu\n'
                             'bo można robić wiele linii')
        self.console.move(450, 600)
        self.console.setAlignment(Qt.AlignTop)
        self.console.setFont(QFont('Times', 18))
        self.console.setWordWrap(True)

        self.timer_1 = QTimer(self)
        self.timer_1.setInterval(250)
        self.timer_1.timeout.connect(self.refresh_position)
        self.timer_1.start()

        # LABELS DEFINITIONS
        self.label_1 = QLabel(self)
        self.label_1.setText('position x: ')
        self.label_1.resize(250, 30)
        self.label_1.move(POSITION_LABELS[0], POSITION_LABELS[1] - 60)
        self.label_1.setFont(QFont('Times', 18))

        self.label_2 = QLabel(self)
        self.label_2.setText('position y: ')
        self.label_2.resize(250, 30)
        self.label_2.move(POSITION_LABELS[0], POSITION_LABELS[1] - 30)
        self.label_2.setFont(QFont('Times', 18))

        self.label_3 = QLabel(self)
        self.label_3.setText('position z: ')
        self.label_3.resize(250, 30)
        self.label_3.move(POSITION_LABELS[0], POSITION_LABELS[1])
        self.label_3.setFont(QFont('Times', 18))

        self.label_4 = QLabel(self)
        self.label_4.setText('start point: ')
        self.label_4.move(MAIN_MENU[0] - 50, MAIN_MENU[1] + 50)
        self.label_4.setFont(QFont('Times', 14))

        self.label_5 = QLabel(self)
        self.label_5.setText('end point: ')
        self.label_5.move(MAIN_MENU[0] - 50, MAIN_MENU[1] + 100)
        self.label_5.setFont(QFont('Times', 14))

        self.label_6 = QLabel(self)
        self.label_6.setText('x coord')
        self.label_6.move(MAIN_MENU[0] + 100, MAIN_MENU[1])
        self.label_6.setFont(QFont('Times', 14))

        self.label_7 = QLabel(self)
        self.label_7.setText('y coord')
        self.label_7.move(MAIN_MENU[0] + 200, MAIN_MENU[1])
        self.label_7.setFont(QFont('Times', 14))

        self.label_8 = QLabel(self)
        self.label_8.setText('z coord')
        self.label_8.move(MAIN_MENU[0] + 300, MAIN_MENU[1])
        self.label_8.setFont(QFont('Times', 14))

        self.label_9 = QLabel(self)
        self.label_9.setText('left-down corner: ')
        self.label_9.move(MAIN_MENU[0] - 80, MAIN_MENU[1] + 50)
        self.label_9.setFont(QFont('Times', 14))
        self.label_9.resize(250, 30)

        self.label_10 = QLabel(self)
        self.label_10.setText('right-up corner: ')
        self.label_10.move(MAIN_MENU[0] - 80, MAIN_MENU[1] + 100)
        self.label_10.setFont(QFont('Times', 14))
        self.label_10.resize(250, 30)

        self.label_11 = QLabel(self)
        self.label_11.setText('height: ')
        self.label_11.move(MAIN_MENU[0] + 350, MAIN_MENU[1] + 50)
        self.label_11.setFont(QFont('Times', 14))

        self.label_12 = QLabel(self)
        self.label_12.setText('width: ')
        self.label_12.move(MAIN_MENU[0] + 350, MAIN_MENU[1] + 100)
        self.label_12.setFont(QFont('Times', 14))

        self.label_13 = QLabel(self)
        self.label_13.setText('center of circle: ')
        self.label_13.move(MAIN_MENU[0] - 80, MAIN_MENU[1] + 50)
        self.label_13.setFont(QFont('Times', 14))
        self.label_13.resize(250, 30)

        self.label_14 = QLabel(self)
        self.label_14.setText('radius: ')
        self.label_14.move(MAIN_MENU[0] + 350, MAIN_MENU[1] + 50)
        self.label_14.setFont(QFont('Times', 14))

        self.label_15 = QLabel(self)
        self.label_15.setText('start z: ')
        self.label_15.move(MAIN_MENU[0] - 50, MAIN_MENU[1] + 200)
        self.label_15.setFont(QFont('Times', 14))

        self.label_16 = QLabel(self)
        self.label_16.setText('end z: ')
        self.label_16.move(MAIN_MENU[0] - 50, MAIN_MENU[1] + 250)
        self.label_16.setFont(QFont('Times', 14))

        self.label_17 = QLabel(self)
        self.label_17.setFont(QFont('Times', 14))
        self.label_17.resize(250, 30)
        self.label_17.setText('Ścieżka dostępu: ')
        self.label_17.move(MAIN_MENU[0] - 80, MAIN_MENU[1] + 50)

        self.label_18 = QLabel(self)
        self.label_18.resize(250, 30)
        self.label_18.setText('Nazwa pliku: ')
        self.label_18.move(MAIN_MENU[0] - 80, MAIN_MENU[1] + 100)
        self.label_18.setFont(QFont('Times', 14))

        # BUTTONS DEFINITIONS
        self.pybutton = QPushButton('Choose option', self)
        self.pybutton.resize(300, 50)
        self.pybutton.move(50, 170)
        self.pybutton.setFont(QFont('Times', 18))

        self.button_1 = QPushButton('x+', self)
        self.button_1.resize(60, 60)
        self.button_1.move(MOVE_BUTTONS[0] + 70, MOVE_BUTTONS[1])
        self.button_1.pressed.connect(self.x_plus_pressed)
        self.button_1.released.connect(self.x_plus_released)
        self.button_1.setFont(QFont('Times', 26))

        self.button_2 = QPushButton('x-', self)
        self.button_2.resize(60, 60)
        self.button_2.move(MOVE_BUTTONS[0] - 70, MOVE_BUTTONS[1])
        self.button_2.pressed.connect(self.x_minus_pressed)
        self.button_2.released.connect(self.x_minus_released)
        self.button_2.setFont(QFont('Times', 26))

        self.button_3 = QPushButton('y-', self)
        self.button_3.resize(60, 60)
        self.button_3.move(MOVE_BUTTONS[0], MOVE_BUTTONS[1] + 70)
        self.button_3.pressed.connect(self.y_minus_pressed)
        self.button_3.released.connect(self.y_minus_released)
        self.button_3.setFont(QFont('Times', 26))

        self.button_4 = QPushButton('y+', self)
        self.button_4.resize(60, 60)
        self.button_4.move(MOVE_BUTTONS[0], MOVE_BUTTONS[1] - 70)
        self.button_4.pressed.connect(self.y_plus_pressed)
        self.button_4.released.connect(self.y_plus_released)
        self.button_4.setFont(QFont('Times', 26))

        self.button_5 = QPushButton('z-', self)
        self.button_5.resize(60, 60)
        self.button_5.move(MOVE_BUTTONS[0] + 150, MOVE_BUTTONS[1] + 40)
        self.button_5.pressed.connect(self.z_minus_pressed)
        self.button_5.released.connect(self.z_minus_released)
        self.button_5.setFont(QFont('Times', 26))

        self.button_6 = QPushButton('z+', self)
        self.button_6.resize(60, 60)
        self.button_6.move(MOVE_BUTTONS[0] + 150, MOVE_BUTTONS[1] - 40)
        self.button_6.pressed.connect(self.z_plus_pressed)
        self.button_6.released.connect(self.z_plus_released)
        self.button_6.setFont(QFont('Times', 26))

        self.button_7 = QPushButton('Set intake', self)
        self.button_7.resize(150, 40)
        self.button_7.move(SET_BUTTONS[0], SET_BUTTONS[1])
        self.button_7.clicked.connect(self.set_intake_button)
        self.button_7.setFont(QFont('Times', 18))

        self.button_8 = QPushButton('Set z plane', self)
        self.button_8.resize(150, 40)
        self.button_8.move(SET_BUTTONS[0], SET_BUTTONS[1] + 50)
        self.button_8.clicked.connect(self.set_plane_z_button)
        self.button_8.setFont(QFont('Times', 18))

        self.button_9 = QPushButton('Set drill diameter', self)
        self.button_9.resize(150, 40)
        self.button_9.move(SET_BUTTONS[0], SET_BUTTONS[1] + 100)
        self.button_9.clicked.connect(self.set_drill_diameter_button)
        self.button_9.setFont(QFont('Times', 14))

        self.button_10 = QPushButton('Generate new path', self)
        self.button_10.resize(300, 50)
        self.button_10.move(50, 50)
        self.button_10.clicked.connect(self.generate_new_path_button)
        self.button_10.setFont(QFont('Times', 18))

        self.button_11 = QPushButton('Add to existing path', self)
        self.button_11.resize(300, 50)
        self.button_11.move(50, 110)
        self.button_11.clicked.connect(self.add_to_path_button)
        self.button_11.setFont(QFont('Times', 18))

        self.button_12 = QPushButton('STOP', self)
        self.button_12.resize(200, 200)
        self.button_12.move(START_STOP[0] + 210, START_STOP[1])
        self.button_12.clicked.connect(self.stop_button)
        self.button_12.setFont(QFont('Times', 34))
        self.button_12.setEnabled(False)

        self.button_13 = QPushButton('RESUME', self)
        self.button_13.resize(200, 200)
        self.button_13.move(START_STOP[0] + 420, START_STOP[1])
        self.button_13.clicked.connect(self.resume_button)
        self.button_13.setFont(QFont('Times', 34))
        self.button_13.setEnabled(False)

        self.button_14 = QPushButton('RESET', self)
        self.button_14.resize(200, 200)
        self.button_14.move(START_STOP[0] + 630, START_STOP[1])
        self.button_14.clicked.connect(self.reset_button)
        self.button_14.setFont(QFont('Times', 34))
        self.button_14.setEnabled(False)

        self.button_15 = QPushButton('START', self)
        self.button_15.resize(200, 200)
        self.button_15.move(START_STOP[0], START_STOP[1])
        self.button_15.clicked.connect(self.start_button)
        self.button_15.setFont(QFont('Times', 34))

        self.button_16 = QPushButton('Generate ticks', self)
        self.button_16.resize(400, 100)
        self.button_16.move(START_STOP[0], START_STOP[1] - 120)
        self.button_16.clicked.connect(self.generate_ticks_button)
        self.button_16.setFont(QFont('Times', 32))

        self.button_17 = QPushButton('Simulate the path', self)
        self.button_17.resize(400, 100)
        self.button_17.move(START_STOP[0] + 420, START_STOP[1] - 120)
        self.button_17.clicked.connect(self.simulate_path_button)
        self.button_17.setFont(QFont('Times', 32))

        # TEXT EDIT FIELDS DEFINITIONS
        self.text_edit_1 = QLineEdit(self)
        self.text_edit_1.resize(150, 40)
        self.text_edit_1.move(SET_BUTTONS[0] + 160, SET_BUTTONS[1])

        self.text_edit_2 = QLineEdit(self)
        self.text_edit_2.resize(150, 40)
        self.text_edit_2.move(SET_BUTTONS[0] + 160, SET_BUTTONS[1] + 50)

        self.text_edit_3 = QLineEdit(self)
        self.text_edit_3.resize(150, 40)
        self.text_edit_3.move(SET_BUTTONS[0] + 160, SET_BUTTONS[1] + 100)

        self.text_edit_4 = QLineEdit(self)
        self.text_edit_4.resize(80, 40)
        self.text_edit_4.move(MAIN_MENU[0] + 90, MAIN_MENU[1] + 45)

        self.text_edit_5 = QLineEdit(self)
        self.text_edit_5.resize(80, 40)
        self.text_edit_5.move(MAIN_MENU[0] + 190, MAIN_MENU[1] + 45)

        self.text_edit_7 = QLineEdit(self)
        self.text_edit_7.resize(80, 40)
        self.text_edit_7.move(MAIN_MENU[0] + 90, MAIN_MENU[1] + 100)

        self.text_edit_8 = QLineEdit(self)
        self.text_edit_8.resize(80, 40)
        self.text_edit_8.move(MAIN_MENU[0] + 190, MAIN_MENU[1] + 100)

        self.text_edit_6 = QLineEdit(self)
        self.text_edit_6.resize(80, 40)
        self.text_edit_6.move(MAIN_MENU[0] + 290, MAIN_MENU[1] + 45)

        self.text_edit_9 = QLineEdit(self)
        self.text_edit_9.resize(80, 40)
        self.text_edit_9.move(MAIN_MENU[0] + 290, MAIN_MENU[1] + 100)

        self.text_edit_10 = QLineEdit(self)
        self.text_edit_10.resize(80, 40)
        self.text_edit_10.move(MAIN_MENU[0] + 420, MAIN_MENU[1] + 45)

        self.text_edit_11 = QLineEdit(self)
        self.text_edit_11.resize(80, 40)
        self.text_edit_11.move(MAIN_MENU[0] + 420, MAIN_MENU[1] + 100)

        self.text_edit_12 = QLineEdit(self)
        self.text_edit_12.resize(80, 40)
        self.text_edit_12.move(MAIN_MENU[0] + 50, MAIN_MENU[1] + 200)

        self.text_edit_13 = QLineEdit(self)
        self.text_edit_13.resize(80, 40)
        self.text_edit_13.move(MAIN_MENU[0] + 50, MAIN_MENU[1] + 250)

        self.text_edit_14 = QLineEdit(self)
        self.text_edit_14.resize(300, 40)
        self.text_edit_14.move(MAIN_MENU[0] + 90, MAIN_MENU[1] + 45)

        self.text_edit_15 = QLineEdit(self)
        self.text_edit_15.resize(300, 40)
        self.text_edit_15.move(MAIN_MENU[0] + 90, MAIN_MENU[1] + 100)

        # SHAPES MENU DEFINITIONS
        self.shapes_menu = QMenu(self)
        self.shapes_menu_line2d = self.shapes_menu.addAction('Line 2D')
        self.shapes_menu_line2d.setFont(QFont('Times', 18))
        self.shapes_menu_line2d.triggered.connect(self.shape_line2d)
        self.shapes_menu_line3d = self.shapes_menu.addAction('Line 3D')
        self.shapes_menu_line3d.setFont(QFont('Times', 18))
        self.shapes_menu_line3d.triggered.connect(self.shape_line3d)
        self.shapes_menu_rectangular2d = self.shapes_menu.addAction('Rectangular 2D')
        self.shapes_menu_rectangular2d.setFont(QFont('Times', 18))
        self.shapes_menu_rectangular2d.triggered.connect(self.shape_rectangular2d)
        self.shapes_menu_circle2d = self.shapes_menu.addAction('Circle 2D')
        self.shapes_menu_circle2d.setFont(QFont('Times', 18))
        self.shapes_menu_circle2d.triggered.connect(self.shape_circle2d)
        self.shapes_menu_flatten_surface = self.shapes_menu.addAction('Flatten surface')
        self.shapes_menu_flatten_surface.setFont(QFont('Times', 18))
        self.shapes_menu_flatten_surface.triggered.connect(self.shape_flatten_surface)
        self.shape_menu_import_file = self.shapes_menu.addAction('Import file')
        self.shape_menu_import_file.setFont(QFont('Times', 18))
        self.shape_menu_import_file.triggered.connect(self.shape_import_file)

        self.pybutton.setMenu(self.shapes_menu)
        self.hide_main_menu()

    # sterowanie frezarką za pomocą klawiszy wzdłuż zmiennej x

    def x_plus_pressed(self):
        self.frezarka.start_moving_x(FORWARD)

    def x_plus_released(self):
        self.frezarka.stop_moving()

    def x_minus_pressed(self):
        self.frezarka.start_moving_x(BACKWARD)

    def x_minus_released(self):
        self.frezarka.stop_moving()

    # sterowanie frezarką za pomocą klawiszy wzdłuż zmiennej y

    def y_plus_pressed(self):
        self.frezarka.start_moving_y(FORWARD)

    def y_plus_released(self):
        self.frezarka.stop_moving()

    def y_minus_pressed(self):
        self.frezarka.start_moving_y(BACKWARD)

    def y_minus_released(self):
        self.frezarka.stop_moving()

    # sterowanie frezarką za pomocą klawiszy wzdłuż zmiennej z

    def z_plus_pressed(self):
        self.frezarka.start_moving_z(FORWARD)

    def z_plus_released(self):
        self.frezarka.stop_moving()

    def z_minus_pressed(self):
        self.frezarka.start_moving_z(BACKWARD)

    def z_minus_released(self):
        self.frezarka.stop_moving()

    # obsługa przycisków

    # obsługa przycisku do dodawanie kolejnych punktów do generowanej ścieżki
    # w zależności od obecnie wybranej opcji wykonuje się blok kodu z nią związany
    def add_to_path_button(self):

        if self.pybutton.text() == 'Line 2D':
            try:
                start_x = float(self.text_edit_4.text())
                start_y = float(self.text_edit_5.text())
                stop_x = float(self.text_edit_7.text())
                stop_y = float(self.text_edit_8.text())
                point_start = [start_x, start_y]
                point_stop = [stop_x, stop_y]
                self.generator.generated_points.extend(self.generator.line2D(point_start, point_stop))
                self.printc('Line 2D poprawnie wygenerowane')
            except:
                self.printc('Niepoprawne wartości współrzędnych dla Line 2D')

        elif self.pybutton.text() == 'Line 3D':
            try:
                start_x = float(self.text_edit_4.text())
                start_y = float(self.text_edit_5.text())
                start_z = float(self.text_edit_6.text())
                stop_x = float(self.text_edit_7.text())
                stop_y = float(self.text_edit_8.text())
                stop_z = float(self.text_edit_9.text())
                point_start = [start_x, start_y, start_z]
                point_stop = [stop_x, stop_y, stop_z]
                self.generator.generated_points.extend(self.generator.line3D(point_start, point_stop))
                self.printc('Line 3D poprawnie wygenerowane')
            except:
                self.printc('Niepoprawne wartości współrzędnych dla Line 3D')

        elif self.pybutton.text() == 'Rectangular 2D':
            # prostokąt można wygenerować na kilka sposobów, można wprowadzić:
            # - współrzędną lewego dolnego rogu
            # - współrzędną prawego górnego rogu
            # - wysokość oraz szerokość
            # wprowadzenie dwóch z powyższych pozwala na wygenerowanie prostokąta
            check = 0
            try:
                left_down_x = float(self.text_edit_4.text())
                left_down_y = float(self.text_edit_5.text())
                check += 100
            except:
                pass

            try:
                right_up_x = float(self.text_edit_7.text())
                right_up_y = float(self.text_edit_8.text())
                check += 10
            except:
                pass

            try:
                height = float(self.text_edit_10.text())
                width = float(self.text_edit_11.text())
                check += 1
            except:
                pass

            if check == 110:
                left_down = [left_down_x, left_down_y]
                right_up = [right_up_x, right_up_y]
                self.generator.generated_points.extend(self.generator.rectangular2D(left_down_corner=left_down,
                                                                                    up_right_corner=right_up))
                self.printc('Rectangular 2D poprawnie wygenerowane')

            elif check == 101:
                left_down = [left_down_x, left_down_y]
                self.generator.generated_points.extend(self.generator.rectangular2D(left_down_corner=left_down,
                                                                                    height=height, width=width))
                self.printc('Rectangular 2D poprawnie wygenerowane')

            elif check == 11:
                right_up = [right_up_x, right_up_y]
                self.generator.generated_points.extend(self.generator.rectangular2D(up_right_corner=right_up,
                                                                                    height=height, width=width))
                self.printc('Rectangular 2D poprawnie wygenerowane')

            else:
                self.printc('Niepoprawne wartości współrzędnych dla Rectangular 2D')

        elif self.pybutton.text() == 'Circle 2D':
            try:
                center = [float(self.text_edit_4.text()), float(self.text_edit_5.text())]
                radius = float(self.text_edit_10.text())
                self.generator.generated_points.extend(self.generator.circle2D(center, radius))
                self.printc('Circle 2D poprawnie wygenerowane')
            except:
                self.printc('Niepoprawne wartości współrzędnych dla Circle 2D')

        elif self.pybutton.text() == 'Flatten surface':
            check = 0
            try:
                left_down_x = float(self.text_edit_4.text())
                left_down_y = float(self.text_edit_5.text())
                check += 100
            except:
                pass

            try:
                right_up_x = float(self.text_edit_7.text())
                right_up_y = float(self.text_edit_8.text())
                check += 10
            except:
                pass

            try:
                height = float(self.text_edit_10.text())
                width = float(self.text_edit_11.text())
                check += 1
            except:
                pass

            try:
                start_z = float(self.text_edit_12.text())
                stop_z = float(self.text_edit_13.text())
                check += 1000
            except:
                pass

            rect = object
            self.printc(str(check))

            if check == 1110:
                left_down = [left_down_x, left_down_y]
                right_up = [right_up_x, right_up_y]
                if left_down_x < right_up_x and left_down_y < right_up_y:
                    rect = Rectangular(start_z, left_down_corner=left_down, up_right_corner=right_up)
                else:
                    check = -1

            elif check == 1101:
                left_down = [left_down_x, left_down_y]
                if left_down_x + width <= MAX_X and left_down_y + height <= MAX_Y:
                    rect = Rectangular(start_z, left_down_corner=left_down, height=height, width=width)
                else:
                    check = -1

            elif check == 1011:
                right_up = [right_up_x, right_up_y]
                if right_up_x - width >= 0 and right_up_y - height >= 0:
                    rect = Rectangular(start_z, up_right_corner=right_up, height=height, width=width)
                else:
                    check = -1

            else:
                check = -1

            # jeżeli wprowadzone zostały poprawne dane
            if check != -1 and check != 0 and start_z >= stop_z:
                self.generator.generated_points.extend(self.generator.flatten_surface(rect, stop_z))
                self.printc('Flatten surface poprawnie wygenerowane')
            else:
                self.printc('Niepoprawne wartości współrzędnych dla Flatten surface')

        elif self.pybutton.text() == 'Import file':
            import_path = str(self.text_edit_14.text())
            file_name = str(self.text_edit_15.text())

            try:
                if import_path == '':
                    self.generator.generated_points.extend(read_data(file_name))
                else:
                    self.generator.generated_points.extend(read_data(file_name, import_path))
                self.printc('Zaimportowano dane poprawnie.')
            except:
                self.printc('Niepoprawna nazwa pliku, lub ścieżka dostępu! Spróbój ponownie')

        else:
            self.printc('Należy wybrać jedną z opcji i wprowadzić dane!')

    # obsługa przycisku generacji nowej ścieżki
    # czyści listę wygenerowanych wcześniej punktów i wywołuje funkcję add_to_path_button()
    def generate_new_path_button(self):
        self.generator.generated_points = []
        self.add_to_path_button()

    # obsługa przycosku do ustawiania wżeru frezarki
    def set_intake_button(self):
        try:
            self.generator.intake = float(self.text_edit_1.text())
            self.printc('Obecnie ustawiona wartość intake: ' + str(self.generator.intake))
        except:
            self.printc('Zła wartość, ' + 'obecnie ustwaiona wartość intake: ' + str(self.generator.intake))

    # obsługa przycisku do ustawiania płaszczyzny działania dla wszystkich figur 2D
    def set_plane_z_button(self):
        try:
            plane_z = float(self.text_edit_2.text())
            # jeżeli ustawiana wartość mieści się w granicach obszaru roboczego
            if MIN_Z <= plane_z <= MAX_Z:
                self.generator.plane_z = plane_z
                self.printc('Obecnie ustawiona wartość plane z: ' + str(self.generator.plane_z))
            else:
                self.printc('Zła wartość, obecnie ustawiona wartość plane z: ' + str(self.generator.plane_z))
        except:
            self.printc('Zła wartość, obecnie ustawiona wartość plane z: ' + str(self.generator.plane_z))

    # obsługa przycisku do ustawiania średnicy narzędzia frezującego
    # jest to parametr potrzebny do funkcji wyrównywania powierzchni
    def set_drill_diameter_button(self):
        try:
            self.generator.drill_diameter = float(self.text_edit_3.text())
            self.printc('Obecnie ustawiona wartość drill diameter: ' + str(self.generator.drill_diameter))
        except:
            self.printc(
                'Zła wartość, ' + 'obecnie ustawiona wartość drill diameter: ' + str(self.generator.drill_diameter))

    # obsuga przycisku START
    def start_button(self):
        self.frezarka.current_impuls = 0    # zeruję wskaźnik wysyłanej paczki impulsów
        self.frezarka.more = True           # i ustawiam parametr pozwalający na wysłanie
                                            # listy kroków do mikrokontrolera
        self.move_ticks_thread = threading.Thread(target=self.move_ticks)
        self.move_ticks_thread.start()      # uruchamiam obsługę zadanej ścieżki w osobnym wątku programu
        self.button_12.setEnabled(True)
        self.button_13.setEnabled(False)
        self.button_14.setEnabled(False)
        self.button_15.setEnabled(False)

    # obsługa przycisku STOP
    def stop_button(self):
        self.frezarka.stop()                # wywołuję odpowiednią metodę klasy frezarka
        self.button_12.setEnabled(False)
        self.button_13.setEnabled(True)
        self.button_14.setEnabled(True)
        self.button_15.setEnabled(False)

    # obsługa przycisku RESUME
    def resume_button(self):
        self.move_ticks_thread = threading.Thread(target=self.move_ticks)
        self.move_ticks_thread.start()      # uruchamiam ponownie wątek zatrzymany po naciśnięciu przyciku STOP
        self.frezarka.resume()              # i wywołują odpowiednią metodę klasy frezarka
        self.button_12.setEnabled(True)
        self.button_13.setEnabled(False)
        self.button_14.setEnabled(False)
        self.button_15.setEnabled(False)

    # obsługa przycisku RESET
    def reset_button(self):
        self.frezarka.reset()              # przekazanie obsługi do klasy frezarka
        self.button_12.setEnabled(False)
        self.button_13.setEnabled(False)
        self.button_14.setEnabled(False)
        self.button_15.setEnabled(True)

    # obsługa przycisku do generowania impulsów na sterowniki
    def generate_ticks_button(self):
        self.tics_to_send = []      # wyzerowanie obecnej listy impulsów

        # jeżeli lista wygenerowanych punktów nie jest pusta
        if len(self.generator.generated_points) > 0:
            start = self.frezarka.get_position()    # pobieram aktualną pozycję frezarki
            # i generuję impulsy pozwalające na jej zrealizowanie
            self.generated_ticks = generate_impuls(self.generator.generated_points, start)

            # nastęnie dzielę wygenerowane impulsy na paczki zawierające 1000 kroków silnika
            while self.current_tick < len(self.generated_ticks):
                seria = ''
                for i in range(0, 1000, 1):
                    if self.current_tick < len(self.generated_ticks):
                        if self.generated_ticks[self.current_tick] == (FORWARD, STILL, STILL):
                            seria += 'X'
                        elif self.generated_ticks[self.current_tick] == (BACKWARD, STILL, STILL):
                            seria += 'x'
                        elif self.generated_ticks[self.current_tick] == (STILL, FORWARD, STILL):
                            seria += 'Y'
                        elif self.generated_ticks[self.current_tick] == (STILL, BACKWARD, STILL):
                            seria += 'y'
                        elif self.generated_ticks[self.current_tick] == (STILL, STILL, FORWARD):
                            seria += 'Z'
                        elif self.generated_ticks[self.current_tick] == (STILL, STILL, BACKWARD):
                            seria += 'z'

                        self.current_tick += 1

                # i tworzę listę zawierającą paczki po 1000 impulsów
                self.tics_to_send.append(seria)

            self.printc('Poprawnie wygenerowano impulsy')
            self.frezarka.impulses = self.tics_to_send
        else:
            self.printc('Nie podano żadnej ścieżki narzędzia')

    # obsługa przycisku do symulacji ścieżki narzędzia
    def simulate_path_button(self):
        try:
            # wykorzystuję funkcję z innego pliku do wygenerowania wykresu ścieżki robota
            plot_toolpath(self.generator.generated_points, self.generated_ticks, self.frezarka.get_position())
            self.printc('Ścieżka wyświetlona poprawnie')
        except:
            self.printc('Nie można wyświetlić wygenerowanej ścieżki')


    # poniższa seria funkcji służy do wyświetlania i ukrywania odpowiednich pół do wpisywania danych
    # mowa o funkcjach zaczynających się od "shape_..."

    def shape_line2d(self):
        self.pybutton.setText('Line 2D')
        self.hide_main_menu()
        self.label_4.show()
        self.label_5.show()
        self.label_6.show()
        self.label_7.show()
        self.text_edit_4.show()
        self.text_edit_5.show()
        self.text_edit_7.show()
        self.text_edit_8.show()

    def shape_line3d(self):
        self.pybutton.setText('Line 3D')
        self.hide_main_menu()
        self.label_4.show()
        self.label_5.show()
        self.label_6.show()
        self.label_7.show()
        self.label_8.show()
        self.text_edit_4.show()
        self.text_edit_5.show()
        self.text_edit_6.show()
        self.text_edit_7.show()
        self.text_edit_8.show()
        self.text_edit_9.show()

    def shape_rectangular2d(self):
        self.pybutton.setText('Rectangular 2D')
        self.hide_main_menu()
        self.label_9.show()
        self.label_10.show()
        self.label_11.show()
        self.label_12.show()
        self.label_6.show()
        self.label_7.show()
        self.text_edit_4.show()
        self.text_edit_5.show()
        self.text_edit_7.show()
        self.text_edit_8.show()
        self.text_edit_10.show()
        self.text_edit_11.show()

    def shape_circle2d(self):
        self.pybutton.setText('Circle 2D')
        self.hide_main_menu()
        self.label_13.show()
        self.label_14.show()
        self.label_6.show()
        self.label_7.show()
        self.text_edit_4.show()
        self.text_edit_5.show()
        self.text_edit_10.show()

    def shape_flatten_surface(self):
        self.pybutton.setText('Flatten surface')
        self.hide_main_menu()
        self.label_9.show()
        self.label_10.show()
        self.label_11.show()
        self.label_12.show()
        self.label_15.show()
        self.label_16.show()
        self.label_6.show()
        self.label_7.show()
        self.text_edit_4.show()
        self.text_edit_5.show()
        self.text_edit_7.show()
        self.text_edit_8.show()
        self.text_edit_10.show()
        self.text_edit_11.show()
        self.text_edit_12.show()
        self.text_edit_13.show()

    def shape_import_file(self):
        self.pybutton.setText('Import file')
        self.hide_main_menu()
        self.label_17.show()
        self.label_18.show()
        self.text_edit_15.show()
        self.text_edit_14.show()

    # funkcja uruchamiana zawsze w osobnym wątku, służąca
    # do wykonywania zadanej trajektorii przez robota
    def move_ticks(self):
        self.frezarka.start()

    # funkcja odświeżająca informację o pozycji frezarki
    def refresh_position(self):
        try:
            # wysłanie znaku 'd' do mikrokontrolera powoduje odesłanie
            # w informacji zwrotnej położenia frezarki
            self.frezarka.control_uart.write('d'.encode())
        except:
            pass

        self.label_1.setText('position x:  ' + str(self.frezarka.x))
        self.label_2.setText('position y:  ' + str(self.frezarka.y))
        self.label_3.setText('position z:  ' + str(self.frezarka.z))

    # funkcja do wypisywania komunikatów dla użytkownika w oknie aplikacji - GUI
    def printc(self, text):
        self.displayed_text = text + '\n\n' + self.displayed_text
        self.console.setText(self.displayed_text)

    # funckja do ukrywania pól do wprowadzania parametrów i ich oznaczeń
    def hide_main_menu(self):
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label_10.hide()
        self.label_11.hide()
        self.label_12.hide()
        self.label_13.hide()
        self.label_14.hide()
        self.label_15.hide()
        self.label_16.hide()
        self.label_17.hide()
        self.label_18.hide()
        self.text_edit_4.hide()
        self.text_edit_5.hide()
        self.text_edit_6.hide()
        self.text_edit_7.hide()
        self.text_edit_8.hide()
        self.text_edit_9.hide()
        self.text_edit_10.hide()
        self.text_edit_11.hide()
        self.text_edit_12.hide()
        self.text_edit_13.hide()
        self.text_edit_14.hide()
        self.text_edit_15.hide()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

