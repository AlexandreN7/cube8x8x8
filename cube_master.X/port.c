
#include "main.h"
//=============================================================================
// Filename: Ports.c
//=============================================================================

void initPorts(void) {


    //Set oscillator options
    //OSCCON = 0x30;              //4MHz
     OSCCON = 0x70;                //16MHZ
    //Analog configuration
    ANCON0 = 0b00000000;        //AIN4 is used as analog input
    //ADCON1 = 0b00000111;        //AIN8,9, and 10 are used as analog input
    //ADCON2 = 0xBC;              //20 TAD, Fosc/4
    ADON = 0;                   //enable ADC

    //Digital configurations
    PORTA = 0b00000000;         // Initial state of PORTA
    TRISA = 0b00000000;         // Set PORTA pin directions: all input

    PORTB = 0b01000000;         // Initial state of PORTB (driver and receiver disabled, TX high, other outputs off)
    TRISB = 0b10000000;         // Set PORTB pin in output expect uart pins RB0/RB1

    PORTC = 0b00000000;         // Initial state of PORTC (turn LEDs, outputs off)
    TRISC = 0b00000000;         // Set PORTC pin directions: RC0-RC4 output, RC5-RC7 input


    GIE = 1;
    PEIE = 1;
    INTCON =0b11000000;

    OSCTUNEbits.PLLEN = 1;



}
