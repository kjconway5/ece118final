#include "ES_Configure.h"
#include "EventChecker.h"
#include "ES_Events.h"
#include "serial.h"
#include "AD.h"
#include "sensormotor.h"
#include "TemplateFSM.h"

#define SENSOR_THRESHOLD  500
#define DEBOUNCE_COUNT    5    // number of consecutive identical readings required

//#define EVENTCHECKER_TEST
#ifdef EVENTCHECKER_TEST
#include <stdio.h>
#define SaveEvent(x) do {eventName=__func__; storedEvent=x;} while (0)
static const char *eventName;
static ES_Event storedEvent;
#endif

/*******************************************************************************
 * BUMPERS
 ******************************************************************************/
uint8_t BumperEventChecker(void) {
    static uint8_t lastLeft = 0, lastRight = 0;
    static uint8_t cntLeft = 0, cntRight = 0;
    ES_Event thisEvent;
    uint8_t returnVal = FALSE;

    uint8_t curLeft  = ReadLeftBumper()  > SENSOR_THRESHOLD;
    uint8_t curRight = ReadRightBumper() > SENSOR_THRESHOLD;

    if (curLeft != lastLeft) {
        cntLeft++;
        if (cntLeft >= DEBOUNCE_COUNT) {
            lastLeft = curLeft;
            cntLeft = 0;
            thisEvent.EventType = curLeft ? LEFT_BUMPER_PRESSED : LEFT_BUMPER_RELEASED;
            thisEvent.EventParam = curLeft;
            returnVal = TRUE;
#ifndef EVENTCHECKER_TEST
            PostBotHSM(thisEvent);
#else
            SaveEvent(thisEvent);
#endif
        }
    } else {
        cntLeft = 0;
    }

    if (curRight != lastRight) {
        cntRight++;
        if (cntRight >= DEBOUNCE_COUNT) {
            lastRight = curRight;
            cntRight = 0;
            thisEvent.EventType = curRight ? RIGHT_BUMPER_PRESSED : RIGHT_BUMPER_RELEASED;
            thisEvent.EventParam = curRight;
            returnVal = TRUE;
#ifndef EVENTCHECKER_TEST
            PostBotHSM(thisEvent);
#else
            SaveEvent(thisEvent);
#endif
        }
    } else {
        cntRight = 0;
    }

    return returnVal;
}

/*******************************************************************************
 * TAPE SENSORS
 ******************************************************************************/
uint8_t TapeEventChecker(void) {
    static uint8_t lastFront = 0, lastRear = 0, lastLeft = 0, lastRight = 0;
    static uint8_t cntFront = 0, cntRear  = 0, cntLeft  = 0, cntRight  = 0;
    ES_Event thisEvent;
    uint8_t returnVal = FALSE;

    uint8_t curFront = ReadFrontTape() > SENSOR_THRESHOLD;
    uint8_t curRear  = ReadRearTape()  > SENSOR_THRESHOLD;
    uint8_t curLeft  = ReadLeftTape()  > SENSOR_THRESHOLD;
    uint8_t curRight = ReadRightTape() > SENSOR_THRESHOLD;

    // Front
    if (curFront != lastFront) {
        cntFront++;
        if (cntFront >= DEBOUNCE_COUNT) {
            lastFront = curFront;
            cntFront = 0;
            thisEvent.EventType = curFront ? FRONT_TAPE_ON : FRONT_TAPE_OFF;
            thisEvent.EventParam = curFront;
            returnVal = TRUE;
#ifndef EVENTCHECKER_TEST
            PostBotHSM(thisEvent);
#else
            SaveEvent(thisEvent);
#endif
        }
    } else { cntFront = 0; }

    // Rear
    if (curRear != lastRear) {
        cntRear++;
        if (cntRear >= DEBOUNCE_COUNT) {
            lastRear = curRear;
            cntRear = 0;
            thisEvent.EventType = curRear ? REAR_TAPE_ON : REAR_TAPE_OFF;
            thisEvent.EventParam = curRear;
            returnVal = TRUE;
#ifndef EVENTCHECKER_TEST
            PostBotHSM(thisEvent);
#else
            SaveEvent(thisEvent);
#endif
        }
    } else { cntRear = 0; }

    // Left
    if (curLeft != lastLeft) {
        cntLeft++;
        if (cntLeft >= DEBOUNCE_COUNT) {
            lastLeft = curLeft;
            cntLeft = 0;
            thisEvent.EventType = curLeft ? LEFT_TAPE_ON : LEFT_TAPE_OFF;
            thisEvent.EventParam = curLeft;
            returnVal = TRUE;
#ifndef EVENTCHECKER_TEST
            PostTemplateFSM(thisEvent);
#else
            SaveEvent(thisEvent);
#endif
        }
    } else { cntLeft = 0; }

    // Right
    if (curRight != lastRight) {
        cntRight++;
        if (cntRight >= DEBOUNCE_COUNT) {
            lastRight = curRight;
            cntRight = 0;
            thisEvent.EventType = curRight ? RIGHT_TAPE_ON : RIGHT_TAPE_OFF;
            thisEvent.EventParam = curRight;
            returnVal = TRUE;
#ifndef EVENTCHECKER_TEST
            PostBotHSM(thisEvent);
#else
            SaveEvent(thisEvent);
#endif
        }
    } else { cntRight = 0; }

    return returnVal;
}

