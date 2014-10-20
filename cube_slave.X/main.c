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

#define _XTAL_FREQ 8000000 

char UART_Init(const long int baudrate);
void UART_Write(char data);

unsigned char Rxdata[25];
unsigned char Txdata[] = "MICROCHIP_USART";





int main(int argc, char** argv) {
   UART_Init(9600);
    while(1) {
        UART_Write('A');
        for(int i= 0 ; i<100000; i++) {}
    }


}

char UART_Init(const long int baudrate)
{
  unsigned int x;
  x = (_XTAL_FREQ - baudrate*64)/(baudrate*64); //SPBRG for Low Baud Rate
  if(x>255) //If High Baud Rate required
  {
    x = (_XTAL_FREQ - baudrate*16)/(baudrate*16); //SPBRG for High Baud Rate
   // BRGH = 1; //Setting High Baud Rate
    TXSTA1bits.BRGH = 1;
  }
  if(x<256)
  {
    //  SPBRG1 =12;

    SPBRG1 = 12; //Writing SPBRG register
    SPBRGH1 =0;
    TXSTA1bits.SYNC = 0; //Selecting Asynchronous Mode
    RCSTA1bits.SPEN = 1; //Enables Serial Port
    TRISC7 = 1;
    TRISC6 = 1;
    CREN1 = 1; //Enables Continuous Reception
    TXEN1 = 1; //Enables Transmission
   return 1;
  }
  return 0;
}


void UART_Write(char data)
{
  while(!TRMT1); //Waiting for Previous Data to Transmit completly
  TXREG = data; //Writing data to Transmit Register, Starts transmission
}