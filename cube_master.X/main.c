/*
 * File:   main.c
 * Author: archi
 *
 * Created on 16 octobre 2014, 17:36
 */

#pragma config XINST = OFF, SOSCSEL = DIG , CANMX = PORTB
#pragma config FCMEN=ON, IESO=ON , WDTEN = OFF , EBTRB = OFF /*, FOSC = HS1*/

#include <xc.h>
#include <stdio.h>
#include <stdlib.h>
#include <p18f25k80.h>

#include <timers.h>
#include <portb.h>
#include <usart.h>

//#define USE_OR_MASKS

unsigned char Rxdata[25];
unsigned char Txdata[] = "MICROCHIP_USART";

// BAUD_RATE_GEN is calculated as  = [Fosc / (64 * Desired Baudrate)] - 1
// It needs to be changed depending upon oscillator frequency.
//  8MHz / (64 * 2400) - 1 = 51 (approx.)
#define BAUD_RATE_GEN 25



int main(int argc, char** argv) {


    //initialisations
   // CMCON = 0b00000111; /* Désactive les comparateurs. */
    ADCON0 = 0b00000000;
    ADCON1 = 0b00001111;
    WDTCON = 0;
    OSCCON = 0b01111111;
    //UCON = 0; /* Désactive l'USB. */
    //UCFG = 0b00001000;
    TRISC = 0b00000000;
    TRISA = 0b11111111;
    TRISB = 0b11111111;
        GIE = 1;
    PEIE = 1;



    Open1USART((USART_TX_INT_OFF | USART_RX_INT_OFF | USART_ASYNCH_MODE | USART_EIGHT_BIT | USART_CONT_RX | USART_BRGH_LOW) , BAUD_RATE_GEN);
    baud1USART(BAUD_8_BIT_RATE | BAUD_AUTO_OFF);

    while(1) {
  //-------------------------configure USART ---------------------------------------------------------
    // API configures USART for desired parameters:
    //  - TX/RX interrupts turned off
    //  - Asynchronous mode
    //  - 8 bits
    //  - Continuous Receive Enabled
    //  - Low speed baud rate generator mode (Fosc / 16)


//------------USART Transmission ----------------------------------------------------------------
  //  puts1USART((char *)Txdata);             // transmit the string
   // while(Busy1USART());
    Write1USART('a');
    //putrs1USART('y');

 //      for (int i =0 ; i<1000; i++) {}
//-----------USART Reception ---------------------------------------------------------------------
 ///   getsUSART((char *)Rxdata, 24);         // receive data up to 24 bytes
 //   Rxdata[24] = 0;                         // NULL terminate the string for putsUSART call.
 //   putsUSART((char *)Rxdata);             // echo back the data recieved back to host

//    CloseUSART();
    }
}

