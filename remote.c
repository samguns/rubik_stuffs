
/*--------------------------------------------------------------------------------------------------------*\
|*                                                                                                        *|
|*                                      - NXT Smooth Tank Drive -                                         *|
|*                                            ROBOTC on NXT                                               *|
|*                                                                                                        *|
|*  This program allows you to drive a robot via remote control using the ROBOTC Debugger.                *|
|*  This particular method uses "Tank Drive" where each side is controlled individually like a tank.      *|
|*  This program also ignores low values that would cause your robot to move when the joysticks fail to   *|
|*  return back to exact center.  You may need to play with the 'threshold' value to get it just right.   *|
|*                                                                                                        *|
|*                                        ROBOT CONFIGURATION                                             *|
|*    NOTES:                                                                                              *|
|*                                                                                                        *|
|*    MOTORS & SENSORS:                                                                                   *|
|*    [I/O Port]              [Name]              [Type]              [Description]                       *|
|*    Port B                  motorB              NXT                 Right motor                         *|
|*    Port C                  motorC              NXT                 Left motor                          *|
\*---------------------------------------------------------------------------------------------------4246-*/

#include "JoystickDriver.c"
#pragma DebuggerWindows("joystickSimple")

task main()
{
  int threshold = 20;             /* Int 'threshold' will allow us to ignore low       */

  nSyncedMotors = synchNone;
  nSyncedMotors = synchBC;

  nMotorEncoder[motorA] = 0;
  nMotorEncoderTarget[motorA] = 10;
  while(true)                            // Infinite loop:
  {
    getJoystickSettings(joystick);
    if(abs(joystick.joy1_y1) > threshold)   // If the right analog stick's Y-axis readings are either above or below the threshold:
    {
    	if (joystick.joy1_y1 < 0)
    	{
    	  //motor[motorC] = 50;
        motor[motorB] = 30;
      }
      else
      {
      	//motor[motorC] = -50;
      	motor[motorB] = -30;
      }
    }
    else
    {
    	motor[motorB] = 0;
    	//motor[motorC] = 0;
    }

    if (abs(joystick.joy1_x1) > threshold)
    {
    	if (joystick.joy1_x1 < 0)
    	{
    	  	motor[motorA] = -20;
    	}
    	else
    			motor[motorA] = 20;
    }
    else
    {
    	motor[motorA] = 0;
    }
  }
}
