/* Small5ptFont Version 09.

  Created by OlivierFlying747-8
  https://fredrik.hubbe.net/lightsaber/proffieos.html
  Copyright (c) 2016-2026 Fredrik Hubinette
  Copyright (c) 2026 OlivierFlying747-8
  With contributions by:
  Fredrik Hubinette aka profezzorn,
  In case of problems, you can find us at: https://crucible.hubbe.net where somebody will be there to help.
  Distributed under the terms of the GNU General Public License v3.
  https://www.gnu.org/licenses/

Smallest possible but still readable text font for OLED, each character is maximum 5 pixels tall x 5 (6) pixels wide,
but the majority of digits and alphabet characters are 5 tall x 3 wide.

The idea is to have a text font with a minimalist flash-memory footprint for a text based menu system.

Characters supported:
- Digits from 0 to 9.
- Latin alphabet from A to Z and a to z.
- Punctuation & special characters.
  '@' & '$' should not used, because they are taller than 5 pixels!

Longest Bit Count Type Required (number of columns without 0b or UL)
 1–8  uint8_t
 9–16 uint16_t
17–32 uint32_t
*/

const uint8_t Small5pt7bChar0[] = {   // 0x20 ' ' (Space)
  0b0UL
};
const uint8_t Small5pt7bChar1[] = {   // 0x21 '!' (ExclamationMark)
  0b10111UL
};
const uint8_t Small5pt7bChar2[] = {   // 0x22 '"' (DoubleQuote)
  0b11UL,
  0b00UL,
  0b11UL
};
const uint8_t Small5pt7bChar3[] = {   // 0x23 '#' (Hashtag)
  0b01010UL,
  0b11111UL,
  0b01010UL,
  0b11111UL,
  0b01010UL
};
const uint8_t Small5pt7bChar4[] = {   // 0x24 '$' (Dollar) (7 tall!)
  0b0100100UL,
  0b0101010UL,
  0b1111111UL,
  0b0101010UL,
  0b0010010UL
};
const uint8_t Small5pt7bChar5[] = {   // 0x25 '%' (Percent)
  0b10001UL,
  0b01000UL,
  0b00100UL,
  0b00010UL,
  0b10001UL
};
const uint8_t Small5pt7bChar6[] = {   // 0x26 '&' (Ampersand)
  0b01010UL,
  0b10101UL,
  0b01101UL,
  0b10010UL,
  0b01000UL
};
const uint8_t Small5pt7bChar7[] = {   // 0x27 ''' (Quote)
  0b11UL
};
const uint8_t Small5pt7bChar8[] = {   // 0x28 '(' (OpenParenthesis)
  0b01110UL,
  0b10001UL
};
const uint8_t Small5pt7bChar9[] = {   // 0x29 ')' (CloseParenthesis)
  0b10001UL,
  0b01110UL,
};
const uint8_t Small5pt7bChar10[] = {   // 0x2A '*' (Multiply) (using symbol 0x78 'x' instead)
  0b101UL,
  0b010UL,
  0b101UL
};
const uint8_t Small5pt7bChar11[] = {   // 0x2B '+' (Plus)
  0b010UL,
  0b111UL,
  0b010UL
};
const uint8_t Small5pt7bChar12[] = {   // 0x2C ',' (Comma)
  0b100UL,
  0b011UL
};
const uint8_t Small5pt7bChar13[] = {   // 0x2D '-' (Minus)
  0b1UL,
  0b1UL,
  0b1UL
};
const uint8_t Small5pt7bChar14[] = {   // 0x2E '.' (Period)
  0b11UL,
};
const uint8_t Small5pt7bChar15[] = {   // 0x2F '/' (Slash or Divide)
  0b11000UL,
  0b00100UL,
  0b00011UL
};
const uint8_t Small5pt7bChar16[] = {   // 0x30 '0' (Zero)
  0b01110UL,
  0b10001UL,
  0b01110UL
};
const uint8_t Small5pt7bChar17[] = {   // 0x31 '1'
  0b10010UL,
  0b11111UL,
  0b10000UL
};
const uint8_t Small5pt7bChar18[] = {   // 0x32 '2'
  0b10010UL,
  0b11001UL,
  0b10110UL
};
const uint8_t Small5pt7bChar19[] = {   // 0x33 '3'
  0b10001UL,
  0b10101UL,
  0b01010UL
};
const uint8_t Small5pt7bChar20[] = {   // 0x34 '4'
  0b00111UL,
  0b00100UL,
  0b11111UL
};
const uint8_t Small5pt7bChar21[] = {   // 0x35 '5'
  0b10111UL,
  0b10101UL,
  0b01001UL
};
const uint8_t Small5pt7bChar22[] = {   // 0x36 '6'
  0b11110UL,
  0b10101UL,
  0b11101UL
};
const uint8_t Small5pt7bChar23[] = {   // 0x37 '7'
  0b11001UL,
  0b00101UL,
  0b00011UL
};
const uint8_t Small5pt7bChar24[] = {   // 0x38 '8'
  0b11111UL,
  0b10101UL,
  0b11111UL
};
const uint8_t Small5pt7bChar25[] = {   // 0x39 '9'
  0b10111UL,
  0b10101UL,
  0b01111UL
};
const uint8_t Small5pt7bChar26[] = {   // 0x3A ':' (Colon)
  0b101UL
};
const uint8_t Small5pt7bChar27[] = {   // 0x3B ';' (SemiColon)
  0b1000UL,
  0b0101UL
};
const uint8_t Small5pt7bChar28[] = {   // 0x3C '<' (Left)
  0b00100UL,
  0b01010UL,
  0b10001UL
};
const uint8_t Small5pt7bChar29[] = {   // 0x3D '=' (Equal)
  0b101UL,
  0b101UL,
  0b101UL
};
const uint8_t Small5pt7bChar30[] = {   // 0x3E '>' (Right)
  0b10001UL,
  0b01010UL,
  0b00100UL
};
const uint8_t Small5pt7bChar31[] = {   // 0x3F '?' (QuestionMark)
  0b00010UL,
  0b00001UL,
  0b10101UL,
  0b00010UL
};
const uint8_t Small5pt7bChar32[] = {   // 0x40 '@' (At) (6 tall!)
  0b011110UL,
  0b100001UL,
  0b101101UL,
  0b101001UL,
  0b101110UL
};
const uint8_t Small5pt7bChar33[] = {   // 0x41 'A'
  0b11110UL,
  0b00101UL,
  0b11110UL
};
const uint8_t Small5pt7bChar34[] = {   // 0x42 'B'
  0b11111UL,
  0b10101UL,
  0b10101UL,
  0b01010UL
};
const uint8_t Small5pt7bChar35[] = {   // 0x43 'C'
  0b01110UL,
  0b10001UL,
  0b10001UL
};
const uint8_t Small5pt7bChar36[] = {   // 0x44 'D'
  0b11111UL,
  0b10001UL,
  0b10001UL,
  0b01110UL
};
const uint8_t Small5pt7bChar37[] = {   // 0x45 'E'
  0b11111UL,
  0b10101UL,
  0b10001UL
};
const uint8_t Small5pt7bChar38[] = {   // 0x46 'F'
  0b11111UL,
  0b00101UL,
  0b00001UL
};
const uint8_t Small5pt7bChar39[] = {   // 0x47 'G'
  0b01110UL,
  0b10001UL,
  0b10101UL,
  0b01101UL
};
const uint8_t Small5pt7bChar40[] = {   // 0x48 'H'
  0b11111UL,
  0b00100UL,
  0b11111UL
};
const uint8_t Small5pt7bChar41[] = {   // 0x49 'I'
  0b10001UL,
  0b11111UL,
  0b10001UL
};
const uint8_t Small5pt7bChar42[] = {   // 0x4A 'J'
  0b01000UL,
  0b10001UL,
  0b01111UL,
  0b00001UL
};
const uint8_t Small5pt7bChar43[] = {   // 0x4B 'K'
  0b11111UL,
  0b00100UL,
  0b01010UL,
  0b10001UL
};
const uint8_t Small5pt7bChar44[] = {   // 0x4C 'L'
  0b11111UL,
  0b10000UL,
  0b10000UL
};
const uint8_t Small5pt7bChar45[] = {   // 0x4D 'M'
  0b11111UL,
  0b00010UL,
  0b00100UL,
  0b00010UL,
  0b11111UL
};
const uint8_t Small5pt7bChar46[] = {   // 0x4E 'N'
  0b11111UL,
  0b00010UL,
  0b00100UL,
  0b11111UL
};
const uint8_t Small5pt7bChar47[] = {   // 0x4F 'O'
  0b01110UL,
  0b10001UL,
  0b10001UL,
  0b01110UL
};
const uint8_t Small5pt7bChar48[] = {   // 0x50 'P'
  0b11111UL,
  0b00101UL,
  0b00010UL
};
const uint8_t Small5pt7bChar49[] = {   // 0x51 'Q'
  0b01110UL,
  0b10001UL,
  0b10101UL,
  0b01110UL,
  0b10000UL
};
const uint8_t Small5pt7bChar50[] = {   // 0x52 'R'
  0b11111UL,
  0b00101UL,
  0b01101UL,
  0b10010UL
};
const uint8_t Small5pt7bChar51[] = {   // 0x53 'S'
  0b10010UL,
  0b10101UL,
  0b01001UL
};
const uint8_t Small5pt7bChar52[] = {   // 0x54 'T'
  0b00001UL,
  0b11111UL,
  0b00001UL
};
const uint8_t Small5pt7bChar53[] = {   // 0x55 'U'
  0b01111UL,
  0b10000UL,
  0b10000UL,
  0b01111UL
};
const uint8_t Small5pt7bChar54[] = {   // 0x56 'V'
  0b00111UL,
  0b01000UL,
  0b10000UL,
  0b01000UL,
  0b00111UL
};
const uint8_t Small5pt7bChar55[] = {   // 0x57 'W'
  0b01111UL,
  0b10000UL,
  0b01100UL,
  0b10000UL,
  0b01111UL
};
const uint8_t Small5pt7bChar56[] = {   // 0x58 'X'
  0b11011UL,
  0b00100UL,
  0b11011UL
};
const uint8_t Small5pt7bChar57[] = {   // 0x59 'Y'
  0b00011UL,
  0b11100UL,
  0b00011UL
};
const uint8_t Small5pt7bChar58[] = {   // 0x5A 'Z'
  0b11001UL,
  0b10101UL,
  0b10011UL
};
const uint8_t Small5pt7bChar59[] = {   // 0x5B '[' (OpenBracket)
  0b11111UL,
  0b10001UL
};
const uint8_t Small5pt7bChar60[] = {   // 0x5C '\' (BackSlash)
  0b00011UL,
  0b00100UL,
  0b11000UL
};
const uint8_t Small5pt7bChar61[] = {   // 0x5D ']' (CloseBracket)
  0b10001UL,
  0b11111UL
};
const uint8_t Small5pt7bChar62[] = {   // 0x5E '^' (Up) (up pointing arrow)
  0b100UL,
  0b010UL,
  0b001UL,
  0b010UL,
  0b100UL
};
const uint8_t Small5pt7bChar63[] = {   // 0x5F '_' (Underscore)
  0b1UL,
  0b1UL,
  0b1UL,
  0b1UL
};
const uint8_t Small5pt7bChar64[] = {   // 0x60 '`' (BackTick)
  0b01UL,
  0b10UL,
};