/*******************************************************************************
 * BEACON
 ******************************************************************************/
// at the top of EventChecker.c, near the other module variables
static uint8_t beaconDetected = 0;
static uint8_t beaconCnt = 0;

uint8_t BeaconEventChecker(void) {
    ES_Event thisEvent;
    uint8_t returnVal = FALSE;

    if (beaconDetected) return FALSE;

    if (ReadBeacon() < SENSOR_THRESHOLD) {
        beaconCnt++;
        if (beaconCnt >= 20) {
            beaconDetected = 1;
            thisEvent.EventType = BEACON_DETECTED;
            thisEvent.EventParam = 0;
            returnVal = TRUE;
#ifndef EVENTCHECKER_TEST
            PostBotHSM(thisEvent);
#else
            SaveEvent(thisEvent);
#endif
        }
    } else {
        beaconCnt = 0;
    }
    return returnVal;
}

void ResetBeaconDetector(void) {
    beaconDetected = 0;
    beaconCnt = 0;
}

/*******************************************************************************
 * TRACKWIRE
 ******************************************************************************/
uint8_t TrackwireEventChecker(void) {
    static uint8_t lastState = 0;
    static uint8_t cnt = 0;
    ES_Event thisEvent;
    uint8_t returnVal = FALSE;

    uint8_t curState = ReadTrackWire() < SENSOR_THRESHOLD;

    if (curState != lastState) {
        cnt++;
        if (cnt >= DEBOUNCE_COUNT) {
            lastState = curState;
            cnt = 0;
            thisEvent.EventType = curState ? TRACKWIRE_DETECTED : TRACKWIRE_LOST;
            thisEvent.EventParam = curState;
            returnVal = TRUE;
#ifndef EVENTCHECKER_TEST
            PostBotHSM(thisEvent);
#else
            SaveEvent(thisEvent);
#endif
        }
    } else { cnt = 0; }

    return returnVal;
}

/*******************************************************************************
 * TEST HARNESS
 ******************************************************************************/
#ifdef EVENTCHECKER_TEST
#include <stdio.h>
static uint8_t(*EventList[])(void) = {EVENT_CHECK_LIST};
void PrintEvent(void);

void main(void) {
    BOARD_Init();
    SensorMotorInit();
    int i;
    printf("\r\nEvent checking test harness for %s", __FILE__);
    while (1) {
        if (IsTransmitEmpty()) {
            for (i = 0; i < sizeof (EventList) >> 2; i++) {
                if (EventList[i]() == TRUE) {
                    PrintEvent();
                    break;
                }
            }
        }
    }
}

void PrintEvent(void) {
    printf("\r\nFunc: %s\tEvent: %s\tParam: 0x%X", eventName,
            EventNames[storedEvent.EventType], storedEvent.EventParam);
}
#endif