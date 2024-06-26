/*
 * send_uart.c
 *
 *  Created on: 6 lip 2021
 *      Author: bened
 */
#include "send_uart.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "main.h"
#include "usart.h"

uint8_t s_bufor[s_bufor_size];		// bufor kołowy na wysyłane dane
uint8_t* s_head = s_bufor + 5;		// wskaźnik na początek danych
uint8_t* s_tail = s_bufor + 5;		// wskaźnik na koniec danych
uint8_t* s_end = s_bufor + (s_bufor_size - 1);		// wskaźnik na koniec bufora
uint8_t data_send;		// wysyłana obecnie dana


// funkcja wywoływana po przerwaniu związanym z zakończeniem wysyłania danej przez UART
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
	HAL_GPIO_TogglePin(GPIOE, GPIO_PIN_10);		// zamiana stanu diody LED
	send_one_character(&huart5);				// wysłanie kolejnego bajtu
}


// funkcja wysyłająca jeden bajt
void send_one_character()
{
	// jeżeli bufor z danymi do wysłania nie jest pusty
	if (s_tail != s_head)
	{
		data_send =  *s_tail;	// pobieram daną z bufora
		*s_tail = '\0';			// i ją z bufora usuwam

		if (s_tail == s_end)	// jeżeli doszedłem do końca bufora
			s_tail = s_bufor;	// przeskakuję na początek
		else					// w przeciwnym wypadku
			s_tail = s_tail + 1;	// przesuwam wskaźnik na następne miejsce w pamieci

		// wysyłam pobraną z bufora daną
		HAL_UART_Transmit_IT(&huart5, &data_send, 1);
	}
}


// funkcja zapisuje daną, którą chcemy wysłać do bufora kołowego
void send_uart(const char message[])
{
	uint8_t data;

	// zapisuje każdy bajt wiadomości na kolejnych pozycjach bufora kołowego
	for (int i = 0; i < strlen(message); i++)
	{
		data = message[i];

		if (s_head == s_end)
		{
			if (s_bufor != s_tail)
			{
				*s_head = data;
				s_head = s_bufor;
			}
		}
		else if (s_head + 1 != s_tail)
		{
			*s_head = data;
			s_head = s_head + 1;
		}
	}

	// i uruchamiam mechanizm wysyłania
	send_one_character();
}

