#include "JoystickDriver.c"

task main()
{
	long x, y, z;
  string displayx, displayy, displayz;

  nSyncedMotors = synchNone;
  nSyncedMotors = synchBC;

  nMotorEncoder[motorA] = 0;
  nMotorEncoderTarget[motorA] = 10;

  while(true)
  {
  	x = y = z = 0;
    x = messageParm[0];
    y = messageParm[1];
    z = messageParm[2];

    //Formats the variables into a 'Value x: ' format and displays each on a seperate line
    stringFormat(displayx, "Value x: %d", x);
    stringFormat(displayy, "Value y: %d", y);
    stringFormat(displayz, "Value z: %d", z);

    displayCenteredTextLine(0, displayx);
    displayCenteredTextLine(2, displayy);
    displayCenteredTextLine(4, displayz);
    ClearMessage();

    if (0 == z)
    {
    	motor[motorA] = 0;
    	motor[motorB] = 0;
    	ClearMessage();
    	continue;
    }

    if (0 == x)
    {
    	if (1 == y)
    	  motor[motorB] = x;
    	else
    		motor[motorB] = 100 - x - 100;
    }

    if (1 == x)
    {
    	if (1 == y)
    		motor[motorA] = -10;
      else
      	motor[motorA] = 10;

      motor[motorA] = 0;
    }

    wait1Msec(300);
  }
}
