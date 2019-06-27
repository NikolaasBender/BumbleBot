const int forPin = 9; // the pin that the LED is attached to
const int bacPin = 10;
const int lefPin = 11;
const int rigPin = 6;

void setup()
{
    // initialize the serial communication:
    Serial.begin(9600);
    // initialize the ledPin as an output:
    pinMode(forPin, OUTPUT);
    pinMode(bacPin, OUTPUT);
    pinMode(lefPin, OUTPUT);
    pinMode(rigPin, OUTPUT);
}

void loop()
{
    string brightness;

    // check if data has been sent from the computer:
    if (Serial.available())
    {
        // read the most recent byte (which will be from 0 to 255):
        brightness = Serial.readBytes(4, 4);
        // set the brightness of the LED:
        analogWrite(forPin, (byte)brightness[0]);
        analogWrite(bacPin, (byte)brightness[1]);
        analogWrite(lefPin, (byte)brightness[2]);
        analogWrite(rigPin, (byte)brightness[3]);
    }
}
