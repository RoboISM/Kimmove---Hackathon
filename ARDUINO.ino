void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(7, INPUT);
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);

  pinMode(13,  OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(13, HIGH);
  digitalWrite(9, HIGH);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);

  if(digitalRead(7) && digitalRead(6)) Serial.println("CLOSE");
  else if(digitalRead(7)) Serial.println("TOGGLE");
  else if(digitalRead(4)) Serial.println("RELOAD");
  else if(digitalRead(6) && digitalRead(5)) Serial.println("LR");
  else if(digitalRead(6)) Serial.println("LEFT");
  else if(digitalRead(5)) Serial.println("RIGHT");
  else Serial.println("NONE");
  delay(125);
}
