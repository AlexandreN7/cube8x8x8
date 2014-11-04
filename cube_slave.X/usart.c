#include "main.h"
//=============================================================================
// Filename: usart.c
//=============================================================================

void initComms()
{
    TXSTA2bits.CSRC = 0;
    TXSTA2bits.TX9 = 0;
    TXSTA2bits.TXEN = 1;
    TXSTA2bits.SYNC = 0;
    TXSTA2bits.SENDB = 0;
    TXSTA2bits.BRGH = 1;
    TXSTA2bits.TRMT = 1;
    TXSTA2bits.TX9D = 0;

    RCSTA2bits.SPEN = 1;
    RCSTA2bits.RX9 = 0;
    RCSTA2bits.SREN = 0;
    RCSTA2bits.CREN  = 1;
    RCSTA2bits.ADDEN = 0;
    RCSTA2bits.FERR = 0;
    RCSTA2bits.OERR = 0;
    RCSTA2bits.RX9D = 0;

    BAUDCON2bits.ABDOVF = 0;
    BAUDCON2bits.RCIDL = 1;
    BAUDCON2bits.RXDTP = 0;
    BAUDCON2bits.TXCKP = 0;
    BAUDCON2bits.BRG16 = 1;
    BAUDCON2bits.WUE = 0;
    BAUDCON2bits.ABDEN = 0;

    PIE3bits.RC2IE = 1;
    RCONbits.IPEN   = 1; // ENABLE interrupt priority

   //////////////////////////SETTING BAUDRATE////////////////
   //((FCY/16)/BAUD) - 1; // set baud to 9600  FCY=4000000
   // SPBRG = 103;      => a choper dans la datasheet
   //SPBRG2 = 25;      // 9600

   //SPBRG = 51;   // 19200
   //SPBRG2 = 12
   
    SPBRG = 115;  // 115000  // On suppose que FCY = 64 000 000
    SPBRGH2 = 0;
    SPBRG2 = 137;

   



}

void writeStringToUART (const char *msg)
{
    while(*msg)    {
        while(PIR3bits.TX2IF == 0) {}
        TXREG2 = *msg++;
    }
}

void writeDataToUART(char data)
{
  while(PIR3bits.TX2IF == 0) {}
  TXREG2 = data;
}
