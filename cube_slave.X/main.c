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
#pragma config PLLCFG = ON     // PLL x4 Enable bit (Disabled)
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


// DEFINE LIST

#define slave 0

#define ledR1 PORTAbits.RA0
#define ledR2 PORTAbits.RA3
#define ledR3 PORTAbits.RA6
#define ledR4 PORTCbits.RC2
#define ledR5 PORTBbits.RB2
#define ledR6 PORTBbits.RB5
#define ledR7 PORTBbits.RB0
#define ledR8 PORTCbits.RC5

#define ledB1 PORTAbits.RA1
#define ledB2 PORTAbits.RA2
#define ledB3 PORTCbits.RC0
#define ledB4 PORTCbits.RC2
#define ledB5 PORTBbits.RB4
#define ledB6 PORTBbits.RB2
#define ledB7 PORTCbits.RC6
#define ledB8 PORTCbits.RC4

#define clock PORTBbits.RB1


char tampon = 0;
char stock_led[128] = 0;
int compteur = 0;
char compteur_clock = 1;
char state_clock = 0;

void interrupt low_priority high_isr(void) {
    if (RC2IF) {
        tampon = RCREG2;

        if (compteur == 128) {
            compteur = 0;
        }
        stock_led[compteur] = tampon;
        compteur++;
    }
    RC2IF = 0; // On met le flag à 0
}

void affichage(int);



void main(void) {
    unsigned char address = 0;
    char msg1[80] = "Slave Ready \n \r";


    initPorts(); // Initialize ports to startup state
    initComms(); // Initialize the serial port

    while (1) {

	if ( clock == 1 )
	{
		compteur_clock = compteur_clock+1;
		
		if (compteur_clock == 8)
		{
			compteur_clock =1;
		}
	}


        //PORTA = stock_led[esclave];
        //PORTC = stock_led[esclave + 1];
    }
}

void affichage(int n)
{

		if(0b00000001 & stock_led[slave]) {
			ledR1 = 1;	
		}
		else {
			ledR1 = 0;
		}	
	
		if(0b00000010 & stock_led[slave]) {
			ledR2 = 1;	
		}
		else {
			ledR2 = 0;
		}	

		if(0b00000100 & stock_led[slave]) {
			ledR3 = 1;	
		}
		else {
			ledR3 = 0;
		}	

		if(0b00001000 & stock_led[slave]) {
			ledR4 = 1;	
		}
		else {
			ledR4 = 0;
		}	

		if(0b00010000 & stock_led[slave]) {
			ledR5 = 1;	
		}
		else {
			ledR5 = 0;
		}	

		if(0b00100000 & stock_led[slave]) {
			ledR6 = 1;	
		}
		else {
			ledR6 = 0;
		}	

		if(0b01000001 & stock_led[slave]) {
			ledR7 = 1;	
		}
		else {
			ledR7 = 0;
		}	

		if(ob10000000 & stock_led[slave]) {
			ledR8 = 1;
		}
		else {
			ledR8 = 0;
		}
			
	}	
}
