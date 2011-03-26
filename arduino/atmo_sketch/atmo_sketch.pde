/*****************************************************************************
 * This file is part of atmo-client
 *****************************************************************************
 * Copyright (C) 2011 vobject <vobject@gmail.com>
 *
 * atmo-client is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 *  atmo-client is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with atmo-client.  If not, see <http://www.gnu.org/licenses/>.
 ****************************************************************************/

#define CHANNEL_LEFT_R      7
#define CHANNEL_LEFT_G      8
#define CHANNEL_LEFT_B      9
#define CHANNEL_RIGHT_R    10
#define CHANNEL_RIGHT_G    11
#define CHANNEL_RIGHT_B    12
#define CHANNEL_TOP_R      13
#define CHANNEL_TOP_G      14
#define CHANNEL_TOP_B      15
#define CHANNEL_BOTTOM_R   16
#define CHANNEL_BOTTOM_G   17
#define CHANNEL_BOTTOM_B   18

const size_t redPin   = 11;
const size_t greenPin = 10;
const size_t bluePin  =  9;

const uint8_t ATMO_COMMAND_SIZE = 16;
int current_cmd[ATMO_COMMAND_SIZE] = { 0 };


int serialRead() {
  while (!Serial.available()) { }
  return Serial.read();
}


void setup()
{
  // atmo plugin sends at 38400 baud.
  Serial.begin(38400);
}

void loop()
{
  if (Serial.available()) {
    if (0xff == Serial.read() &&
        0x00 == serialRead()  &&
        0x00 == serialRead()) {
      for (uint8_t i = 0; i < ATMO_COMMAND_SIZE; ++i) {
        current_cmd[i] = serialRead();
      }

      analogWrite(redPin,   current_cmd[CHANNEL_LEFT_R]);
      analogWrite(greenPin, current_cmd[CHANNEL_LEFT_G]);
      analogWrite(bluePin,  current_cmd[CHANNEL_LEFT_B]);
    }
  }
  else {
    delay(5);
  }
}