const uint8_t Small5pt7bChar65[] = {   // 0x61 'a'
  0b11110UL,
  0b00101UL,
  0b11110UL
};
const uint8_t Small5pt7bChar66[] = {   // 0x62 'b'
  0b11111UL,
  0b10101UL,
  0b10101UL,
  0b01010UL
};
const uint8_t Small5pt7bChar67[] = {   // 0x63 'c'
  0b01110UL,
  0b10001UL,
  0b10001UL
};
const uint8_t Small5pt7bChar68[] = {   // 0x64 'd'
  0b11111UL,
  0b10001UL,
  0b10001UL,
  0b01110UL
};
const uint8_t Small5pt7bChar69[] = {   // 0x65 'e'
  0b11111UL,
  0b10101UL,
  0b10001UL
};
const uint8_t Small5pt7bChar70[] = {   // 0x66 'f'
  0b11111UL,
  0b00101UL,
  0b00001UL
};
const uint8_t Small5pt7bChar71[] = {   // 0x67 'g'
  0b01110UL,
  0b10001UL,
  0b10101UL,
  0b01101UL
};
const uint8_t Small5pt7bChar72[] = {   // 0x68 'h'
  0b11111UL,
  0b00100UL,
  0b11111UL
};
const uint8_t Small5pt7bChar73[] = {   // 0x69 'i'
  0b10001UL,
  0b11111UL,
  0b10001UL
};
const uint8_t Small5pt7bChar74[] = {   // 0x6A 'j'
  0b01000UL,
  0b10001UL,
  0b01111UL,
  0b00001UL
};
const uint8_t Small5pt7bChar75[] = {   // 0x6B 'k'
  0b11111UL,
  0b00100UL,
  0b01010UL,
  0b10001UL
};
const uint8_t Small5pt7bChar76[] = {   // 0x6C 'l'
  0b11111UL,
  0b10000UL,
  0b10000UL
};
const uint8_t Small5pt7bChar77[] = {   // 0x6D 'm'
  0b11111UL,
  0b00010UL,
  0b00100UL,
  0b00010UL,
  0b11111UL
};
const uint8_t Small5pt7bChar78[] = {   // 0x6E 'n'
  0b11111UL,
  0b00010UL,
  0b00100UL,
  0b11111UL
};
const uint8_t Small5pt7bChar79[] = {   // 0x6F 'o'
  0b01110UL,
  0b10001UL,
  0b10001UL,
  0b01110UL
};
const uint8_t Small5pt7bChar80[] = {   // 0x70 'p'
  0b11111UL,
  0b00101UL,
  0b00010UL
};
const uint8_t Small5pt7bChar81[] = {   // 0x71 'q'
  0b01110UL,
  0b10001UL,
  0b10101UL,
  0b01110UL,
  0b10000UL
};
const uint8_t Small5pt7bChar82[] = {   // 0x72 'r'
  0b11111UL,
  0b00101UL,
  0b01101UL,
  0b10010UL
};
const uint8_t Small5pt7bChar83[] = {   // 0x73 's'
  0b10010UL,
  0b10101UL,
  0b01001UL
};
const uint8_t Small5pt7bChar84[] = {   // 0x74 't'
  0b00001UL,
  0b11111UL,
  0b00001UL
};
const uint8_t Small5pt7bChar85[] = {   // 0x75 'u'
  0b01111UL,
  0b10000UL,
  0b10000UL,
  0b01111UL
};
/*
const uint8_t Small5pt7bChar86[] = {   // 0x76 'v' (regular "v")
  0b00111UL,
  0b01000UL,
  0b10000UL,
  0b01000UL,
  0b00111UL
};
*/
const uint8_t Small5pt7bChar86[] = {   // 0x76 'v' (Down) ("fat" lower case 'v' for down pointing arrow)
  0b001UL,
  0b010UL,
  0b100UL,
  0b010UL,
  0b001UL
};
const uint8_t Small5pt7bChar87[] = {   // 0x77 'w'
  0b01111UL,
  0b10000UL,
  0b01100UL,
  0b10000UL,
  0b01111UL
};
const uint8_t Small5pt7bChar88[] = {   // 0x78 'x'
  0b11011UL,
  0b00100UL,
  0b11011UL
};
const uint8_t Small5pt7bChar89[] = {   // 0x79 'y'
  0b00011UL,
  0b11100UL,
  0b00011UL
};
const uint8_t Small5pt7bChar90[] = {   // 0x7A 'z'
  0b11001UL,
  0b10101UL,
  0b10011UL
};
const uint8_t Small5pt7bChar91[] = {   // 0x7B '{' (LeftBrace)
  0b00100UL,
  0b11011UL,
  0b10001UL
};
const uint8_t Small5pt7bChar92[] = {   // 0x7C '|' (Pipe)
  0b11111UL
};
const uint8_t Small5pt7bChar93[] = {   // 0x7D '}' (RightBrace)
  0b10001UL,
  0b11011UL,
  0b00100UL
};
const uint8_t Small5pt7bChar94[] = {   // 0x7E '~' (Tilde)
  0b10UL,
  0b01UL,
  0b10UL,
  0b01UL
};

