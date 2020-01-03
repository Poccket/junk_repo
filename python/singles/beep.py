import pyaudio
import numpy as np
import re
import time

def is_morse(txt):
    match = re.match("^[-\/\. ]*$", txt)
    return match is not None

p = pyaudio.PyAudio()

# the length of a dot is one unit
# the length of a dash is three units
# the space within sequences is one unit (we use a silenced dot here)
# the space between sequences is three units (we use a silenced dash here)
# the space between words is seven units
# unit length is defined in seconds
unit_len = 0.5
volume = 0.5
sample_r = 44100
sine_f = 440.0
do_convert = True

dash = None
dot = None
space = None

def gen_samples(fs, f, length):
    global dash
    global dot
    global space
    dash = (np.sin(2*np.pi*np.arange(fs*(length*3))*f/fs)).astype(np.float32)
    dot = (np.sin(2*np.pi*np.arange(fs*length)*f/fs)).astype(np.float32)
    space = (np.sin(2*np.pi*np.arange(fs*(length*7))*f/fs)).astype(np.float32)
gen_samples(sample_r, sine_f, unit_len)

# dot = -, dash = .
morse_table = {"a": ".-"    ,    "b": "-..."  ,    "c": "-.-."  ,    "d": "-.."   ,    "e": "."     ,
               "f": "..-."  ,    "g": "--."   ,    "h": "...."  ,    "i": ".."    ,    "j": ".---"  ,
               "k": "-.-"   ,    "l": ".-.."  ,    "m": "--"    ,    "n": "-."    ,    "o": "---"   ,
               "p": ".--."  ,    "q": "--.-"  ,    "r": ".-."   ,    "s": "..."   ,    "t": "-"     ,    # sorry for breaking formatting here
               "u": "..-"   ,    "v": "...-"  ,    "w": ".--"   ,    "x": "-..-"  ,    "y": "-.--"  ,    "z": "--.." ,

               "0": "-----" ,    "1": ".----" ,    "2": "..---" ,    "3": "...--" ,    "4": "....-" ,
               "5": "....." ,    "6": "-...." ,    "7": "--..." ,    "8": "---.." ,    "9": "----." ,

               ".": ".-.-.-",    ",": "--..--",    "?": "..--..",    "'": ".----.",    "/": "-..-." ,
               "&": ".-..." ,    ":": "---...",    "=": "-...-" ,    "\"":".-..-.",    "@": "...-.-"}

prosigns = {
    ".-.-."    :  "END OF MESSAGE",               # AR
    ".-..."    :  "STAND BY",                     # AS
    "-...-.-"  :  "RECEIVER WELCOME TO TRANSMIT", # BK
    "-...-"    :  "PAUSE.",                       # BT
    "-.-.-"    :  "BEGIN.",                       # KA
    "-.--."    :  "END.",                         # KN
    "-.-..-.." :  "GOING OFF THE AIR",            # CL
    "-.-.--.-" :  "CALLING ANYONE",               # CQ
    "-.--."    :  "GO ONLY",                      # KN
    "...-.-"   :  "FINAL MESSAGE",                # SK
    "...-."    :  "UNDERSTOOD",                   # VE
}

