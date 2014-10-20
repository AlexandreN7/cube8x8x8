/*
 * File:   main.c
 * Author: archi
 *
 * Created on 16 octobre 2014, 17:36
 */

#pragma config XINST = OFF, SOSCSEL = DIG , CANMX = PORTB
#pragma config FCMEN=ON, IESO=ON , WDTEN = OFF , EBTRB = OFF


#include <stdio.h>
#include <stdlib.h>
#include <p18f25k80.h>
#include <xc.h>
#include <timers.h>
#include <portb.h>
#include <usart.h>



unsigned char Rxdata[25];
unsigned char Txdata[] = "MICROCHIP_USART";

// BAUD_RATE_GEN is calculated as  = [Fosc / (64 * Desired Baudrate)] - 1
// It needs to be changed depending upon oscillator frequency.
//  8MHz / (64 * 2400) - 1 = 51 (approx.)
#define BAUD_RATE_GEN 51



int main(int argc, char** argv) {

  //-------------------------configure USART ---------------------------------------------------------
    // API configures USART for desired parameters:
    //  - TX/RX interrupts turned off
    //  - Asynchronous mode
    //  - 8 bits
    //  - Continuous Receive Enabled
    //  - Low speed baud rate generator mode (Fosc / 16)
    OpenUSART(USART_TX_INT_OFF | USART_RX_INT_OFF | USART_ASYNCH_MODE | USART_EIGHT_BIT | USART_CONT_RX | USART_BRGH_LOW, BAUD_RATE_GEN);
    baudUSART(BAUD_8_BIT_RATE | BAUD_AUTO_OFF);

//------------USART Transmission ----------------------------------------------------------------
    putsUSART((char *)Txdata);             // transmit the string

//-----------USART Reception ---------------------------------------------------------------------
    getsUSART((char *)Rxdata, 24);         // receive data up to 24 bytes
    Rxdata[24] = 0;                         // NULL terminate the string for putsUSART call.
    putsUSART((char *)Rxdata);             // echo back the data recieved back to host

    CloseUSART();
    while(1);  			//End of program
}

