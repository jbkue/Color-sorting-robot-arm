#include<Servo.h>
// creates the servo objects for the robotic arm
Servo base_ser, joint_0, joint_1, wrist, gripper;
// Sets up the arm by attaching the servos to pins in the parenthesises
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1000);
  base_ser.attach(3);
  joint_0.attach(5);
  joint_1.attach(6);
  wrist.attach(9);
  gripper.attach(10);
  stand_by();
}
// base_ser, joint_0, joint_1, wrist, gripper;
// Main loop of the program that will run the code that is located in the brackets
// functions to use
//
// stand_by();
// down(90);
// pan(servo, degree);
// put_down(degree);
// pick_up(degree);
// delay(1000);

void loop() {

}


// pan function used as mainly a supporting function for the following functions
// takes servo and desired poistion as arguments and moves the robot to that position
int pan(Servo ser, int to_pos) {
  int current_servo_pos = ser.read();
  for (int pos = current_servo_pos; pos <= to_pos; pos += 1) {
    // in steps of 1 degree
    ser.write(pos);
    delay(15);
  }
  for (int pos = current_servo_pos; pos >= to_pos; pos -= 1) {
    ser.write(pos);
    delay(15);
  }
}

//Puts the robot arm straight up, and closes the gripper.
int stand_by() {
  pan(base_ser, base_ser.read());
  pan(joint_0, 90);
  pan(joint_1, 90);
  pan(wrist, 135);
  if (gripper.read() != 180) {
    pan(gripper, 180);
  }
}
// puts the arm down at a given position in relation to the base servo
int down(int base_pos) {
  if (base_pos <= 180) {
    pan(base_ser, base_pos);
    delay(100);
    pan(joint_0, 15);
    delay(100);
    pan(joint_1, 140);
    delay(100);
  }
  else if (base_pos > 180) {
    pan(base_ser, base_pos -= 180);
    delay(100);
    pan(joint_0, 165);
    delay(100);
    pan(joint_1, 40);
    delay(100);
  }
}
// Closes the gripper, be careful changing this function as it can draw too much current and burn the motor
int close_gripper() {
  pan(gripper, 100);

}
// opens the gripper by moving the servo motor to 0 degress, the largest it can open
int open_gripper() {
  pan(gripper, 0);
}
// combination of functions used to pick up an object at a given pos in relation to the base ser(baser_ser)
int pick_up(int pos)  {
  stand_by();
  delay(1000);
  open_gripper();
  delay(1000);
  down(pos);
  delay(1000);
  close_gripper();
  delay(1000);
  stand_by();
  delay(1000);
}
// combination of functions used to put down an object as a given pos in relation to the base "servo(baser_ser)"
int put_down(int pos) {
  stand_by();
  delay(1000);
  down(pos);
  delay(1000);
  open_gripper();
  delay(1000);
  stand_by();
  delay(1000);
}
// prints the position of all the servo motors in the serial monitor
String print_pos() {
  String print_pos = "Base Servo: " + base_ser.read();
  print_pos += "\nJoint_0: " + joint_0.read();
  print_pos += "\nJoint_1: " + joint_1.read();
  print_pos += "\nWrist: " + wrist.read();
  print_pos += "\nGripper" + gripper.read();
  return print_pos;
}