abbr = {
    "AA"       :  "ALL AFTER",
    "AB"       :  "ALL BEFORE",
    "ABT"      :  "ABOUT",
    "ADEE"     :  "ADRESSEE",
    "ADR"      :  "ADDRESS",
    "AGN"      :  "AGAIN",
#   "AM"       :  "AMPLITUDE MODULATION",   Real word, don't wanna do this tbh.
    "ANT"      :  "ANTENNA",              # This is different, I swear!
    "BCI"      :  "BROADCAST INTERFERENCE",
    "BCL"      :  "BROADCAST LISTENER",
    "BCNU"     :  "BE SEEING YOU",
    "BK"       :  "BREAK",
    "BN"       :  "BETWEEN",
    "BT"       :  " -- ",
    "BTR"      :  "BETTER",
    "B4"       :  "BEFORE",
#   "C"        :  "YES", # :/
    "CFM"      :  "CONFIRM",
    "CK"       :  "CHECK",
    "CKT"      :  "CIRCUIT",
    "CL"       :  "CLOSING STATION",
    "CLBK"     :  "CALLBOOK",
    "CLD"      :  "CALLED",
    "CLG"      :  "CALLING",
    "CNT"      :  "CAN'T",
    "CONDX"    :  "CONDITIONS",
    "CQ"       :  "CALLING ANYONE",
    "CQD"      :  "CALLING ANYONE, IN DISTRESS",
    "CU"       :  "SEE YOU",
    "CUL"      :  "SEE YOU LATER",
    "CUM"      :  "COME",
    "CW"       :  "CONTINUOUS WAVE",
    "DA"       :  "DAY",
    "DE"       :  "FROM",
    "DIFF"     :  "DIFFERENCE",
    "DLVD"     :  "DELIVERED",
    "DN"       :  "DOWN",
    "DR"       :  "DEAR",
    "DX"       :  "DISTANCE",
    "EL"       :  "ELEMENT",
    "ES"       :  "DISTANCE",
    "FER"      :  "FOR",
    "FM"       :  "FROM",
    "GA"       :  "GOOD AFTERNOON",
    "GB"       :  "GOOD BYE",
    "GD"       :  "GOOD",
    "GE"       :  "GOOD EVENING",
    "GESS"     :  "GUESS",
    "GG"       :  "GOING",
    "GM"       :  "GOOD MORNING",
    "GN"       :  "GOOD NIGHT",
    "GND"      :  "GROUND",
    "GUD"      :  "GOOD",
    "GV"       :  "GIVE",
    "GVG"      :  "GIVING",
    "HH"       :  "ERROR IN SENDING",
#   "HI"       :  "HIGH"  wasnt sure bout this
    "HPE"      :  "HOPE",
    "HQ"       :  "HEADQUARTERS",
    "HR"       :  "HERE",
    "HV"       :  "HAVE",
    "HW"       :  "HOW COPY",
    "IMI"      :  "SAY AGAIN",
    "LID"      :  "POOR OPERATOR",
    "LNG"      :  "LONG",
    "LTR"      :  "LATER",
    "LV"       :  "LEAVE",
    "LVG"      :  "LEAVING",
    "MA"       :  "MILLAMPERES",
    "MILL"     :  "TYPEWRITER",
    "MILS"     :  "MILLAMPERES",
    "MSG"      :  "MESSAGE",
    "NCS"      :  "NET CONTROL STATION",
    "ND"       :  "NOTHING DOING",
    "NIL"      :  "NOTHING",
    "NM"       :  "NO MORE",
    "NR"       :  "NUMBER",
    "NW"       :  "NOW",
    "OB"       :  "OLD BOY",
    "OC"       :  "OLD CHAP",
    "OM"       :  "OLD MAN",
    "OP"       :  "OPERATOR",
    "OPR"      :  "OPERATOR",
    "OT"       :  "OLD TIMER",
    "PBL"      :  "PREAMBLE",
    "PKG"      :  "PACKAGE",
    "PSE"      :  "PLEASE",
    "PT"       :  "POINT",
    "PWR"      :  "POWER",
    "PX"       :  "PRESS",
    "RC"       :  "RAGCHEW",
    "RCD"      :  "RECEIVED",
    "RCVR"     :  "RECEIVER",
    "RE"       :  "REGARDING",
    "REF"      :  "REFER TO",
    "RFI"      :  "RADIO FREQUENCY INTERFERENCE",
    "RIG"      :  "STATION EQUIPMENT",
    "RPT"      :  "REPEAT",
    "RTTY"     :  "RADIO TELETYPE",
    "RST"      :  "READABILITY, STRENGTH, TONE",
    "RX"       :  "RECEIVER",
    "SASE"     :  "SALF-ADDRESSED, STAMPED ENVELOPE",
    "SED"      :  "SAID",
    "SEZ"      :  "SAYS",
    "SGD"      :  "SIGNED",
    "SIG"      :  "SIGNAL",
    "SINE"     :  "SIGNED",
    "SKED"     :  "SCHEDULE",
    "SRI"      :  "SORRY",
    "SS"       :  "SWEEPSTAKES",
    "SSB"      :  "SINGLE SIDE BAND",
    "STN"      :  "STATION",
    "SUM"      :  "SOME",
    "SVC"      :  "SERVICE",
    "TFC"      :  "TRAFFIC",
    "TMW"      :  "TOMORROW",
    "TKS"      :  "THANKS",
    "TNX"      :  "THANKS",
    "TR"       :  "TRANSMIT",
    "TRIX"     :  "TRICKS",
    "TT"       :  "THAT",
    "TTS"      :  "THAT IS",
    "TU"       :  "THANK YOU",
    "TVI"      :  "TELEVISION INTERFERENCE",
    "TX"       :  "TRANSMIT",
    "TXT"      :  "TEXT",
    "VFB"      :  "VERY FINE BUSINESS",
    "VFO"      :  "VARIABLE FREQUENCY OSCILLATOR",
    "VY"       :  "VERY",
    "WA"       :  "WORD AFTER",
    "WB"       :  "WORD BEFORE",
    "WD"       :  "WORD",
    "WDS"      :  "WORDS",
    "WID"      :  "WITH",
    "WKD"      :  "WORKED",
    "WKG"      :  "WORKING",
    "WL"       :  "WELL",
    "WPM"      :  "WORDS PER MINUTE",
    "WRD"      :  "WORD",
    "WUD"      :  "WOULD",
    "WX"       :  "WEATHER",
    "XCVR"     :  "TRANSCEIVER",
    "XMTR"     :  "TRANSMITTER",
    "XTAL"     :  "CRYSTAL",
    "XYL"      :  "WIFE",
    "YL"       :  "YOUNG LADY",
    "YR"       :  "YEAR",
    "30"       :  "NO MORE TO SEND.",
    "73"       :  "BEST REGARDS",
    "88"       :  "LOVE AND KISSES",
    "161"      :  "BEST REGARDS, LOVE AND KISSES"
 }

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sample_r,
                output=True)
