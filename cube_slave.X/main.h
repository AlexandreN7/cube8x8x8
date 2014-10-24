#include <xc.h>
#include <pic18f25k80.h>
#include <stdio.h>
#include <stdlib.h>
#include "port.h"
//#include "delays.h"
#include "usart.h"


// I/O designations
//Pin 2 (RA0/AN0) - Address bit 0 (inverted logic input) / Analog Vref input
//Pin 3 (RA1) - Address bit 1 (inverted logic input)
//Pin 4 (RA2) - Address bit 2 (inverted logic input)
//Pin 5 (RA3) - Address bit 3 (inverted logic input)
//Pin 7 (AN4) - Threshold B analog input
//Pin 11 (RC0) - High LED B
//Pin 12 (RC1) - Low LED B
//Pin 13 (RC2) - Output B
//Pin 14 (RC3) - High LED A
//Pin 15 (RC4) - Low LED A
//Pin 16 (RC5) - Spare
//Pin 17 (TX1) - Bus TX
//Pin 18 (RX1) - Bus RX
//Pin 21 (AN10) - Sensor A analog input (scaled down 3:1)
//Pin 22 (AN8) - Threshold A analog input
//Pin 23 (RB2) - Bus DE (driver enable output)
//Pin 24 (RB3) - Bus RE (inverted logic) (receiver enable output)
//Pin 25 (AN9) - Sensor B analog input (scaled down 3:1)
//Pin 26 (RB5) - Output A
//Pin 27 (TX2) - Debug UART TX
//Pin 28 (RX2) - Debug UART RX

#define nADDR0                          RA0
#define nADDR1                          RA1
#define nADDR2                          RA2
#define nADDR3                          RA3

#define VREF_CHANNEL                    0

#define SENSOR_A_CHANNEL                10
#define THRESHOLD_A_CHANNEL             8
#define LOW_LED_A                       RC4
#define HIGH_LED_A                      RC3
#define OUTPUT_A                        RB5

#define SENSOR_B_CHANNEL                9
#define THRESHOLD_B_CHANNEL             4
#define LOW_LED_B                       RC1
#define HIGH_LED_B                      RC0
#define OUTPUT_B                        RC2

#define BUS_DE                          RB2
#define nBUS_RE                         RB3

#define SPARE                           RC5

#define TRUE                1
#define FALSE               0

#define ON              1
#define OFF                 0


// Global variables

char msg[80];

// Function prototypes
//void readSensor(unsigned char sensor);
//unsigned int readVoltage(unsigned char channel);
//void output(unsigned char channel, unsigned char outputType, unsigned char onOff);
unsigned char readAddress();