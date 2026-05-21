#ifndef SENSORMOTOR_H
#define SENSORMOTOR_H


void SensorMotorInit(void);


int ReadLeftTape(void);
int ReadRightTape(void);
int ReadFrontTape(void);
int ReadRearTape(void);
int ReadLeftBumper(void);
int ReadRightBumper(void);
int ReadTrackWire(void);
int ReadBeacon(void);


void DriveForward(int speed);
void DriveBackward(int speed);
void StopDriving(void);
void TankLeft(int speed);
void TankRight(int speed);


void ShootForward(int speed);
void ShootBackward(int speed);
void StopShooting(void);

#endif // SENSORMOTOR_H
