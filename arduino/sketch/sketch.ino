/*****************************************************************************
 * This file is part of atmo-client
 *****************************************************************************
 * Copyright (C) 2011-2012 vobject <vobject@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program. If not, see <http://www.gnu.org/licenses/>.
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

const unsigned int l_redPin   = 11;
const unsigned int l_greenPin = 10;
const unsigned int l_bluePin  =  9;

const unsigned int r_redPin   =  6;
const unsigned int r_greenPin =  5;
const unsigned int r_bluePin  =  3;

const uint8_t ATMO_COMMAND_SIZE = 16;
uint8_t current_cmd[ATMO_COMMAND_SIZE] = { 0 };

int serialRead()
{
   while (!Serial.available());
   return Serial.read();
}

void setup()
{
   pinMode(l_redPin, OUTPUT);
   pinMode(l_greenPin, OUTPUT);
   pinMode(l_bluePin, OUTPUT);

   pinMode(r_redPin, OUTPUT);
   pinMode(r_greenPin, OUTPUT);
   pinMode(r_bluePin, OUTPUT);

   // atmo plugin sends at 38400 baud.
   Serial.begin(38400);
}

void loop()
{
   if (Serial.available())
   {
      if (0xff == Serial.read() &&
          0x00 == serialRead()  &&
          0x00 == serialRead())
      {
         for (uint8_t i = 0; i < ATMO_COMMAND_SIZE; ++i)
         {
            current_cmd[i] = serialRead();
         }

         analogWrite(l_redPin,   current_cmd[CHANNEL_LEFT_R]);
         analogWrite(l_greenPin, current_cmd[CHANNEL_LEFT_G]);
         analogWrite(l_bluePin,  current_cmd[CHANNEL_LEFT_B]);

         analogWrite(r_redPin,   current_cmd[CHANNEL_RIGHT_R]);
         analogWrite(r_greenPin, current_cmd[CHANNEL_RIGHT_G]);
         analogWrite(r_bluePin,  current_cmd[CHANNEL_RIGHT_B]);
      }
   }
}
