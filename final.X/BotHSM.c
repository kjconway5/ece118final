/*
 * File: TemplateFSM.c
 * Author: J. Edward Carryer
 * Modified: Gabriel H Elkaim
 *
 * Template file to set up a Flat State Machine to work with the Events and Services
 * Frameword (ES_Framework) on the Uno32 for the CMPE-118/L class. Note that this file
 * will need to be modified to fit your exact needs, and most of the names will have
 * to be changed to match your code.
 *
 * This is provided as an example and a good place to start.
 *
 *Generally you will just be modifying the statenames and the run function
 *However make sure you do a find and replace to convert every instance of
 *  "Template" to your current state machine's name
 * History
 * When           Who     What/Why
 * -------------- ---     --------
 * 09/13/13 15:17 ghe      added tattletail functionality and recursive calls
 * 01/15/12 11:12 jec      revisions for Gen2 framework
 * 11/07/11 11:26 jec      made the queue static
 * 10/30/11 17:59 jec      fixed references to CurrentEvent in RunTemplateSM()
 * 10/23/11 18:20 jec      began conversion from SMTemplate.c (02/20/07 rev)
 */


/*******************************************************************************
 * MODULE #INCLUDE                                                             *
 ******************************************************************************/

#include "ES_Configure.h"
#include "ES_Framework.h"
#include "ES_Timers.h"
#include "RoachFSM.h"
#include <BOARD.h>
//Uncomment these for the Roaches
#include "roach.h"
//#include "RoachFrameworkEvents.h"
#include <stdio.h>


/*******************************************************************************
 * MODULE #DEFINES                                                             *
 ******************************************************************************/
#define LEFT_MTR(x) Roach_LeftMtrSpeed(x)
#define RIGHT_MTR(x) Roach_RightMtrSpeed(x)
#define REVERSE_TIMER 0
#define TURN_TIMER 1
#define TURN_TIME 600
#define REVERSE_TIME 1000
#define DRIVE_SPEED 60
#define TURN_SPEED 45

/*******************************************************************************
 * PRIVATE FUNCTION PROTOTYPES                                                 *
 ******************************************************************************/
/* Prototypes for private functions for this machine. They should be functions
   relevant to the behavior of this state machine.*/


/*******************************************************************************
 * PRIVATE MODULE VARIABLES                                                            *
 ******************************************************************************/

/* You will need MyPriority and the state variable; you may need others as well.
 * The type of state variable should match that of enum in header file. */

typedef enum {
    InitPState,
    Hiding,
    Fleeing,
    Reversing,
    Turning,
} RoachFSMState_t;

static const char *StateNames[] = {
	"InitPState",
	"Hiding",
	"Fleeing",
	"Reversing",
	"Turning",
};


static RoachFSMState_t CurrentState = InitPState; // <- change enum name to match ENUM
static uint8_t MyPriority;


/*******************************************************************************
 * PUBLIC FUNCTIONS                                                            *
 ******************************************************************************/

/**
 * @Function InitTemplateFSM(uint8_t Priority)
 * @param Priority - internal variable to track which event queue to use
 * @return TRUE or FALSE
 * @brief This will get called by the framework at the beginning of the code
 *        execution. It will post an ES_INIT event to the appropriate event
 *        queue, which will be handled inside RunTemplateFSM function. Remember
 *        to rename this to something appropriate.
 *        Returns TRUE if successful, FALSE otherwise
 * @author J. Edward Carryer, 2011.10.23 19:25 */
uint8_t InitRoachFSM(uint8_t Priority)
{
    MyPriority = Priority;
    // put us into the Initial PseudoState
    CurrentState = InitPState;
    // post the initial transition event
    if (ES_PostToService(MyPriority, INIT_EVENT) == TRUE) {
        return TRUE;
    } else {
        return FALSE;
    }
}

/**
 * @Function PostTemplateFSM(ES_Event ThisEvent)
 * @param ThisEvent - the event (type and param) to be posted to queue
 * @return TRUE or FALSE
 * @brief This function is a wrapper to the queue posting function, and its name
 *        will be used inside ES_Configure to point to which queue events should
 *        be posted to. Remember to rename to something appropriate.
 *        Returns TRUE if successful, FALSE otherwise
 * @author J. Edward Carryer, 2011.10.23 19:25 */
