/*
 * File:   sensormotor.c
 * Author: kye
 *
 * Created on May 21, 2026, 5:14 PM
 */


#include <stdio.h>
#include "xc.h"
#include "AD.h"
#include "BOARD.h"
#include "IO_Ports.h"
#include "LED.h"
#include "pwm.h"
#include "serial.h"
#include "sensormotor.h"

#define LeftTapePin (AD_PORTV3)
#define RightTapePin (AD_PORTV4)
#define FrontTapePin (AD_PORTV5)
#define RearTapePin (AD_PORTV6)

#define LeftBumperPin (AD_PORTV7)
#define RightBumperPin (AD_PORTV8)

#define TrackWirePin (AD_PORTW3)
#define BeaconPin (AD_PORTW4)

#define LeftDriveMotorPWM (PWM_PORTY12)
#define RightDriveMotorPWM (PWM_PORTY10)

#define LeftShootMotorPWM (PWM_PORTY04)
#define RightShootMotorPWM (PWM_PORTX11)

#define LeftDriveIN1 (PIN3)
#define LeftDriveIN2 (PIN4)
#define RightDriveIN1 (PIN5)
#define RightDriveIN2 (PIN6)

#define LeftShooterIN1 (PIN7)
#define LeftShooterIN2 (PIN8)
#define RightShooterIN1 (PIN9)
#define RightShooterIN2 (PIN10)

void SensorMotorInit(void) {
    BOARD_Init();
    AD_Init();
    PWM_Init();

    AD_AddPins(LeftTapePin);
    AD_AddPins(RightTapePin);
    AD_AddPins(FrontTapePin);
    AD_AddPins(RearTapePin);
    AD_AddPins(LeftBumperPin);
    AD_AddPins(RightBumperPin);
    AD_AddPins(TrackWirePin);
    AD_AddPins(BeaconPin);

    PWM_SetFrequency(PWM_DEFAULT_FREQUENCY);
    PWM_AddPins(LeftDriveMotorPWM);
    PWM_AddPins(RightDriveMotorPWM);
    PWM_AddPins(LeftShootMotorPWM);
    PWM_AddPins(RightShootMotorPWM);

    IO_PortsSetPortOutputs(PORTZ, LeftDriveIN1);
    IO_PortsSetPortOutputs(PORTZ, LeftDriveIN2);
    IO_PortsSetPortOutputs(PORTZ, RightDriveIN1);
    IO_PortsSetPortOutputs(PORTZ, RightDriveIN2);
    IO_PortsSetPortOutputs(PORTZ, LeftShooterIN1);
    IO_PortsSetPortOutputs(PORTZ, LeftShooterIN2);
    IO_PortsSetPortOutputs(PORTZ, RightShooterIN1);
    IO_PortsSetPortOutputs(PORTZ, RightShooterIN2);

}

int ReadLeftTape(void) {
    return AD_ReadADPin(LeftTapePin);
}

int ReadFrontTape(void) {
    return AD_ReadADPin(FrontTapePin);
}

int ReadRightTape(void) {
    return AD_ReadADPin(RightTapePin);
}

int ReadRearTape(void) {
    return AD_ReadADPin(RearTapePin);
}

int ReadLeftBumper(void) {
    return AD_ReadADPin(LeftBumperPin);
}

int ReadRightBumper(void) {
    return AD_ReadADPin(RightBumperPin);
}

int ReadTrackWire(void) { 
    return AD_ReadADPin(TrackWirePin); 
}

int ReadBeacon(void) {
    return AD_ReadADPin(BeaconPin);
}

void DriveForward(int speed) {
    IO_PortsSetPortBits(PORTZ, LeftDriveIN1);
    IO_PortsClearPortBits(PORTZ, LeftDriveIN2);

    IO_PortsSetPortBits(PORTZ, RightDriveIN1);
    IO_PortsClearPortBits(PORTZ, RightDriveIN2);

    PWM_SetDutyCycle(LeftDriveMotorPWM, speed);
    PWM_SetDutyCycle(RightDriveMotorPWM, speed);
}