paris = "PARIS"

demo = ["-.. . / ... - -. / .---- / --. .- / .-.-.- / -.-. --.- / - --- / - .-. / .-.-.-",
        "... - -. / .---- / -.. . / ... - -. / ...-- / .-.-.- / .... .-- / ..--.. / -.--. / ... - -. / .----",
        "-.. . / ... - -. / .---- / .-.-.- / --. -.. / .-.-.- / - . ... - -. --. / -... ..- --. / .-.-.- / .... --- .-- / .-. / ..- / --- -- / ..--..",
        "--. -.. / .-.-.- / .-. .--. - / -... -. / .-..-. - . ... - -. --. .-..-. / .- -. -.. / .-..-. .... --- .-- .-..-. / .-.-.- / ... .-. .. / --- --",
        "-.. . / ... - -. / .---- / .-.-.- / -... ..- --. / .-.-.- / ... . -- .. / .- ..- - --- / -.- . -.-- / .-.-.- / ...- . .-. -.-- / --. -.. / .-.-.-",
        "-.. . / ... - -. / ...-- / .-.-.- / .. / -.-. / .-.-.- / -- ..- ... - / --. --- / .-.-.- / --. -... / ...-- -----",
        "-.. . / ... - -. / .---- / .-.-.- / --... ...-- / --- --",]

