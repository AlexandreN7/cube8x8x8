#include <xc.h>

#include "main.h"
//=============================================================================
// 7ROBOT
// Created by Alexandre Proux
// Cube 8x8x8
//============================================================github=============
//
//
//=============================================================================

//****************************************************************************************
//                    CONFIGURATION BITS PIC18F25K80
//****************************************************************************************

// Configuration register

// CONFIG1L
#pragma config RETEN = OFF      // VREG Sleep Enable bit (Ultra low-power regulator is Disabled (Controlled by REGSLP bit))
#pragma config INTOSCSEL = HIGH // LF-INTOSC Low-power Enable bit (LF-INTOSC in High-power mode during Sleep)
#pragma config SOSCSEL = DIG    // SOSC Power Selection and mode Configuration bits (Digital (SCLKI) mode)
#pragma config XINST = OFF      // Extended Instruction Set (Disabled)

// CONFIG1H
#pragma config FOSC = INTIO1    // Oscillator (Internal RC oscillator)
#pragma config PLLCFG = ON    // PLL x4 Enable bit (Disabled)
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor (Disabled)
#pragma config IESO = ON       // Internal External Oscillator Switch Over Mode (Disabled)

// CONFIG2L
#pragma config PWRTEN = OFF     // Power Up Timer (Disabled)
#pragma config BOREN = SBORDIS  // Brown Out Detect (Enabled in hardware, SBOREN disabled)
#pragma config BORV = 3         // Brown-out Reset Voltage bits (1.8V)
#pragma config BORPWR = ZPBORMV // BORMV Power level (ZPBORMV instead of BORMV is selected)

// CONFIG2H
#pragma config WDTEN = OFF      // Watchdog Timer (WDT disabled in hardware; SWDTEN bit disabled)
#pragma config WDTPS = 1048576  // Watchdog Postscaler (1:1048576)

// CONFIG3H
#pragma config CANMX = PORTB    // ECAN Mux bit (ECAN TX and RX pins are located on RB2 and RB3, respectively)
#pragma config MSSPMSK = MSK7   // MSSP address masking (7 Bit address masking mode)
#pragma config MCLRE = OFF      // Master Clear Enable (MCLR Disabled, RG5 Enabled)

// CONFIG4L
#pragma config STVREN = ON      // Stack Overflow Reset (Enabled)
#pragma config BBSIZ = BB2K     // Boot Block Size (2K word Boot Block size)

// CONFIG5L
#pragma config CP0 = OFF        // Code Protect 00800-01FFF (Disabled)
#pragma config CP1 = OFF        // Code Protect 02000-03FFF (Disabled)
#pragma config CP2 = OFF        // Code Protect 04000-05FFF (Disabled)
#pragma config CP3 = OFF        // Code Protect 06000-07FFF (Disabled)

// CONFIG5H
#pragma config CPB = OFF        // Code Protect Boot (Disabled)
#pragma config CPD = OFF        // Data EE Read Protect (Disabled)

// CONFIG6L
#pragma config WRT0 = OFF       // Table Write Protect 00800-03FFF (Disabled)
#pragma config WRT1 = OFF       // Table Write Protect 04000-07FFF (Disabled)
#pragma config WRT2 = OFF       // Table Write Protect 08000-0BFFF (Disabled)
#pragma config WRT3 = OFF       // Table Write Protect 0C000-0FFFF (Disabled)

// CONFIG6H
#pragma config WRTC = OFF       // Config. Write Protect (Disabled)
#pragma config WRTB = OFF       // Table Write Protect Boot (Disabled)
#pragma config WRTD = OFF       // Data EE Write Protect (Disabled)

// CONFIG7L
#pragma config EBTR0 = OFF      // Table Read Protect 00800-03FFF (Disabled)
#pragma config EBTR1 = OFF      // Table Read Protect 04000-07FFF (Disabled)
#pragma config EBTR2 = OFF      // Table Read Protect 08000-0BFFF (Disabled)
#pragma config EBTR3 = OFF      // Table Read Protect 0C000-0FFFF (Disabled)

// CONFIG7H
#pragma config EBTRB = OFF      // Table Read Protect Boot (Disabled)


// DEFINE LISTE
#define mux1   PORTCbits.RC7
#define mux2   PORTCbits.RC6
#define mux3   PORTCbits.RC5
#define mux4   PORTCbits.RC4
#define mux5   PORTCbits.RC0
#define mux6   PORTCbits.RC1
#define mux7   PORTCbits.RC2
#define mux8   PORTCbits.RC3

#define clock  PORTAbits.RA0

// GLOBAL
char tampon = 0;
char compteur = 0;
char flag_reception = 0;
char it = 0;

void interrupt low_priority low_isr(void) { // interruption de l'UART

    if (RC2IF /*&& PIE3bits.TX2IE*/) {
        tampon = RCREG2;
        if (compteur == 128) {
            compteur = 0;
        }
        writeDataToUART(tampon);
        compteur++;
    }
    RC2IF = 0; // On met le flag a 0
}


void interrupt low_priority timer_isr(void) {
    // Check for overflow of TMR0
    if (TMR0IE && TMR0IF) {
        // mettre la clock ici
    }
    TMR0IF = 0;
}


void init_timer(void);
void multiplexeur(char);

void main(void) {
    char msg1[80] = "MASTER IS READY \n \r";
    long i = 0;
    long j = 0;

    initPorts(); // Initialize ports to startup state
    initComms(); // Initialize the serial port

    while (1) {
        for (i = 0; i < 8; i++) {
            multiplexeur(i);
            clock = 1;
            for (j = 0; j < 100; j++) {
            }
            clock = 0;
            for (j = 0; j < 10000; j++) {

            }
        }
        

    }
}

void multiplexeur(char n) {
    mux1 = 0;
    mux2 = 0;
    mux3 = 0;
    mux4 = 0;
    mux5 = 0;
    mux6 = 0;
    mux7 = 0;
    mux8 = 0;

    switch (n) {
        case 0:
            mux1 = 1;
            break;

        case 1:
            mux2 = 1;
            break;

        case 2:
            mux3 = 1;
            break;

        case 3:
            mux4 = 1;
            break;

        case 4:
            mux5 = 1;
            break;

        case 5:
            mux6 = 1;
            break;

        case 6:
            mux7 = 1;
            break;

        case 7:
            mux8 = 1;
            break;

    }

}

void init_timer(void) {
    //Setup Timer0
    T0PS0 = 0; //Prescaler is divide by 256
    T0PS1 = 1;
    T0PS2 = 0;
    PSA = 0; //Timer Clock Source is from Prescaler
    T0CS = 0; //Prescaler gets clock from FCPU
    T08BIT = 1; //8 BIT MODE
    TMR0IE = 1; //Enable TIMER0 Interrupt
    PEIE = 1; //Enable Peripheral Interrupt
    GIE = 1; //Enable INTs globally
}