void DriveBackward(int speed) {
    IO_PortsSetPortBits(PORTZ, LeftDriveIN2);
    IO_PortsClearPortBits(PORTZ, LeftDriveIN1);

    IO_PortsSetPortBits(PORTZ, RightDriveIN2);
    IO_PortsClearPortBits(PORTZ, RightDriveIN1);
    
    PWM_SetDutyCycle(LeftDriveMotorPWM, speed);
    PWM_SetDutyCycle(RightDriveMotorPWM, speed);
}

void ShootForward(int speed) {
    IO_PortsClearPortBits(PORTZ, LeftShooterIN1);
    IO_PortsSetPortBits(PORTZ, LeftShooterIN2);

    IO_PortsClearPortBits(PORTZ, RightShooterIN1);
    IO_PortsSetPortBits(PORTZ, RightShooterIN2);

    PWM_SetDutyCycle(LeftShootMotorPWM, speed);
    PWM_SetDutyCycle(RightShootMotorPWM, speed);
}

void ShootBackward(int speed) {
    IO_PortsSetPortBits(PORTZ, LeftShooterIN2);
    IO_PortsClearPortBits(PORTZ, LeftShooterIN1);

    IO_PortsSetPortBits(PORTZ, RightShooterIN2);
    IO_PortsClearPortBits(PORTZ, RightShooterIN1);

    PWM_SetDutyCycle(LeftShootMotorPWM, speed);
    PWM_SetDutyCycle(RightShootMotorPWM, speed);
}

void StopDriving(void) {
    IO_PortsClearPortBits(PORTZ, LeftDriveIN2);
    IO_PortsClearPortBits(PORTZ, LeftDriveIN1);

    IO_PortsClearPortBits(PORTZ, RightDriveIN2);
    IO_PortsClearPortBits(PORTZ, RightDriveIN1);

    PWM_SetDutyCycle(LeftDriveMotorPWM, 0);
    PWM_SetDutyCycle(RightDriveMotorPWM, 0);    
} 

void TankLeft(int speed) {
    IO_PortsSetPortBits(PORTZ, LeftDriveIN2);
    IO_PortsClearPortBits(PORTZ, LeftDriveIN1);

    IO_PortsSetPortBits(PORTZ, RightDriveIN1);
    IO_PortsClearPortBits(PORTZ, RightDriveIN2);

    PWM_SetDutyCycle(LeftDriveMotorPWM, speed);
    PWM_SetDutyCycle(RightDriveMotorPWM, speed);
}

void TankRight(int speed) {
    IO_PortsSetPortBits(PORTZ, LeftDriveIN1);
    IO_PortsClearPortBits(PORTZ, LeftDriveIN2);

    IO_PortsSetPortBits(PORTZ, RightDriveIN2);
    IO_PortsClearPortBits(PORTZ, RightDriveIN1);

    PWM_SetDutyCycle(LeftDriveMotorPWM, speed);
    PWM_SetDutyCycle(RightDriveMotorPWM, speed);
}

void StopShooting(void) {
    IO_PortsClearPortBits(PORTZ, LeftShooterIN1);
    IO_PortsClearPortBits(PORTZ, LeftShooterIN2);

    IO_PortsClearPortBits(PORTZ, RightShooterIN1);
    IO_PortsClearPortBits(PORTZ, RightShooterIN2);

    PWM_SetDutyCycle(LeftShootMotorPWM, 0);
    PWM_SetDutyCycle(RightShootMotorPWM, 0);
}

void TurnRight(int speed) {
    IO_PortsSetPortBits(PORTZ, LeftDriveIN1);
    IO_PortsClearPortBits(PORTZ, LeftDriveIN2);

    IO_PortsClearPortBits(PORTZ, RightDriveIN2);
    IO_PortsClearPortBits(PORTZ, RightDriveIN1);

    PWM_SetDutyCycle(LeftDriveMotorPWM, speed);
    PWM_SetDutyCycle(RightDriveMotorPWM, 0);
}

void TurnLeft(int speed) {
    IO_PortsSetPortBits(PORTZ, LeftDriveIN1);
    IO_PortsClearPortBits(PORTZ, LeftDriveIN2);

    IO_PortsClearPortBits(PORTZ, RightDriveIN2);
    IO_PortsClearPortBits(PORTZ, RightDriveIN1);

    PWM_SetDutyCycle(LeftDriveMotorPWM, speed);
    PWM_SetDutyCycle(RightDriveMotorPWM, 0);
}