def do_demo():
    stn = [[440.0, 0.5], [380.0, 0.3]]
    curr_stn = 0
    for inp in demo:
        sine_f, unit_len = stn[curr_stn]
        gen_samples(sample_r, sine_f, unit_len)
        stream.start_stream()
        morse_dec = ""
        morse_word = ""
        if not is_morse(inp):
            for char in inp.lower():
                if char in morse_table.keys():
                    for item in morse_table[char]:
                        if item == "-":
                            stream.write(volume*dash)
                        else:
                            stream.write(volume*dot)
                        stream.write(0*dot)
                    print(morse_table[char], end=' ', flush=True)
                    stream.write(0*dash)
                elif char == " ":
                    print("/ ", end='', flush=True)
                    stream.write(0*space)
        else:
            for char in inp.lower():
                if char == " ":
                    if morse_dec:
                        if morse_dec == "SKIP":
                            morse_dec = ""
                            continue
                        if morse_dec[:4] == "SKIP":
                            morse_dec = morse_dec[4:]
                        try:
                            if morse_dec in prosigns.keys():
                                morse_word += prosigns[morse_dec]
                            else:
                                morse_word += list(morse_table.keys())[list(morse_table.values()).index(morse_dec)].upper()
                            morse_dec = ""
                        except ValueError:
                            print("Bad input. Found invalid morse character:", morse_dec, "\nDid you forget spaces?")
                            morse_dec = ""
                            continue
                        stream.write(0*dash)
                elif char == "-":
                    stream.write(volume*dash)
                    stream.write(0*dot)
                    morse_dec += "-"
                elif char == ".":
                    stream.write(volume*dot)
                    stream.write(0*dot)
                    morse_dec += "."
                elif char == "/":
                    if morse_dec:
                        try:
                            if morse_dec in prosigns.keys():
                                morse_word += prosigns[morse_dec]
                            else:
                                morse_word += list(morse_table.keys())[list(morse_table.values()).index(morse_dec)].upper()
                        except ValueError:
                            print("Bad input. Found invalid morse character:", morse_dec, "\nDid you forget spaces?")
                            break
                    if morse_word:
                        if morse_word in abbr.keys() and do_convert:
                            print(abbr[morse_word], end=' ', flush=True)
                        else:
                            print(morse_word, end=' ', flush=True)
                        morse_word = ""
                        morse_dec = "SKIP"
                    else:
                        print(" ", end='', flush=True)
                    stream.write(0*space)
            if morse_dec:
                try:
                    if morse_dec in prosigns.keys():
                        morse_word += prosigns[morse_dec]
                    else:
                        morse_word += list(morse_table.keys())[list(morse_table.values()).index(morse_dec)].upper()
                except ValueError:
                    print("Bad input. Found invalid morse character:", morse_dec, "\nDid you forget spaces?")
                    break
            if morse_word:
                if morse_word in abbr.keys() and do_convert:
                    print(abbr[morse_word], end=' ', flush=True)
                else:
                    print(morse_word, end=' ', flush=True)
        print("")
        stream.stop_stream()
        time.sleep(4)
        curr_stn = not curr_stn

