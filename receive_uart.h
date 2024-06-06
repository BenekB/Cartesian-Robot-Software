/*
 * receive_uart.h
 *
 *  Created on: Jul 5, 2021
 *      Author: bened
 */

#ifndef INC_RECEIVE_UART_H_
#define INC_RECEIVE_UART_H_
#define r_bufor_size 2000
#define r_bufor_size5 40
#include <stdint.h>


void receive_and_write(uint8_t data);
int take_x_bytes(int x, uint8_t* data);
int data_length();
int take_all_bytes(uint8_t* data);
void receive_and_write5(uint8_t data);
int take_x_bytes5(int x, uint8_t* data);
int data_length5();
void clean_bufor();

#endif /* INC_RECEIVE_UART_H_ */
