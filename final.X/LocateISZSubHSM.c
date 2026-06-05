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
    CORRECTLEFT,
    FORWARD_LEFT,
    CORRECTRIGHT,
    BUMPED_LEFT,
    CROSSING_LEFT


} StartingSubHSMState_t;

static const char *StateNames[] = {
	"InitPSubState",
	"LCORNER",
	"RCORNER",
	"FORWARD",
	"CORRECTLEFT",
	"FORWARD_LEFT",
	"CORRECTRIGHT",
    "BUMPED_LEFT",
    "CROSSING_LEFT"
};



#define TURN_TIMER 4
#define TURN_TIME 1000

#define CROSSING_TIMER     7
#define CROSSING_TIMER_MS  4000

#define BACKUP_TIMER 10
#define BACKUP_TIMER_MS 250

#define TANK_OBSTACLE 11
#define TANK_OBSTACLE_MS 930

static uint8_t ignoreTape = FALSE;


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
int turn_counter = 0;
static StartingSubHSMState_t CurrentState = InitPSubState;
static StartingSubHSMState_t PreviousState = InitPSubState;
static uint8_t MyPriority;

// tape state tracking for combo detection

/*******************************************************************************
 * PUBLIC FUNCTIONS                                                            *
 ******************************************************************************/
static void CheckMoveToShooting(void)
{
    if (turn_counter >= 2) {
        // StopDriving();
        ES_Event moveEvent;
        moveEvent.EventType = MOVE_TO_SHOOTING;
        moveEvent.EventParam = 0;
        PostBotHSM(moveEvent);
    }
}
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
    CurrentState = InitPSubState;
    PreviousState = InitPSubState;
    returnEvent = RunLocateISZSubHSM(INIT_EVENT);
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
            turn_counter = 0;
            if (ThisEvent.EventType == ES_INIT) {
                nextState = FORWARD;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }
            break;
        
        case FORWARD: 
            switch(ThisEvent.EventType) {
                case ES_ENTRY: 
                    TurnRight(650);
                    break;
                case RIGHT_TAPE_OFF:
                    nextState = CORRECTLEFT;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;
                
                case LEFT_TAPE_ON:
                    nextState = LCORNER;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case FRONT_TAPE_ON:
                    nextState = LCORNER;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;
                
                case LEFT_BUMPER_PRESSED:
                case RIGHT_BUMPER_PRESSED:
                    nextState = BUMPED_LEFT;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case ES_EXIT:
                    StopDriving();
                    break;

                case ES_NO_EVENT: 
                    break;
            }
            break;

        case CORRECTLEFT:
            switch(ThisEvent.EventType) {
                case ES_ENTRY: 
                    TurnLeft(650);
                    break;
                case RIGHT_TAPE_ON:
                    nextState = FORWARD;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case LEFT_TAPE_ON:
                    nextState = LCORNER;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;
                
                case FRONT_TAPE_ON:
                    nextState = LCORNER;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case LEFT_BUMPER_PRESSED:
                case RIGHT_BUMPER_PRESSED:
                    nextState = BUMPED_LEFT;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case ES_EXIT:
                    StopDriving();
                    break;

                case ES_NO_EVENT: 
                    break;
            }
            break;

        case LCORNER:
            switch(ThisEvent.EventType) {
                case ES_ENTRY: 
                    turn_counter++;
                    CheckMoveToShooting();
                    TankRight(650);
                    ES_Timer_InitTimer(TURN_TIMER, TURN_TIME);
                    break;
                case ES_TIMEOUT:
                    if (ThisEvent.EventParam == TURN_TIMER) {
                        nextState = CORRECTLEFT;
                        makeTransition = TRUE;
                        ThisEvent.EventType = ES_NO_EVENT;
                    }
                    break;
                    
                case ES_EXIT:
                    StopDriving();
                    
                    break;

                case ES_NO_EVENT: 
                    break;
            }
            break;

        case BUMPED_LEFT:
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    DriveBackward(650);
                    ES_Timer_InitTimer(BACKUP_TIMER, BACKUP_TIMER_MS);
                    break;

                case ES_EXIT:
                    StopDriving();
                    break;

                case ES_TIMEOUT:
                    if (ThisEvent.EventParam == BACKUP_TIMER) {
                            TankRight(650);
                            ES_Timer_InitTimer(TANK_OBSTACLE, TANK_OBSTACLE_MS);
                        }
                    

                    if (ThisEvent.EventParam == TANK_OBSTACLE) {
                        // StopDriving();
                        nextState = CROSSING_LEFT;
                        makeTransition = TRUE;
                        ThisEvent.EventType = ES_NO_EVENT;
                    }
                    break;
            }
            break;

        case CROSSING_LEFT:
            switch (ThisEvent.EventType) {

                case ES_ENTRY:
                    printf("In CROSSING state\n");
                    ignoreTape = TRUE;
                    DriveForward(500);
                    ES_Timer_InitTimer(CROSSING_TIMER, CROSSING_TIMER_MS);
                    break;

                case ES_TIMEOUT:
                    if (ThisEvent.EventParam == CROSSING_TIMER) {
                        // StopDriving();
                        ignoreTape = FALSE;
                        // TankRight(500);
                        // ES_Timer_InitTimer(TANK_OBSTACLE, TANK_OBSTACLE_MS);
                    }
                    if (ThisEvent.EventParam == TANK_OBSTACLE) {
                        // StopDriving();
                        nextState = CORRECTRIGHT;
                        makeTransition = TRUE;
                        ThisEvent.EventType = ES_NO_EVENT;
                    }
                    break;

                case FRONT_TAPE_ON:
                case FRONT_TAPE_OFF:
                case LEFT_TAPE_ON:
                case LEFT_TAPE_OFF:
                case RIGHT_TAPE_ON:
                case RIGHT_TAPE_OFF:
                case REAR_TAPE_ON:
                case REAR_TAPE_OFF:

                    if (ignoreTape == TRUE) {
                        ThisEvent.EventType = ES_NO_EVENT;
                    } else {
                        // handle tape normally here
                        if (ThisEvent.EventType == FRONT_TAPE_ON) {
                            // nextState = FORWARD;
                            // makeTransition = TRUE;
                            // ThisEvent.EventType = ES_NO_EVENT;
                            TankLeft(500);
                            ES_Timer_InitTimer(TANK_OBSTACLE, TANK_OBSTACLE_MS);
                        }
                    }
                    break;


            case ES_NO_EVENT:
            default:
                break;
        }
        break;

