/*
 * File: TemplateSubHSM.c
 * Author: J. Edward Carryer
 * Modified: Gabriel H Elkaim
 *
 * Template file to set up a Heirarchical State Machine to work with the Events and
 * Services Framework (ES_Framework) on the Uno32 for the CMPE-118/L class. Note that
 * this file will need to be modified to fit your exact needs, and most of the names
 * will have to be changed to match your code.
 *
 * There is for a substate machine. Make sure it has a unique name
 *
 * This is provided as an example and a good place to start.
 *
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
#include "BOARD.h"
#include "BotHSM.h"
#include "LocateISZSubHSM.h"
#include "sensormotor.h"

/*******************************************************************************
 * MODULE #DEFINES                                                             *
 ******************************************************************************/
typedef enum {
    InitPSubState,
    LCORNER,
    RCORNER,
    FORWARD,
    FORWARD_OFF,
    BUMPED,
    CROSSING,
} StartingSubHSMState_t;

static const char *StateNames[] = {
	"InitPSubState",
	"LCORNER",
	"RCORNER",
	"FORWARD",
    "FORWARD_OFF",
	"BUMPED",
	"CROSSING",
};



/*******************************************************************************
 * PRIVATE FUNCTION PROTOTYPES                                                 *
 ******************************************************************************/
/* Prototypes for private functions for this machine. They should be functions
   relevant to the behavior of this state machine */

/*******************************************************************************
 * PRIVATE MODULE VARIABLES                                                    *
 ******************************************************************************/
/* You will need MyPriority and the state variable; you may need others as well.
 * The type of state variable should match that of enum in header file. */

static StartingSubHSMState_t CurrentState  = InitPSubState;
static StartingSubHSMState_t PreviousState = InitPSubState;
static uint8_t MyPriority;

// tape state tracking for combo detection
static uint8_t frontTapeOn = 0;
static uint8_t rightTapeOn = 0;
static uint8_t leftTapeOn  = 0;


/*******************************************************************************
 * PUBLIC FUNCTIONS                                                            *
 ******************************************************************************/

/**
 * @Function InitLocateISZSubHSM(uint8_t Priority)
 * @param Priority - internal variable to track which event queue to use
 * @return TRUE or FALSE
 * @brief This will get called by the framework at the beginning of the code
 *        execution. It will post an ES_INIT event to the appropriate event
 *        queue, which will be handled inside RunTemplateFSM function. Remember
 *        to rename this to something appropriate.
 *        Returns TRUE if successful, FALSE otherwise
 * @author J. Edward Carryer, 2011.10.23 19:25 */
uint8_t InitLocateISZSubHSM(void) {
    ES_Event returnEvent;
    CurrentState  = InitPSubState;
    PreviousState = InitPSubState;
    returnEvent   = RunLocateISZSubHSM(INIT_EVENT);
    if (returnEvent.EventType == ES_NO_EVENT) {
        return TRUE;
    }
    return FALSE;
}

/**
 * @Function RunLocateISZSubHSM(ES_Event ThisEvent)
 * @param ThisEvent - the event (type and param) to be responded.
 * @return Event - return event (type and param), in general should be ES_NO_EVENT
 * @brief This function is where you implement the whole of the heirarchical state
 *        machine, as this is called any time a new event is passed to the event
 *        queue. This function will be called recursively to implement the correct
 *        order for a state transition to be: exit current state -> enter next state
 *        using the ES_EXIT and ES_ENTRY events.
 * @note Remember to rename to something appropriate.
 *       The lower level state machines are run first, to see if the event is dealt
 *       with there rather than at the current level. ES_EXIT and ES_ENTRY events are
 *       not consumed as these need to pass pack to the higher level state machine.
 * @author J. Edward Carryer, 2011.10.23 19:25
 * @author Gabriel H Elkaim, 2011.10.23 19:25 */