uint8_t PostRoachFSM(ES_Event ThisEvent)
{
    return ES_PostToService(MyPriority, ThisEvent);
}

/**
 * @Function RunTemplateFSM(ES_Event ThisEvent)
 * @param ThisEvent - the event (type and param) to be responded.
 * @return Event - return event (type and param), in general should be ES_NO_EVENT
 * @brief This function is where you implement the whole of the flat state machine,
 *        as this is called any time a new event is passed to the event queue. This
 *        function will be called recursively to implement the correct order for a
 *        state transition to be: exit current state -> enter next state using the
 *        ES_EXIT and ES_ENTRY events.
 * @note Remember to rename to something appropriate.
 *       Returns ES_NO_EVENT if the event have been "consumed."
 * @author J. Edward Carryer, 2011.10.23 19:25 */
ES_Event RunRoachFSM(ES_Event ThisEvent) {
    uint8_t makeTransition = FALSE;
    RoachFSMState_t nextState;

    ES_Tattle();

    switch (CurrentState) {
        case InitPState:
            if (ThisEvent.EventType == ES_INIT) {
                nextState = Fleeing;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }
            break;

        case Fleeing:
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    LEFT_MTR(DRIVE_SPEED);
                    RIGHT_MTR(DRIVE_SPEED);
                    break;
                case DARK_EVENT:
                    nextState = Hiding;
                    makeTransition = TRUE;
                    break;
                case FRONT_BUMPERS:
                case FRONTLEFT_BUMPER:
                case FRONTRIGHT_BUMPER:
                    nextState = Reversing;
                    makeTransition = TRUE;
                    break;
                case ES_EXIT:
                    LEFT_MTR(0);
                    RIGHT_MTR(0);
                    break;
                default:
                    break;
            }
            break;

        case Hiding:
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    LEFT_MTR(0);
                    RIGHT_MTR(0);
                    break;
                case LIGHT_EVENT:
                    nextState = Fleeing;
                    makeTransition = TRUE;
                    break;
                case ES_EXIT:
                    break;
                default:
                    break;
            }
            break;

        case Reversing:
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    LEFT_MTR(-DRIVE_SPEED);
                    RIGHT_MTR(-DRIVE_SPEED);
                    ES_Timer_InitTimer(REVERSE_TIMER, REVERSE_TIME);
                    break;
                case ES_TIMEOUT:
                case BACK_BUMPERS:
                case BACKLEFT_BUMPER:
                case BACKRIGHT_BUMPER:
                    nextState = Turning;
                    makeTransition = TRUE;
                    break;
                case FRONT_BUMPERS:
                case FRONTLEFT_BUMPER:
                case FRONTRIGHT_BUMPER:
                    break;  // intentionally ignored, drains the queue
                case ES_EXIT:
                    LEFT_MTR(0);
                    RIGHT_MTR(0);
                    ES_Timer_StopTimer(REVERSE_TIMER);
                    break;
                default:
                    break;
            }
            break;

        case Turning:
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    LEFT_MTR(TURN_SPEED);
                    RIGHT_MTR(-TURN_SPEED);
                    ES_Timer_InitTimer(TURN_TIMER, TURN_TIME);
                    break;
                case ES_TIMEOUT:
                    nextState = Fleeing;
                    makeTransition = TRUE;
                    break;
                case FRONT_BUMPERS:
                case FRONTLEFT_BUMPER:
                case FRONTRIGHT_BUMPER:
                    nextState = Reversing;
                    makeTransition = TRUE;
                    break;
                case BACK_BUMPERS:
                case BACKLEFT_BUMPER:
                case BACKRIGHT_BUMPER:
                    break; // intentionally ignored, drains the queue
                case ES_EXIT:
                    LEFT_MTR(0);
                    RIGHT_MTR(0);
                    ES_Timer_StopTimer(TURN_TIMER);
                    break;
                default:
                    break;
            }
            break;

        default:
            break;
    }

    if (makeTransition == TRUE) {
        RunRoachFSM(EXIT_EVENT);
        CurrentState = nextState;
        RunRoachFSM(ENTRY_EVENT);
    }

    ES_Tail();
    return ThisEvent;
}


/*******************************************************************************
 * PRIVATE FUNCTIONS                                                           *
 ******************************************************************************/
