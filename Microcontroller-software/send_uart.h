/*
 * send_uart.h
 *
 *  Created on: 6 lip 2021
 *      Author: bened
 */

#ifndef INC_SEND_UART_H_
#define INC_SEND_UART_H_
#define s_bufor_size 20
#include <stdint.h>
#include "main.h"


void send_one_character();
void send_uart(const char message[]);
void send_uart_counter(const char message[]);


#endif /* INC_SEND_UART_H_ */