ES_Event RunLocateISZSubHSM(ES_Event ThisEvent) {
    uint8_t makeTransition = FALSE;
    StartingSubHSMState_t nextState;

    ES_Tattle(); // trace call stack

    switch (CurrentState) {
        case InitPSubState:
            if (ThisEvent.EventType == ES_INIT) {
                nextState = FORWARD;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }
            break;

        case FORWARD:
            if (ThisEvent.EventType == ES_ENTRY) {
                DriveForward(500);
                frontTapeOn = 0;  // reset tape flags on entry
                rightTapeOn = 0;
                leftTapeOn  = 0;
            }
            if (ThisEvent.EventType == ES_EXIT) {
                StopDriving();
            }

            // track individual tape sensor states
            if (ThisEvent.EventType == FRONT_TAPE_ON)  { frontTapeOn = 1; }
            if (ThisEvent.EventType == FRONT_TAPE_OFF) { frontTapeOn = 0; }
            if (ThisEvent.EventType == RIGHT_TAPE_ON)  { rightTapeOn = 1; }
            if (ThisEvent.EventType == RIGHT_TAPE_OFF) { rightTapeOn = 0; }
            if (ThisEvent.EventType == LEFT_TAPE_ON)   { leftTapeOn  = 1; }
            if (ThisEvent.EventType == LEFT_TAPE_OFF)  { leftTapeOn  = 0; }

            // right corner: front + right sensors both on
            if (frontTapeOn && rightTapeOn) {
                nextState = RCORNER;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            // left corner: front + left sensors both on
            } else if (frontTapeOn && leftTapeOn) {
                nextState = LCORNER;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }

            if (ThisEvent.EventType == LEFT_BUMPER_PRESSED || ThisEvent.EventType == RIGHT_BUMPER_PRESSED) {
                nextState = BUMPED;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }

            if (ThisEvent.EventType == FRONT_TAPE_OFF) {
                nextState = FORWARD_OFF;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }

            break;

        case FORWARD_OFF:
            if (ThisEvent.EventType == ES_ENTRY) {
                if (ThisEvent.EventType == RIGHT_TAPE_ON) {
                    TurnRight(500);
                } else if (ThisEvent.EventType == LEFT_TAPE_ON) {
                    TurnLeft(500);
                } else {
                    TurnLeft(500);
                }
            }
            if (ThisEvent.EventType == ES_EXIT) {
                StopDriving();
            }
            if (ThisEvent.EventType == FRONT_TAPE_ON) {
                nextState = FORWARD;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }
            break;

        case LCORNER:
            if (ThisEvent.EventType == ES_ENTRY) {
                TankLeft(500);
            }
            if (ThisEvent.EventType == ES_EXIT) {
                StopDriving();
            }
            if (ThisEvent.EventType == FRONT_TAPE_OFF && leftTapeOn == 0) {
                nextState = FORWARD;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }
            break;

        case RCORNER:
            if (ThisEvent.EventType == ES_ENTRY) {
                TankRight(500);
            }
            if (ThisEvent.EventType == ES_EXIT) {
                StopDriving();
            }
            if (ThisEvent.EventType == FRONT_TAPE_OFF &&
                rightTapeOn == 0) {
                nextState = FORWARD;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }
            break;

        case BUMPED:
            if (ThisEvent.EventType == ES_ENTRY) {
                TankLeft(500);
            }
            if (ThisEvent.EventType == ES_EXIT) {
                StopDriving();
            }
            if (ThisEvent.EventType == ES_TIMEOUT) {
                nextState = CROSSING;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }
            break;

        case CROSSING:
            if (ThisEvent.EventType == ES_ENTRY) {
                TankLeft(500);
            }
            if (ThisEvent.EventType == ES_EXIT) {
                StopDriving();
            }
            if (ThisEvent.EventType == FRONT_TAPE_OFF) {
                nextState = FORWARD;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }
            break;

        default:
            break;
    } // end switch on Current State

    if (makeTransition == TRUE) {
        RunLocateISZSubHSM(EXIT_EVENT);
        PreviousState = CurrentState;
        CurrentState  = nextState;
        RunLocateISZSubHSM(ENTRY_EVENT);
    }

    ES_Tail(); // trace call stack end
    return ThisEvent;
}


/*******************************************************************************
 * PRIVATE FUNCTIONS                                                           *
 ******************************************************************************/