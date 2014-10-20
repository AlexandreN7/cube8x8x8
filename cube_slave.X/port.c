
#include "main.h"
//=============================================================================
// Filename: Ports.c
//=============================================================================

void initPorts(void) {


    //Set oscillator options
   // OSCCON = 0x30;              //4MHz
    OSCCON = 0x70;                //16MHZ
    //Analog configuration
    ANCON0 = 0b00010000;        //AIN4 is used as analog input
    ADCON1 = 0b00000111;        //AIN8,9, and 10 are used as analog input
    ADCON2 = 0xBC;              //20 TAD, Fosc/4
    ADON = 1;                   //enable ADC

    //Digital configurations
    PORTA = 0b00000000;         // Initial state of PORTA
    TRISA = 0b11111111;         // Set PORTA pin directions: all input

    PORTB = 0b01001000;         // Initial state of PORTB (driver and receiver disabled, TX high, other outputs off)
    TRISB = 0b10010011;         // Set PORTB pin directions: RB2, RB3, RB5, RB6 output, all others input

    PORTC = 0b00000000;         // Initial state of PORTC (turn LEDs, outputs off)
    TRISC = 0b11100000;         // Set PORTC pin directions: RC0-RC4 output, RC5-RC7 input
}