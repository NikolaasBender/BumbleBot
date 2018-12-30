//THESE ARE FOR MEASURING THE BATTERY BANKS
const int bat0 = A0;  
const int bat1 = A1;
const int bat2 = A2;

//THIS IS FOR ENABLING THE RELAYS AND CORRESPOND TO THE RELAYS BETWEEN BANKS
const int enable15 = 1;
const int enable25 = 2;

//NEED THIS TO CORRESPOND TO 3.6v
//DOUBLE CHECK THIS VALUE!!!!
const int discharge = 740;

int 0sens = 0;
int 1sens = 0;
int 2sens = 0;



void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(bat0, INPUT);
  pinMode(bat1, INPUT);
  pinMode(bat2, INPUT);
  
  pinMode(enable15, OUTPUT);
  pinMode(enable25, OUTPUT);
  
  digitalWrite(enable, HIGH);
}

void loop() {
  // read the analog in value:
  0sens = analogRead(bat0);
  1sens = analogRead(bat1);
  2sens = analogRead(bat2);

  // print the results to the Serial Monitor:
  Serial.print("bat0 = %d | bat1 = %d | bat2 = %d", 0sens, 1sens, 2sens);
  

  if(0sens <= discharge || 1sens <= discharge || 2sens <= discharge){
    digitalWrite(enable, LOW);
  }else{
    digitalWrite(enable, HIGH);
  }
  
  delay(200);
}
