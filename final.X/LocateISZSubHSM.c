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
#include <stdio.h>

/*******************************************************************************
 * MODULE #DEFINES                                                             *
 ******************************************************************************/
typedef enum {
    InitPSubState,
    FORWARD,
    FORWARD_OFF,
    TURN_BACK_LEFT,
    TURN_BACK_RIGHT,
    LCORNER,
    RCORNER,
    BUMPED,
    CROSSING,
} TemplateSubHSMState_t;

static const char *StateNames[] = {
	"InitPSubState",
	"FORWARD",
    "FORWARD_OFF",
    "TURN_BACK_LEFT",
    "TURN_BACK_RIGHT",
    "LCORNER",
    "RCORNER",
    "BUMPED",
    "CROSSING",
};



/*******************************************************************************
 * PRIVATE FUNCTION PROTOTYPES                                                 *
 ******************************************************************************/
/* Prototypes for private functions for this machine. They should be functions
   relevant to the behavior of this state machine */

/*******************************************************************************
 * PRIVATE MODULE VARIABLES                                                            *
 ******************************************************************************/
/* You will need MyPriority and the state variable; you may need others as well.
 * The type of state variable should match that of enum in header file. */

static TemplateSubHSMState_t CurrentState = InitPSubState; // <- change name to match ENUM
static uint8_t MyPriority;

// tape state tracking for combo detection

#define BACKUP_TIMER     5
#define BACKUP_TIMER_MS  1000

#define TANK_OBSTACLE     6
#define TANK_OBSTACLE_MS  1500

#define CROSSING_TIMER     7
#define CROSSING_TIMER_MS  4000

#define CORNER_TIMER     8
#define CORNER_TIMER_MS  1250

static uint8_t crossLeft = TRUE;
static uint8_t ignoreTape = FALSE;



/*******************************************************************************
 * PUBLIC FUNCTIONS                                                            *
 ******************************************************************************/

/**
 * @Function InitTemplateSubHSM(uint8_t Priority)
 * @param Priority - internal variable to track which event queue to use
 * @return TRUE or FALSE
 * @brief This will get called by the framework at the beginning of the code
 *        execution. It will post an ES_INIT event to the appropriate event
 *        queue, which will be handled inside RunTemplateFSM function. Remember
 *        to rename this to something appropriate.
 *        Returns TRUE if successful, FALSE otherwise
 * @author J. Edward Carryer, 2011.10.23 19:25 */
