/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "i2c.h"
#include "spi.h"
#include "tim.h"
#include "usart.h"
#include "usb.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <string.h>
#include "receive_uart.h"
#include "send_uart.h"
#define true 'T'
#define false 'F'

// zmienne i flagi obsługujące program
uint8_t receive_buffer;
uint8_t receive_buffer5;
uint8_t received_tab[5];
uint8_t received[3];
int received_data = -1;
int bufor_elements = 0;
int bufor_elements5 = 0;
int abc = 0;
int czy = 0;
int send = 0;
char stop = false;
char start = false;
char already_send = true;
int x_position = 17000000;
int y_position = 0;
int z_position = 1100000;
char receive_next = true;
char actual_byte = '!';
char actual_byte5 = '!';
char next_step = false;
int interval = 595;
char release = true;
int licznik = 0;
int licznik1 = 0;
int time = 0;
int overtime = 0;
char what_move = '!';
char start_moving = false;
int interval_2 = 1495;
int decreasing = 30;
char cont = true;


/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */


// funckja wywoływana po odebraniu całej paczki danych
void user_uart_handler(UART_HandleTypeDef *huart)
{
	if(__HAL_UART_GET_FLAG(&huart4, UART_FLAG_IDLE))   // jeżeli jest to przerwanie informujące o ciszy na łączu dla UART4
	{
	  	__HAL_UART_CLEAR_IDLEFLAG(&huart4);            // zerujemy flagę tego przerwania
	}

	if(__HAL_UART_GET_FLAG(&huart5, UART_FLAG_IDLE))   // jeżeli jest to przerwanie informujące o ciszy na łączu dla UART4
	{
		__HAL_UART_CLEAR_IDLEFLAG(&huart5);				// zerujemy flagę tego przerwania
	}
}


// funkcja właczająca pompę chłodziwa
void turn_on_pump()
{
	// ustawienie tego pinu w stanie niskim powoduje włączenie pompy
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_14, GPIO_PIN_RESET);
}


// funkcja wyłączająca pompę chłodziwa
void turn_off_pump()
{
	// ustawienie tego pinu w stanie wysokim powoduje wyłączenie pompy
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_14, GPIO_PIN_SET);
}


// funkcja włączająca falownik silnika frezarki
void turn_falownik_on()
{
	// ustawienie tego pinu w stanie niskim powoduje włączenie silnika frezarki
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_15, GPIO_PIN_RESET);
}


// funkcja wyłączająca falownik silnika frezarki
void turn_falownik_off()
{
	// ustawienie tego pinu w stanie wysokim powoduje wyłączenie silnika frezarki
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_15, GPIO_PIN_SET);
}


// funkcja wysyłająca aktualną lokalizację narzędzia frezującego
void send_location()
{
	char location[] = "123456789012345";
	location[0] = 'x';							// po znaku x wysyłana jest pozycja w osi x
	location[1] = ((char *)&x_position)[0];		// cztery kolejne bajty zawierające pozycję
	location[2] = ((char *)&x_position)[1];
	location[3] = ((char *)&x_position)[2];
	location[4] = ((char *)&x_position)[3];
	location[5] = 'y';							// dla osi y - analogicznie jak dla x
	location[6] = ((char *)&y_position)[0];
	location[7] = ((char *)&y_position)[1];
	location[8] = ((char *)&y_position)[2];
	location[9] = ((char *)&y_position)[3];
	location[10] = 'z';							// dla osi z - analogicznie jak dla x
	location[11] = ((char *)&z_position)[0];
	location[12] = ((char *)&z_position)[1];
	location[13] = ((char *)&z_position)[2];
	location[14] = ((char *)&z_position)[3];


	send_uart(location);	// wysłanie wiadomości z lokalizacją
}


// funkcja resetująca położenie do minimalnego w osi x i y oraz maksymalnego w osi z
void reset_location()
{
	x_position = 0;
	y_position = 0;
	z_position = 1100000;
}