print("Type anything to output it in morse code.")
print("Put '/' in front of your input to run a command.")
while True:
    inp = input(">")
    if not inp:
        continue
    if inp[0] == "/":
        if inp[1:5] == "help":
            print("  Type anything to output it in morse code.")
            print("  Commands:")
            print("    help - prints this message")
            print("    demo - prints demo")
            print("    sine - change sine frequency (current:", sine_f, ")")
            print("    volu - change volume (current:", volume, ")")
            print("         - a value between 0 and 100 is accepted")
            print("    unit - change unit length (current:", unit_len, ")")
            print("         - if no number is provided, prints unit per character")
            print("    conv - switch whether to convert abbr to words (current:", do_convert, ")")
            print("    quit - quits the program")
        elif inp[1:5] == "demo":
            do_demo()
        elif inp[1:5] == "unit":
            if inp == "/unit":
                print("The length of a dot is one unit\n\
                       The length of a dash is three units\n\
                       The space within sequences is one unit\n\
                       The space between sequences is three units\n\
                       The space between words is seven units")
                continue
            try:
                unit_len = float(inp[5:])
                gen_samples(sample_r, sine_f, unit_len)
            except ValueError:
                print("Bad input. Try it like '/unit 1.0'")
        elif inp[1:5] == "sine":
            try:
                sine_f = float(inp[5:])
                gen_samples(sample_r, sine_f, unit_len)
            except ValueError:
                print("Bad input. Try it like '/sine 440.0'")
        elif inp[1:5] == "volu":
            try:
                temp_v = int(inp[5:])
                if temp_v >= 0 and temp_v <= 100:
                    volume = temp_v / 100
            except ValueError:
                print("Bad input. Try it like '/volu 50'")
        elif inp[1:5] == "conv":
            do_convert = not do_convert
        elif inp[1:5] == "quit":
            print("Goodbye!")
            break
        else:
            print("Run 'help' to see all available commands.")
        continue
    stream.start_stream()
    morse_dec = ""
    morse_word = ""
    if not is_morse(inp):
        for char in inp.lower():
            if char in morse_table.keys():
                for item in morse_table[char]:
                    if item == "-":
                        stream.write(volume*dash)
                    else:
                        stream.write(volume*dot)
                    stream.write(0*dot)
                print(morse_table[char], end=' ', flush=True)
                stream.write(0*dash)
            elif char == " ":
                print("/ ", end='', flush=True)
                stream.write(0*space)
    else:
        for char in inp.lower():
            if char == " ":
                if morse_dec:
                    if morse_dec == "SKIP":
                        morse_dec = ""
                        continue
                    if morse_dec[:4] == "SKIP":
                        morse_dec = morse_dec[4:]
                    try:
                        if morse_dec in prosigns.keys():
                            morse_word += prosigns[morse_dec]
                        else:
                            morse_word += list(morse_table.keys())[list(morse_table.values()).index(morse_dec)].upper()
                        morse_dec = ""
                    except ValueError:
                        print("Bad input. Found invalid morse character:", morse_dec, "\nDid you forget spaces?")
                        morse_dec = ""
                        continue
                    stream.write(0*dash)
            elif char == "-":
                stream.write(volume*dash)
                stream.write(0*dot)
                morse_dec += "-"
            elif char == ".":
                stream.write(volume*dot)
                stream.write(0*dot)
                morse_dec += "."
            elif char == "/":
                if morse_dec:
                    try:
                        if morse_dec in prosigns.keys():
                            morse_word += prosigns[morse_dec]
                        else:
                            morse_word += list(morse_table.keys())[list(morse_table.values()).index(morse_dec)].upper()
                    except ValueError:
                        print("Bad input. Found invalid morse character:", morse_dec, "\nDid you forget spaces?")
                        break
                if morse_word:
                    if morse_word in abbr.keys() and do_convert:
                        print(abbr[morse_word], end=' ', flush=True)
                    else:
                        print(morse_word, end=' ', flush=True)
                    morse_word = ""
                    morse_dec = "SKIP"
                else:
                    print(" ", end='', flush=True)
                stream.write(0*space)
        if morse_dec:
            try:
                if morse_dec in prosigns.keys():
                    morse_word += prosigns[morse_dec]
                else:
                    morse_word += list(morse_table.keys())[list(morse_table.values()).index(morse_dec)].upper()
            except ValueError:
                print("Bad input. Found invalid morse character:", morse_dec, "\nDid you forget spaces?")
                break
        if morse_word:
            if morse_word in abbr.keys() and do_convert:
                print(abbr[morse_word], end=' ', flush=True)
            else:
                print(morse_word, end=' ', flush=True)
    print("")
    stream.stop_stream()

stream.close()

p.terminate()