uint8_t InitLocateISZSubHSM(void)
{
    ES_Event returnEvent;

    CurrentState = InitPSubState;
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
ES_Event RunLocateISZSubHSM(ES_Event ThisEvent)
{
    uint8_t makeTransition = FALSE; // use to flag transition
    TemplateSubHSMState_t nextState; // <- change type to correct enum

    ES_Tattle(); // trace call stack

    switch (CurrentState) {
        case InitPSubState: // If current state is initial Psedudo State
            if (ThisEvent.EventType == ES_INIT)// only respond to ES_Init
            {
                // this is where you would put any actions associated with the
                // transition from the initial pseudo-state into the actual
                // initial state

                // now put the machine into the actual initial state
                nextState = FORWARD;
                makeTransition = TRUE;
                ThisEvent.EventType = ES_NO_EVENT;
            }
            break;

        case FORWARD: // in the first state, replace this with correct names
            
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    printf("In FORWARD\n");
                    DriveForward(600);
                    break;
                case ES_EXIT:
                    StopDriving();
                    break;

                // case LEFT_TAPE_ON:
                //     nextState = LCORNER;
                //     makeTransition = TRUE;
                //     ThisEvent.EventType = ES_NO_EVENT;
                //     break;
    
                case FRONT_TAPE_ON:
                    nextState = FORWARD_OFF;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case RIGHT_TAPE_ON:
                    nextState = RCORNER;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case RIGHT_BUMPER_PRESSED:
                    nextState = BUMPED;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case LEFT_BUMPER_PRESSED:
                    nextState = BUMPED;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case ES_NO_EVENT:
                default: // all unhandled events pass the event back up to the next level
                    break;
                }
            break;

        case BUMPED: 
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    printf("In BUMPED state\n");
                    DriveBackward(500);
                    ES_Timer_InitTimer(BACKUP_TIMER, BACKUP_TIMER_MS);
                    break;

                case ES_EXIT:
                    StopDriving();
                    break;

                case ES_TIMEOUT:
                    if (ThisEvent.EventParam == BACKUP_TIMER) {
                        if (crossLeft == TRUE) {
                            crossLeft = FALSE;
                            TankLeft(500);
                        } else {
                            crossLeft = TRUE;
                            TankRight(500);
                        }
                        ES_Timer_InitTimer(TANK_OBSTACLE, TANK_OBSTACLE_MS);
                    }

                    if (ThisEvent.EventParam == TANK_OBSTACLE) {
                        nextState = CROSSING;
                        makeTransition = TRUE;
                        ThisEvent.EventType = ES_NO_EVENT;
                    }


                    break;

        //         // case LEFT_BUMPER_RELEASED:
        //         //     nextState = FORWARD;
        //         //     makeTransition = TRUE;
        //         //     ThisEvent.EventType = ES_NO_EVENT;
        //         //     break;

        //         // case RIGHT_BUMPER_RELEASED:
        //         //     nextState = FORWARD;
        //         //     makeTransition = TRUE;
        //         //     ThisEvent.EventType = ES_NO_EVENT;
        //         //     break;


                case ES_NO_EVENT:
                default:
                    break;

            }
            break;
        
        case CROSSING:
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
                        StopDriving();
                        // nextState = FORWARD;
                        // makeTransition = TRUE;
                        // ThisEvent.EventType = ES_NO_EVENT;
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
                            TankRight(500);
                            ES_Timer_InitTimer(TANK_OBSTACLE, TANK_OBSTACLE_MS);
                        }
                    }
                    break;


            case ES_NO_EVENT:
            default:
                break;
        }
        break;
        
        case RCORNER: 
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    printf("In RCORNER state\n");
                    ES_Timer_InitTimer(CORNER_TIMER, CORNER_TIMER_MS);
                    TurnLeft(500);
                    break;
                
                case ES_EXIT:
                    StopDriving();
                    break;

                case ES_TIMEOUT:
                    if (ThisEvent.EventParam == CORNER_TIMER) {
                        nextState = FORWARD;
                        makeTransition = TRUE;
                        ThisEvent.EventType = ES_NO_EVENT;
                    }
                    break;
                
                case ES_NO_EVENT:
                default:
                    break;
            }

            break;

        // case LCORNER: 
        //     switch (ThisEvent.EventType) {
        //         case ES_ENTRY:
        //             printf("In LCORNER state\n");
        //             ES_Timer_InitTimer(CORNER_TIMER, CORNER_TIMER_MS);
        //             TurnLeft(500);
        //             break;
                
        //         case ES_EXIT:
        //             StopDriving();
        //             break;

        //         case ES_TIMEOUT:
        //             if (ThisEvent.EventParam == CORNER_TIMER) {
        //                 nextState = FORWARD;
        //                 makeTransition = TRUE;
        //                 ThisEvent.EventType = ES_NO_EVENT;
        //             }
        //             break;
                
        //         case ES_NO_EVENT:
        //         default:
        //             break;
        //     }

        //     break;

        case FORWARD_OFF: 
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    printf("In FORWARD_OFF state\n");
                    DriveForward(600);
                    //StopDriving();
                    break;
                case ES_EXIT:
                    StopDriving();
                    break;

                case RIGHT_TAPE_ON:
                    nextState = TURN_BACK_RIGHT;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case LEFT_TAPE_ON:
                    nextState = TURN_BACK_LEFT;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case ES_NO_EVENT:
                default:
                    break;
            }
            break;

        case TURN_BACK_LEFT:
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    printf("In TURN_BACK_LEFT state\n");
                    TurnBackRight(600);
                    break;
                case ES_EXIT:
                    StopDriving();
                    break;

                case FRONT_TAPE_ON:
                    nextState = FORWARD;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case ES_NO_EVENT:
                default:
                    break;
            }
            break;

        case TURN_BACK_RIGHT:
            switch (ThisEvent.EventType) {
                case ES_ENTRY:
                    printf("In TURN_BACK_RIGHT state\n");
                    TurnBackLeft(600);
                    break;
                case ES_EXIT:
                    StopDriving();
                    break;

                case FRONT_TAPE_ON:
                    nextState = FORWARD;
                    makeTransition = TRUE;
                    ThisEvent.EventType = ES_NO_EVENT;
                    break;

                case ES_NO_EVENT:
                default:
                    break;
            }
            break;
        default: // all unhandled states fall into here
            break;
        } // end switch on Current State

    if (makeTransition == TRUE) { // making a state transition, send EXIT and ENTRY
        // recursively call the current state with an exit event
        RunLocateISZSubHSM(EXIT_EVENT); // <- rename to your own Run function
        CurrentState = nextState;
        RunLocateISZSubHSM(ENTRY_EVENT); // <- rename to your own Run function
    }

    ES_Tail(); // trace call stack end
    return ThisEvent;
}


/*******************************************************************************
 * PRIVATE FUNCTIONS                                                           *
 ******************************************************************************/