// funkcja realizująca opóźnienie zadane w mikrosekundach
// licznik inkrementuje się dokładnie co 1 mikrosekundę
void delay_us (uint16_t us)
{
	__HAL_TIM_SET_COUNTER(&htim1, 0);  						// ustawiam licznik mikrosekund na 0
	while ((uint16_t)__HAL_TIM_GET_COUNTER(&htim1) < us);  	// czekam aż licznik osiągnie zadaną wartość
}


/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_SPI1_Init();
  MX_USB_PCD_Init();
  MX_UART4_Init();
  MX_TIM1_Init();
  MX_UART5_Init();
  /* USER CODE BEGIN 2 */

  // ustawiamy wartości początkowe transmisji szeregowej
  __HAL_UART_CLEAR_IDLEFLAG(&huart4);
  HAL_UART_Receive_IT (&huart4, &receive_buffer, 1);
  __HAL_UART_ENABLE_IT(&huart4, UART_IT_IDLE);
  __HAL_UART_CLEAR_IDLEFLAG(&huart5);
  HAL_UART_Receive_IT (&huart5, &receive_buffer5, 1);
  __HAL_UART_ENABLE_IT(&huart5, UART_IT_IDLE);

  // wartości początkowe wyprowadzeń mikrokontrolera
  HAL_GPIO_WritePin(GPIOE, GPIO_PIN_8, GPIO_PIN_SET);
  HAL_GPIO_WritePin(GPIOE, GPIO_PIN_9, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOE, GPIO_PIN_10, GPIO_PIN_RESET);

  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_1, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_2, GPIO_PIN_SET);

  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_2, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_3, GPIO_PIN_SET);

  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_1, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_2, GPIO_PIN_SET);

  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_14, GPIO_PIN_SET);
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_15, GPIO_PIN_SET);

  // włączenie zliczania mikrosekund
  HAL_TIM_Base_Start(&htim1);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */


while (1)
{
	// jeżeli ilość elementów w buforze jest mniejsza niż 500,
	// to wysyłamy zapytanie o kolejne dane do komputera
	bufor_elements = data_length();
	if (bufor_elements < 500 && already_send == false)
	{
		send_uart("M");
		already_send = true;
	}

	// mechanizm blokowania, aby program nie wysyłał
	// w nieskończoność zapytania o kolejne dane
	if (bufor_elements > 500)
	{
		already_send = false;
	}

	// odbieranie danych z łącza z danymi
	if (bufor_elements > 0 && receive_next == true && cont == true)	// jeżeli spełnione są warunki odbioru
	{
		take_x_bytes(1, received);		// pobieramy jeden bajt
		actual_byte = received[0];		// i zapisujemy go w zmiennej actual_byte

		// w zależności od odebranego bajtu wykonujemy określoną czynność i sprawdzamy
		// czy ruch w danym kierunku nie spowoduje wyjścia z obszaru roboczego
		// ustawiane są odpowiednie flagi
		switch (actual_byte)
		{
			case 'X':		if (x_position < 17000000){next_step = true; receive_next = false;} break;
			case 'x':		if (x_position > 0){next_step = true; receive_next = false;} break;
			case 'Y':		if (y_position < 20000000){next_step = true; receive_next = false;} break;
			case 'y':		if (y_position > 0){next_step = true; receive_next = false;} break;
			case 'Z':		if (z_position < 1100000){next_step = true; receive_next = false;} break;
			case 'z':		if (z_position > 0){next_step = true; receive_next = false;} break;
			default:		break;
		}
	}

	// ustawianie kierunku ruchu silnika do realizacji ścieżki
	if (next_step == true && release == true)
	{
		// w zależności od odebranego bajtu ustawiamy odpowiedni stan na
		// wyjściu sterującym kierunkiem ruchu w danej osi
		// oraz zerujemy licznik mikrosekund
		switch (actual_byte)
		{
			case 'X':	HAL_GPIO_WritePin(GPIOC, GPIO_PIN_1, GPIO_PIN_SET); // kierunek X
		  	  	  	 	__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'x':	HAL_GPIO_WritePin(GPIOC, GPIO_PIN_1, GPIO_PIN_RESET); // kierunek X
		  			 	__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'Y':	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_2, GPIO_PIN_RESET); // kierunek Y
		  	  	  	 	__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'y':	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_2, GPIO_PIN_SET); // kierunek Y
		  			 	__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'Z':	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_1, GPIO_PIN_RESET); // kierunek Z
		  	  	  	 	__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'z':	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_1, GPIO_PIN_SET); // kierunek Z
		  			 	__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			default:	break;
		}

		// blokujemy wykonywanie powyższego bloku do momentu odebrania następnego bajtu danych
		release = false;
	}

	// pobieramy ilość mikrosekund, które upłynęły od ustawienia kierunku ruchu
	time = (uint16_t)__HAL_TIM_GET_COUNTER(&htim1);
	// jeżeli ilość mikrosekund jest większa od ustawionego interwału oraz
	// flaga next_step jest ustawiona, to wykonujemy krok silnika
	if (next_step == true && time >= interval)
	{
		// w zależności od aktualnie odebranego bajtu generujemy impuls prostokątny
		// na odpowiednim wyjściu cyfrowym oraz aktualizujemy pozycję frezarki
		if (actual_byte == 'X')
		{
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_RESET);
			x_position += 125;
		}
		else if (actual_byte == 'x')
		{
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_RESET);
			x_position -= 125;
		}
		else if (actual_byte == 'Y')
		{
			HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_RESET);
			y_position += 125;
		}
		else if (actual_byte == 'y')
		{
			HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_RESET);
			y_position -= 125;
		}
		else if (actual_byte == 'Z')
		{
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET);
			z_position += 50;
		}
		else if (actual_byte == 'z')
		{
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET);
			z_position -= 50;
		}

		// wykonanie kroku powoduje takie ustawienie flag, które pozwoli na odbiór kolejnego bajtu
		next_step = false;
		receive_next = true;
		release = true;
	}

	// obsługa bufora danych wejściowych z łącza instrukcjami sterującymi
	bufor_elements5 = data_length5();	// pobieram ilość elementów bufora z instrukcjami sterującymi
	if (bufor_elements5 > 0)			// jeżeli bufor zawiera jakieś dane
	{
		take_x_bytes5(1, &received[1]);	// pobieram jeden bajt
		actual_byte5 = received[1];		// i wpisuję go do actual_byte5

		// w zależności od odebranego bajtu wykonywana jest odpowiadająca instrukcja
		switch (actual_byte5)
		{
			case 'E':	clean_bufor(); break;		// koniec ruchu
			case 's':	stop = true; break;			// zatrzymanie ruchu - dotyczy sterowania za pomocą przycisków
			case 'S':	cont = false; break;		// stop - wstrzymanie realizacji zadanej trajektorii
			case 'R':	cont = true; break;			// kontynuacja realziacji zadanej trajektorii
			case 'D':	clean_bufor(); cont = true; break; 	// delete - reset
			case 'd':	send_location(); break;		// wysłanie lokalizacji
			case 'l':	reset_location(); break;	// reset lokalizacji

			// w zależności od odebranego bajtu ustawiany jest kierunek ruchu odpowiedniego silnika
			// oraz zerowany jest licznik mikrosekund
			case 'X':	start_moving = true; what_move = 'X';
						HAL_GPIO_WritePin(GPIOC, GPIO_PIN_1, GPIO_PIN_SET);
						__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'x':	start_moving = true; what_move = 'x';
  	  	  	  	  		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_1, GPIO_PIN_RESET);
  	  	  	  	  		__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'Y':	start_moving = true; what_move = 'Y';
						HAL_GPIO_WritePin(GPIOA, GPIO_PIN_2, GPIO_PIN_RESET);
  	  	  	  	  		__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'y':	start_moving = true; what_move = 'y';
  	  	  	  	  		HAL_GPIO_WritePin(GPIOA, GPIO_PIN_2, GPIO_PIN_SET);
  	  	  	  	  		__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'Z':	start_moving = true; what_move = 'Z';
  	  	  	  	  		HAL_GPIO_WritePin(GPIOB, GPIO_PIN_1, GPIO_PIN_RESET);
  	  	  	  	  		__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'z':	start_moving = true; what_move = 'z';
  	  	  				HAL_GPIO_WritePin(GPIOB, GPIO_PIN_1, GPIO_PIN_SET);
  	  	  	  	  		__HAL_TIM_SET_COUNTER(&htim1, 0); break;
			case 'L':	interval = 995; break; 		// niska prędkość
			case 'M':	interval = 495; break;		// średnia prędkość
			case 'F':	interval = 295; break;		// szybka prędkość
			case 'P':	turn_on_pump(); break;
			case 'p':	turn_off_pump(); break;
			case 'B':	turn_falownik_on(); break;
			case 'b':	turn_falownik_off(); break;
			default:	break;
		}
	}

	// obsługa ruchu za pomocą przycisków w GUI
	time = (uint16_t)__HAL_TIM_GET_COUNTER(&htim1);		// pobranie wartości licznika mikrosekund
	if (start_moving == true && time > interval_2)		// jeżeli upłynął odpowiedni czas i mamy zezwolenie
														// na ruch, to wchodzimy do instrukcji warunkowej
	{
		// w zależności od odebranego bajtu generujemy impuls prostokątny na odpowiednim wyprowadzeniu cyfrowym
		// oraz aktualizujemy pozycję narzędzia roboczego
		if (what_move == 'X')
		{
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_RESET);
			x_position += 125;
		}
		else if (what_move == 'x')
		{
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_RESET);
			x_position -= 125;
		}
		else if (what_move == 'Y')
		{
			HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_RESET);
			y_position += 125;
		}
		else if (what_move == 'y')
		{
			HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_RESET);
			y_position -= 125;
		}
		else if (what_move == 'Z')
		{
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET);
		 	z_position += 50;
		}
		else if (what_move == 'z')
 		{
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET);
			delay_us(5);
			HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET);
		 	z_position -= 50;
 		}

		__HAL_TIM_SET_COUNTER(&htim1, 0);		// zerujemy licznik mikrosekund

		// poniższy zestaw instrukcji warunkowych powoduje stopniowe przyspieszanie
		// i hamowanie przy sterowaniu za pomocą przycisków
		if (interval_2 > interval && stop == false)
		{
			interval_2 -= decreasing;
		}

		if (decreasing > 1 && stop == false)
		{
			decreasing--;
		}

		if (stop == true)
		{
			decreasing = 2;
			interval_2 += decreasing;

			if (interval_2 > 1295)
			{
				start_moving = false;
				interval_2 = 1495;
				decreasing = 30;
				stop = false;
			}
		}
	}

	// wciśnięcie niebieskiego przycisku powoduje ustawienie zmiennej send na wartość 1
	// tym samym wykona się poniższy blok kodu
	// w tej chwili nie spełnia żadnej roli, ale może się przydać w przyszłości
	if (send)
	{
		send = 0;	// zerowanie zmiennej, aby instrukcja warunkowa nie wykonywała się bez końca
	}

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI|RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USB|RCC_PERIPHCLK_UART4
                              |RCC_PERIPHCLK_UART5|RCC_PERIPHCLK_I2C1
                              |RCC_PERIPHCLK_TIM1;
  PeriphClkInit.Uart4ClockSelection = RCC_UART4CLKSOURCE_PCLK1;
  PeriphClkInit.Uart5ClockSelection = RCC_UART5CLKSOURCE_PCLK1;
  PeriphClkInit.I2c1ClockSelection = RCC_I2C1CLKSOURCE_HSI;
  PeriphClkInit.USBClockSelection = RCC_USBCLKSOURCE_PLL_DIV1_5;
  PeriphClkInit.Tim1ClockSelection = RCC_TIM1CLK_HCLK;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
