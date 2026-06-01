#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Include project Makefile
ifeq "${IGNORE_LOCAL}" "TRUE"
# do not include local makefile. User is passing all local related variables already
else
include Makefile
# Include makefile containing local settings
ifeq "$(wildcard nbproject/Makefile-local-default.mk)" "nbproject/Makefile-local-default.mk"
include nbproject/Makefile-local-default.mk
endif
endif

# Environment
MKDIR=mkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=default
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=elf
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/final.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=hex
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/final.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
endif

ifeq ($(COMPARE_BUILD), true)
COMPARISON_BUILD=-mafrlcsj
else
COMPARISON_BUILD=
endif

# Object Directory
OBJECTDIR=build/${CND_CONF}/${IMAGE_TYPE}

# Distribution Directory
DISTDIR=dist/${CND_CONF}/${IMAGE_TYPE}

# Source Files Quoted if spaced
SOURCEFILES_QUOTED_IF_SPACED=../ECE118/src/AD.c ../ECE118/src/BOARD.c ../ECE118/src/ES_CheckEvents.c ../ECE118/src/ES_Framework.c ../ECE118/src/ES_KeyboardInput.c ../ECE118/src/ES_PostList.c ../ECE118/src/ES_Queue.c ../ECE118/src/ES_TattleTale.c ../ECE118/src/ES_Timers.c ../ECE118/src/IO_Ports.c ../ECE118/src/LED.c ../ECE118/src/pwm.c ../ECE118/src/RC_Servo.c ../ECE118/src/serial.c ../ECE118/src/timers.c BallService.c BotHSM.c EventChecker.c LocateISZSubHSM.c sensormotor.c TemplateES_Main.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/_ext/1347132459/AD.o ${OBJECTDIR}/_ext/1347132459/BOARD.o ${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o ${OBJECTDIR}/_ext/1347132459/ES_Framework.o ${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o ${OBJECTDIR}/_ext/1347132459/ES_PostList.o ${OBJECTDIR}/_ext/1347132459/ES_Queue.o ${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o ${OBJECTDIR}/_ext/1347132459/ES_Timers.o ${OBJECTDIR}/_ext/1347132459/IO_Ports.o ${OBJECTDIR}/_ext/1347132459/LED.o ${OBJECTDIR}/_ext/1347132459/pwm.o ${OBJECTDIR}/_ext/1347132459/RC_Servo.o ${OBJECTDIR}/_ext/1347132459/serial.o ${OBJECTDIR}/_ext/1347132459/timers.o ${OBJECTDIR}/BallService.o ${OBJECTDIR}/BotHSM.o ${OBJECTDIR}/EventChecker.o ${OBJECTDIR}/LocateISZSubHSM.o ${OBJECTDIR}/sensormotor.o ${OBJECTDIR}/TemplateES_Main.o
POSSIBLE_DEPFILES=${OBJECTDIR}/_ext/1347132459/AD.o.d ${OBJECTDIR}/_ext/1347132459/BOARD.o.d ${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o.d ${OBJECTDIR}/_ext/1347132459/ES_Framework.o.d ${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o.d ${OBJECTDIR}/_ext/1347132459/ES_PostList.o.d ${OBJECTDIR}/_ext/1347132459/ES_Queue.o.d ${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o.d ${OBJECTDIR}/_ext/1347132459/ES_Timers.o.d ${OBJECTDIR}/_ext/1347132459/IO_Ports.o.d ${OBJECTDIR}/_ext/1347132459/LED.o.d ${OBJECTDIR}/_ext/1347132459/pwm.o.d ${OBJECTDIR}/_ext/1347132459/RC_Servo.o.d ${OBJECTDIR}/_ext/1347132459/serial.o.d ${OBJECTDIR}/_ext/1347132459/timers.o.d ${OBJECTDIR}/BallService.o.d ${OBJECTDIR}/BotHSM.o.d ${OBJECTDIR}/EventChecker.o.d ${OBJECTDIR}/LocateISZSubHSM.o.d ${OBJECTDIR}/sensormotor.o.d ${OBJECTDIR}/TemplateES_Main.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/_ext/1347132459/AD.o ${OBJECTDIR}/_ext/1347132459/BOARD.o ${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o ${OBJECTDIR}/_ext/1347132459/ES_Framework.o ${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o ${OBJECTDIR}/_ext/1347132459/ES_PostList.o ${OBJECTDIR}/_ext/1347132459/ES_Queue.o ${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o ${OBJECTDIR}/_ext/1347132459/ES_Timers.o ${OBJECTDIR}/_ext/1347132459/IO_Ports.o ${OBJECTDIR}/_ext/1347132459/LED.o ${OBJECTDIR}/_ext/1347132459/pwm.o ${OBJECTDIR}/_ext/1347132459/RC_Servo.o ${OBJECTDIR}/_ext/1347132459/serial.o ${OBJECTDIR}/_ext/1347132459/timers.o ${OBJECTDIR}/BallService.o ${OBJECTDIR}/BotHSM.o ${OBJECTDIR}/EventChecker.o ${OBJECTDIR}/LocateISZSubHSM.o ${OBJECTDIR}/sensormotor.o ${OBJECTDIR}/TemplateES_Main.o

# Source Files
SOURCEFILES=../ECE118/src/AD.c ../ECE118/src/BOARD.c ../ECE118/src/ES_CheckEvents.c ../ECE118/src/ES_Framework.c ../ECE118/src/ES_KeyboardInput.c ../ECE118/src/ES_PostList.c ../ECE118/src/ES_Queue.c ../ECE118/src/ES_TattleTale.c ../ECE118/src/ES_Timers.c ../ECE118/src/IO_Ports.c ../ECE118/src/LED.c ../ECE118/src/pwm.c ../ECE118/src/RC_Servo.c ../ECE118/src/serial.c ../ECE118/src/timers.c BallService.c BotHSM.c EventChecker.c LocateISZSubHSM.c sensormotor.c TemplateES_Main.c



CFLAGS=
ASFLAGS=
LDLIBSOPTIONS=

############# Tool locations ##########################################
# If you copy a project from one host to another, the path where the  #
# compiler is installed may be different.                             #
# If you open this project with MPLAB X in the new host, this         #
# makefile will be regenerated and the paths will be corrected.       #
#######################################################################
# fixDeps replaces a bunch of sed/cat/printf statements that slow down the build
FIXDEPS=fixDeps

.build-conf:  ${BUILD_SUBPROJECTS}
ifneq ($(INFORMATION_MESSAGE), )
	@echo $(INFORMATION_MESSAGE)
endif
	${MAKE}  -f nbproject/Makefile-default.mk ${DISTDIR}/final.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

MP_PROCESSOR_OPTION=32MX320F128H
MP_LINKER_FILE_OPTION=,--script="../ECE118/bootloader320.ld"
# ------------------------------------------------------------------------------------
# Rules for buildStep: assemble
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assembleWithPreprocess
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compile
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${OBJECTDIR}/_ext/1347132459/AD.o: ../ECE118/src/AD.c  .generated_files/flags/default/41bcdd0f42c2e734232d541da1db509afe725c37 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/AD.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/AD.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/AD.o.d" -o ${OBJECTDIR}/_ext/1347132459/AD.o ../ECE118/src/AD.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/BOARD.o: ../ECE118/src/BOARD.c  .generated_files/flags/default/c92c9c072494e16ee59606ed7560c12ad7c68739 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/BOARD.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/BOARD.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/BOARD.o.d" -o ${OBJECTDIR}/_ext/1347132459/BOARD.o ../ECE118/src/BOARD.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o: ../ECE118/src/ES_CheckEvents.c  .generated_files/flags/default/97ea0d7530d490ffb6da32765107dc3492a7fa8e .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o ../ECE118/src/ES_CheckEvents.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_Framework.o: ../ECE118/src/ES_Framework.c  .generated_files/flags/default/f4f69086a0f65c0e776a7f4f6fe53901e40f1ead .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Framework.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Framework.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_Framework.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_Framework.o ../ECE118/src/ES_Framework.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o: ../ECE118/src/ES_KeyboardInput.c  .generated_files/flags/default/30485ac68a5a90e19b5599ef103d966cf2d8fe4f .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o ../ECE118/src/ES_KeyboardInput.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_PostList.o: ../ECE118/src/ES_PostList.c  .generated_files/flags/default/e130090bd4c9cc92e589aaabb242f0730bb850cd .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_PostList.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_PostList.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_PostList.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_PostList.o ../ECE118/src/ES_PostList.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_Queue.o: ../ECE118/src/ES_Queue.c  .generated_files/flags/default/ab7f7cb41f8b9008296a612396dc96899e1326fc .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Queue.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Queue.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_Queue.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_Queue.o ../ECE118/src/ES_Queue.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o: ../ECE118/src/ES_TattleTale.c  .generated_files/flags/default/d588e4010e41a8a20b686b9da1d786336f041bf9 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o ../ECE118/src/ES_TattleTale.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_Timers.o: ../ECE118/src/ES_Timers.c  .generated_files/flags/default/77018f8476af054bd198fad79119831eacc7bf29 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Timers.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Timers.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_Timers.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_Timers.o ../ECE118/src/ES_Timers.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/IO_Ports.o: ../ECE118/src/IO_Ports.c  .generated_files/flags/default/719baab22552f2dbe709090e7d2a4ba70ff0c3b1 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/IO_Ports.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/IO_Ports.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/IO_Ports.o.d" -o ${OBJECTDIR}/_ext/1347132459/IO_Ports.o ../ECE118/src/IO_Ports.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/LED.o: ../ECE118/src/LED.c  .generated_files/flags/default/136cc6df9b6028d535457d3256d34a2fdc7b4107 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/LED.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/LED.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/LED.o.d" -o ${OBJECTDIR}/_ext/1347132459/LED.o ../ECE118/src/LED.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/pwm.o: ../ECE118/src/pwm.c  .generated_files/flags/default/634b54da17cc69f59955708c4e7dd4a11b405e8c .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/pwm.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/pwm.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/pwm.o.d" -o ${OBJECTDIR}/_ext/1347132459/pwm.o ../ECE118/src/pwm.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/RC_Servo.o: ../ECE118/src/RC_Servo.c  .generated_files/flags/default/e6cb3eb27dd2d5bbb0a48088994e1beb152bd111 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/RC_Servo.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/RC_Servo.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/RC_Servo.o.d" -o ${OBJECTDIR}/_ext/1347132459/RC_Servo.o ../ECE118/src/RC_Servo.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/serial.o: ../ECE118/src/serial.c  .generated_files/flags/default/5f07099a3b3f464d0ab975e99938348e47f35e13 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/serial.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/serial.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/serial.o.d" -o ${OBJECTDIR}/_ext/1347132459/serial.o ../ECE118/src/serial.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/timers.o: ../ECE118/src/timers.c  .generated_files/flags/default/704dfe35df0813351ff6140a41340bd784020bf0 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/timers.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/timers.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/timers.o.d" -o ${OBJECTDIR}/_ext/1347132459/timers.o ../ECE118/src/timers.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/BallService.o: BallService.c  .generated_files/flags/default/37d1977187281b04e5e5420c2e617d0eb77cd492 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/BallService.o.d 
	@${RM} ${OBJECTDIR}/BallService.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/BallService.o.d" -o ${OBJECTDIR}/BallService.o BallService.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/BotHSM.o: BotHSM.c  .generated_files/flags/default/9be6d8e72f5e4ab6d96f2d1e4f1f8917a8b392b5 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/BotHSM.o.d 
	@${RM} ${OBJECTDIR}/BotHSM.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/BotHSM.o.d" -o ${OBJECTDIR}/BotHSM.o BotHSM.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/EventChecker.o: EventChecker.c  .generated_files/flags/default/76e277d6898f8ba73f9e58f86f1b562f895cdcad .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/EventChecker.o.d 
	@${RM} ${OBJECTDIR}/EventChecker.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/EventChecker.o.d" -o ${OBJECTDIR}/EventChecker.o EventChecker.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/LocateISZSubHSM.o: LocateISZSubHSM.c  .generated_files/flags/default/7cb099e2038fcb48a0d00bc4af34edc979575ed7 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/LocateISZSubHSM.o.d 
	@${RM} ${OBJECTDIR}/LocateISZSubHSM.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/LocateISZSubHSM.o.d" -o ${OBJECTDIR}/LocateISZSubHSM.o LocateISZSubHSM.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/sensormotor.o: sensormotor.c  .generated_files/flags/default/27d8497d7d919ffe6b77ade7f9ecf6a92a1a5cb2 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/sensormotor.o.d 
	@${RM} ${OBJECTDIR}/sensormotor.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/sensormotor.o.d" -o ${OBJECTDIR}/sensormotor.o sensormotor.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/TemplateES_Main.o: TemplateES_Main.c  .generated_files/flags/default/45bb081137eaac1cd8115a32440b9972244b9e3a .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/TemplateES_Main.o.d 
	@${RM} ${OBJECTDIR}/TemplateES_Main.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_SIMULATOR=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/TemplateES_Main.o.d" -o ${OBJECTDIR}/TemplateES_Main.o TemplateES_Main.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
else
${OBJECTDIR}/_ext/1347132459/AD.o: ../ECE118/src/AD.c  .generated_files/flags/default/e255e50572fdbe19090d36d8d84976d82c4175a .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/AD.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/AD.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/AD.o.d" -o ${OBJECTDIR}/_ext/1347132459/AD.o ../ECE118/src/AD.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/BOARD.o: ../ECE118/src/BOARD.c  .generated_files/flags/default/7a3070b8d81745563c03e300b66681a2f5019834 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/BOARD.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/BOARD.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/BOARD.o.d" -o ${OBJECTDIR}/_ext/1347132459/BOARD.o ../ECE118/src/BOARD.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o: ../ECE118/src/ES_CheckEvents.c  .generated_files/flags/default/b674fc7e0cd69f5772f38c7739477299f7e80cdd .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_CheckEvents.o ../ECE118/src/ES_CheckEvents.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_Framework.o: ../ECE118/src/ES_Framework.c  .generated_files/flags/default/26fc481fadf96a64417df17c946c71ac2f74d89b .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Framework.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Framework.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_Framework.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_Framework.o ../ECE118/src/ES_Framework.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o: ../ECE118/src/ES_KeyboardInput.c  .generated_files/flags/default/d4e7ef6e3624900899e38113f3bbd2e999126f78 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_KeyboardInput.o ../ECE118/src/ES_KeyboardInput.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_PostList.o: ../ECE118/src/ES_PostList.c  .generated_files/flags/default/ae72b2cbd8394920682aaa27287c6338503eacc1 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_PostList.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_PostList.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_PostList.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_PostList.o ../ECE118/src/ES_PostList.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_Queue.o: ../ECE118/src/ES_Queue.c  .generated_files/flags/default/2608609ca4eda148d5af6fc702e31cd3c238bc63 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Queue.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Queue.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_Queue.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_Queue.o ../ECE118/src/ES_Queue.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o: ../ECE118/src/ES_TattleTale.c  .generated_files/flags/default/20e5a62370327b4b94b019c8a28803d0539cae7c .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_TattleTale.o ../ECE118/src/ES_TattleTale.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/ES_Timers.o: ../ECE118/src/ES_Timers.c  .generated_files/flags/default/d92b22426bcbcb8346277ede11e9abc06088fb7a .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Timers.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/ES_Timers.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/ES_Timers.o.d" -o ${OBJECTDIR}/_ext/1347132459/ES_Timers.o ../ECE118/src/ES_Timers.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/IO_Ports.o: ../ECE118/src/IO_Ports.c  .generated_files/flags/default/f739ab811decc53e5722f3015a66e4cc88483103 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/IO_Ports.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/IO_Ports.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/IO_Ports.o.d" -o ${OBJECTDIR}/_ext/1347132459/IO_Ports.o ../ECE118/src/IO_Ports.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/LED.o: ../ECE118/src/LED.c  .generated_files/flags/default/864aecf2b7a3a68f5d4a5d7585492fb953df63cf .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/LED.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/LED.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/LED.o.d" -o ${OBJECTDIR}/_ext/1347132459/LED.o ../ECE118/src/LED.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/pwm.o: ../ECE118/src/pwm.c  .generated_files/flags/default/3482022a7f3d404255fabb9d62020a7eb1241937 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/pwm.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/pwm.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/pwm.o.d" -o ${OBJECTDIR}/_ext/1347132459/pwm.o ../ECE118/src/pwm.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/RC_Servo.o: ../ECE118/src/RC_Servo.c  .generated_files/flags/default/be41d59778ba5bdf7dd8941c626fc76ef7778f94 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/RC_Servo.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/RC_Servo.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/RC_Servo.o.d" -o ${OBJECTDIR}/_ext/1347132459/RC_Servo.o ../ECE118/src/RC_Servo.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/serial.o: ../ECE118/src/serial.c  .generated_files/flags/default/f098f9a08642329bd171ee040bfd0842e25f95e9 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/serial.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/serial.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/serial.o.d" -o ${OBJECTDIR}/_ext/1347132459/serial.o ../ECE118/src/serial.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/_ext/1347132459/timers.o: ../ECE118/src/timers.c  .generated_files/flags/default/d16869a643ec89fb82eacc8e807770892d08069d .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1347132459" 
	@${RM} ${OBJECTDIR}/_ext/1347132459/timers.o.d 
	@${RM} ${OBJECTDIR}/_ext/1347132459/timers.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/_ext/1347132459/timers.o.d" -o ${OBJECTDIR}/_ext/1347132459/timers.o ../ECE118/src/timers.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/BallService.o: BallService.c  .generated_files/flags/default/9c89ed219f74bb7b4679ae2828445deb9fe85ca4 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/BallService.o.d 
	@${RM} ${OBJECTDIR}/BallService.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/BallService.o.d" -o ${OBJECTDIR}/BallService.o BallService.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/BotHSM.o: BotHSM.c  .generated_files/flags/default/b7c04fbc66aaef4e6b07f50c66a2c4296e30d059 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/BotHSM.o.d 
	@${RM} ${OBJECTDIR}/BotHSM.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/BotHSM.o.d" -o ${OBJECTDIR}/BotHSM.o BotHSM.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/EventChecker.o: EventChecker.c  .generated_files/flags/default/428b190f528735f91f3900ab1e44fbe6658dd399 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/EventChecker.o.d 
	@${RM} ${OBJECTDIR}/EventChecker.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/EventChecker.o.d" -o ${OBJECTDIR}/EventChecker.o EventChecker.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/LocateISZSubHSM.o: LocateISZSubHSM.c  .generated_files/flags/default/6d184ce372ddddd5ba2715dc5cdf1144829f448c .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/LocateISZSubHSM.o.d 
	@${RM} ${OBJECTDIR}/LocateISZSubHSM.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/LocateISZSubHSM.o.d" -o ${OBJECTDIR}/LocateISZSubHSM.o LocateISZSubHSM.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/sensormotor.o: sensormotor.c  .generated_files/flags/default/15a9b8b79cecdc42ff2ccc0b36decf87a84c8f3 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/sensormotor.o.d 
	@${RM} ${OBJECTDIR}/sensormotor.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/sensormotor.o.d" -o ${OBJECTDIR}/sensormotor.o sensormotor.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
${OBJECTDIR}/TemplateES_Main.o: TemplateES_Main.c  .generated_files/flags/default/7c2d815211eabe3affef9af0b34f605d164c36bc .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/TemplateES_Main.o.d 
	@${RM} ${OBJECTDIR}/TemplateES_Main.o 
	${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -ffunction-sections -fdata-sections -O1 -fno-common -I"." -I"../ECE118/include" -MP -MMD -MF "${OBJECTDIR}/TemplateES_Main.o.d" -o ${OBJECTDIR}/TemplateES_Main.o TemplateES_Main.c    -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mdfp="${DFP_DIR}"  
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compileCPP
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${DISTDIR}/final.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk    ../ECE118/bootloader320.ld
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -g -mdebugger -D__MPLAB_DEBUGGER_SIMULATOR=1 -mprocessor=$(MP_PROCESSOR_OPTION)  -o ${DISTDIR}/final.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}          -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)      -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1,-D=__DEBUG_D,--defsym=__MPLAB_DEBUGGER_SIMULATOR=1,--defsym=_min_heap_size=0,--gc-sections,--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--memorysummary,${DISTDIR}/memoryfile.xml -mdfp="${DFP_DIR}"
	
else
${DISTDIR}/final.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk   ../ECE118/bootloader320.ld
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE)  -mprocessor=$(MP_PROCESSOR_OPTION)  -o ${DISTDIR}/final.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}          -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--defsym=_min_heap_size=0,--gc-sections,--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--memorysummary,${DISTDIR}/memoryfile.xml -mdfp="${DFP_DIR}"
	${MP_CC_DIR}/xc32-bin2hex ${DISTDIR}/final.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} 
endif


# Subprojects
.build-subprojects:


# Subprojects
.clean-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${OBJECTDIR}
	${RM} -r ${DISTDIR}

# Enable dependency checking
.dep.inc: .depcheck-impl

DEPFILES=$(wildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