// FORWARD_LEFT
        case FORWARD_LEFT: 
            switch(ThisEvent.EventType) {
                case ES_ENTRY: 
                    TurnLeft(650);
                    break;
                case LEFT_TAPE_OFF:
                    nextState = CORRECTRIGHT;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;
                
                case RIGHT_TAPE_ON:
                    nextState = RCORNER;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case FRONT_TAPE_ON:
                    nextState = RCORNER;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case ES_EXIT:
                    StopDriving();
                    break;

                case ES_NO_EVENT: 
                    break;
            }
            break;

        case CORRECTRIGHT:
            switch(ThisEvent.EventType) {
                case ES_ENTRY: 
                    TurnRight(650);
                    break;
                case LEFT_TAPE_ON:
                    nextState = FORWARD_LEFT;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case RIGHT_TAPE_ON:
                    nextState = RCORNER;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;
                
                case FRONT_TAPE_ON:
                    nextState = RCORNER;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case ES_EXIT:
                    StopDriving();
                    break;

                case ES_NO_EVENT: 
                    break;
            }
            break;

        case RCORNER:
            switch(ThisEvent.EventType) {
                case ES_ENTRY: 
                    turn_counter++;
                    CheckMoveToShooting();
                    TankLeft(650);
                    ES_Timer_InitTimer(TURN_TIMER, TURN_TIME);
                    
                    break;
                case ES_TIMEOUT:
                    if (ThisEvent.EventParam == TURN_TIMER) {
                        nextState = CORRECTRIGHT;
                        makeTransition = TRUE;
                        ThisEvent.EventType = ES_NO_EVENT;
                    }
                    break;
                    
                case ES_EXIT:
                    StopDriving();
                    
                    break;

                case ES_NO_EVENT: 
                    break;
            }
            break;




        default:
            break;
    } // end switch on Current State

    if (makeTransition == TRUE) {
        RunLocateISZSubHSM(EXIT_EVENT);
        PreviousState = CurrentState;
        CurrentState = nextState;
        RunLocateISZSubHSM(ENTRY_EVENT);
    }

    ES_Tail(); // trace call stack end
    return ThisEvent;
}


/*******************************************************************************
 * PRIVATE FUNCTIONS                                                           *
 ******************************************************************************/