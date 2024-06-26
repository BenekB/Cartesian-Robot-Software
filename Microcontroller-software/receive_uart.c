/*
 * receive_uart.c
 *
 *  Created on: Jul 5, 2021
 *      Author: bened
 */


#include "receive_uart.h"
#include <stdint.h>
#include <stdlib.h>
#include "usart.h"
#include "main.h"

uint8_t bufor[r_bufor_size];									// bufor do odbioru danych
uint8_t* head = bufor + 5;					// wskaźnik na ostatnio zapisaną daną
uint8_t* tail = bufor + 5;					// wskaźnik na najwcześniej zapisaną daną
uint8_t* end = bufor + (r_bufor_size - 1);	// wskaźnik na koniec bufora

uint8_t bufor5[r_bufor_size5];									// bufor do odbioru instukcji sterujących
uint8_t* head5 = bufor5 + 5;					// wskaźnik na ostatnio zapisaną daną
uint8_t* tail5 = bufor5 + 5;					// wskaźnik na najwcześniej zapisaną daną
uint8_t* end5 = bufor5 + (r_bufor_size5 - 1);	// wskaźnik na koniec bufora


// funkcja ustawia wskaźniki tak jakby bufor był pusty
void clean_bufor()
{
	head = bufor + 5;
	tail = bufor + 5;
}


// funkcja wywoływana po odebraniu każdego bajtu informacji
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	HAL_GPIO_TogglePin(GPIOE, GPIO_PIN_10);					// zmieniam napięcie na LED na przeciwne

	if (huart == &huart4)									// dla łącza danych
	{
		HAL_UART_Receive_IT (&huart4, &receive_buffer, 1);	// ustawiam przerwanie
		receive_and_write(receive_buffer);					// zapisuję odebraną daną do bufora kołowego danych
	}
	else if (huart == &huart5)								// dla łącza instrukcji kontrolnych
	{
		HAL_UART_Receive_IT (&huart5, &receive_buffer5, 1);	// ustawiam przerwanie
		receive_and_write5(receive_buffer5);				// zapisuję odebraną daną do bufora kołowego instrukcji sterujących
	}
}


// funkcja zwraca ilość danych w buforze kołowym danych
int data_length()
{
	if (head == tail)
		return 0;

	else if (head > tail)
		return head - tail;

	else
		return end - tail + head - bufor;
}


// funkcja zwraca ilość danych w buforze kołowym instrukcji sterujących
int data_length5()
{
	if (head5 == tail5)
		return 0;

	else if (head5 > tail5)
		return head5 - tail5;

	else
		return end5 - tail5 + head5 - bufor5;
}


// funkcja pobierająca x bajtów informacji z bufora danych pod adres data
int take_x_bytes(int x, uint8_t* data)
{
	int ile = 0;		// parametr zliczający ile rzeczywiście bajtów
						// zostało pobranych

	// pobieramy tyle bajtów ile zostało zadanych
	for(int i = 0; i < x; i++)
	{
		if (tail != head)		// jeżeli bufor nie jest pusty
		{
			data[i] =  *tail;
			*tail = '\0';

			if (tail == end)
				tail = bufor;
			else
				tail = tail + 1;

			ile++;
		}
		else					// jeżeli doszliśmy do końca bufora
		{
			data[i] = '\0';
		}
	}

	return ile;		// zwracam ile rzeczywiście pobrano bajtów
					// przed dojściem do końca bufora
}


// funkcja pobierająca x bajtów informacji z bufora instrukcji sterujących pod adres data
// działa identycznie jak funkcja take_x_bytes, tylko pobiera dane z bufora instrukcji sterujących
int take_x_bytes5(int x, uint8_t* data)
{
	int ile = 0;

	for(int i = 0; i < x; i++)
	{
		if (tail5 != head5)
		{
			data[i] =  *tail5;
			*tail5 = '\0';

			if (tail5 == end5)
				tail5 = bufor5;
			else
				tail5 = tail5 + 1;

			ile++;
		}
		else
		{
			data[i] = '\0';
		}
	}

	return ile;
}


// funkcja pobiera odebrany przez UART bajt i zapisuje go do bufora danych w odpowiednie miejsce
void receive_and_write(uint8_t data)
{
	if (head == end)
	{
		if (bufor != tail)
		{
			*head = data;
			head = bufor;
		}
	}

	else if (head + 1 != tail)
	{
		*head = data;
		head = head + 1;
	}
}


// funkcja pobiera odebrany przez UART bajt i zapisuje go do bufora instrukcji sterujących w odpowiednie miejsce
void receive_and_write5(uint8_t data)
{
	if (head5 == end5)
	{
		if (bufor5 != tail5)
		{
			*head5 = data;
			head5 = bufor5;
		}
	}

	else if (head5 + 1 != tail5)
	{
		*head5 = data;
		head5 = head5 + 1;
	}
}