const Glyph Small5pt7bGlyphs[] = {
//{ width, hom many spaces after, "altitude", GLYPHDATA(...) }
//{ width, advance, y_offset, GLYPHDATA(...) }

  { 3, 1,-4, GLYPHDATA(Small5pt7bChar0) },   // 0x20 ' ' (Space)
  { 1, 1,-4, GLYPHDATA(Small5pt7bChar1) },   // 0x21 '!' (Exclamation)
  { 3, 1,-3, GLYPHDATA(Small5pt7bChar2) },   // 0x22 '"' (DoubleQuote)
  { 5, 1,-4, GLYPHDATA(Small5pt7bChar3) },   // 0x23 '#' (Hashtag)
  { 5, 1,-5, GLYPHDATA(Small5pt7bChar4) },   // 0x24 '$' (Dollar)
  { 5, 1,-4, GLYPHDATA(Small5pt7bChar5) },   // 0x25 '%' (Percent)
  { 5, 1,-4, GLYPHDATA(Small5pt7bChar6) },   // 0x26 '&' (Ampersand)
  { 1, 1,-1, GLYPHDATA(Small5pt7bChar7) },   // 0x27 ''' (Quote)
  { 2, 1,-4, GLYPHDATA(Small5pt7bChar8) },   // 0x28 '(' (OpenParenthesis)
  { 2, 1,-4, GLYPHDATA(Small5pt7bChar9) },   // 0x29 ')' (CloseParenthesis)
  { 3, 1,-3, GLYPHDATA(Small5pt7bChar10) },   // 0x2A '*' (Multiply) (but using symbol for 0x78 'x' instead)
  { 3, 1,-3, GLYPHDATA(Small5pt7bChar11) },   // 0x2B '+' (Plus)
  { 2, 1,-4, GLYPHDATA(Small5pt7bChar12) },   // 0x2C ',' (Comma)
  { 3, 1,-3, GLYPHDATA(Small5pt7bChar13) },   // 0x2D '-' (Minus)
  { 1, 1,-4, GLYPHDATA(Small5pt7bChar14) },   // 0x2E '.' (Period)
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar15) },   // 0x2F '/' (Slash or Divide)
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar16) },   // 0x30 '0'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar17) },   // 0x31 '1'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar18) },   // 0x32 '2'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar19) },   // 0x33 '3'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar20) },   // 0x34 '4'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar21) },   // 0x35 '5'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar22) },   // 0x36 '6'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar23) },   // 0x37 '7'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar24) },   // 0x38 '8'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar25) },   // 0x39 '9'
  { 3, 1,-3, GLYPHDATA(Small5pt7bChar26) },   // 0x3A ':' (Colon)
  { 2, 1,-4, GLYPHDATA(Small5pt7bChar27) },   // 0x3B ';' (SemiColon)
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar28) },   // 0x3C '<' (Left)
  { 3, 3,-3, GLYPHDATA(Small5pt7bChar29) },   // 0x3D '=' (Equal)
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar30) },   // 0x3E '>' (Right)
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar31) },   // 0x3F '?' (Question)
  { 6, 1,-4, GLYPHDATA(Small5pt7bChar32) },   // 0x40 '@' (At)
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar33) },   // 0x41 'A'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar34) },   // 0x42 'B'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar35) },   // 0x43 'C'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar36) },   // 0x44 'D'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar37) },   // 0x45 'E'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar38) },   // 0x46 'F'
  { 5, 4,-4, GLYPHDATA(Small5pt7bChar39) },   // 0x47 'G'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar40) },   // 0x48 'H'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar41) },   // 0x49 'I'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar42) },   // 0x4A 'J'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar43) },   // 0x4B 'K'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar44) },   // 0x4C 'L'
  { 5, 1,-4, GLYPHDATA(Small5pt7bChar45) },   // 0x4D 'M'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar46) },   // 0x4E 'N'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar47) },   // 0x4F 'O'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar48) },   // 0x50 'P'
  { 5, 1,-4, GLYPHDATA(Small5pt7bChar49) },   // 0x51 'Q'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar50) },   // 0x52 'R'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar51) },   // 0x53 'S'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar52) },   // 0x54 'T'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar53) },   // 0x55 'U'
  { 5, 1,-4, GLYPHDATA(Small5pt7bChar54) },   // 0x56 'V'
  { 5, 5,-4, GLYPHDATA(Small5pt7bChar55) },   // 0x57 'W'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar56) },   // 0x58 'X'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar57) },   // 0x59 'Y'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar58) },   // 0x5A 'Z'
  { 2, 1,-4, GLYPHDATA(Small5pt7bChar59) },   // 0x5B '[' (OpenBracket)
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar60) },   // 0x5C '\' (BackSlash)
  { 2, 1,-4, GLYPHDATA(Small5pt7bChar61) },   // 0x5D ']' (CloseBracket)
  { 3, 5,-2, GLYPHDATA(Small5pt7bChar62) },   // 0x5E '^' (Up pointing arrow)
  { 4,-1,-4, GLYPHDATA(Small5pt7bChar63) },   // 0x5F '_' (Underscore)
  { 2, 1,-1, GLYPHDATA(Small5pt7bChar64) },   // 0x60 '`' (BackTick)
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar65) },   // 0x61 'a'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar66) },   // 0x62 'b'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar67) },   // 0x63 'c'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar68) },   // 0x64 'd'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar69) },   // 0x65 'e'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar70) },   // 0x66 'f'
  { 5, 4,-4, GLYPHDATA(Small5pt7bChar71) },   // 0x67 'g'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar72) },   // 0x68 'h'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar73) },   // 0x69 'i'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar74) },   // 0x6A 'j'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar75) },   // 0x6B 'k'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar76) },   // 0x6C 'l'
  { 5, 1,-4, GLYPHDATA(Small5pt7bChar77) },   // 0x6D 'm'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar78) },   // 0x6E 'n'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar79) },   // 0x6F 'o'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar80) },   // 0x70 'p'
  { 5, 1,-4, GLYPHDATA(Small5pt7bChar81) },   // 0x71 'q'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar82) },   // 0x72 'r'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar83) },   // 0x73 's'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar84) },   // 0x74 't'
  { 4, 1,-4, GLYPHDATA(Small5pt7bChar85) },   // 0x75 'u'
  { 5, 1,-4, GLYPHDATA(Small5pt7bChar86) },   // 0x76 'v' ( or use the "fat" lower case 'v'" for down pointing arrow)
  { 5, 5,-4, GLYPHDATA(Small5pt7bChar87) },   // 0x77 'w'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar88) },   // 0x78 'x'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar89) },   // 0x79 'y'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar90) },   // 0x7A 'z'
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar91) },   // 0x7B '{' (LeftBrace)
  { 1, 1,-4, GLYPHDATA(Small5pt7bChar92) },   // 0x7C '|' (Pipe)
  { 3, 1,-4, GLYPHDATA(Small5pt7bChar93) },   // 0x7D '}' (RightBrace)
  { 4, 1,-3, GLYPHDATA(Small5pt7bChar94) },   // 0x7E '~' (Tilde)
};

