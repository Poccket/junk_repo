import re

reference = {
	"ones":
		["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
	"tens":
		["zero", "ten", "twenty", "thirty", "fourty", "fifty", "sixty", "seventy", "eighty", "ninety"],
	"teens":
		["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"],
	"names":
		["thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonillion", "decillion"]
	}

def processNum(inp: int) -> str:
	output = ""
	inp = re.sub(r"\D", "", inp)
	if inp == "0": return "zero"
	input = [int(x) for x in str(inp)]

	while len(input) > 0:
		if input[0] != 0:
			if len(input) % 3 == 0:
				output += reference["ones"][int(input[0])] + " hundred "
				if int(input[1]) or int(input[2]):
					output += "and "
			elif len(input) % 3 == 2:
				if input[0] == 1:
					output += reference["teens"][int(input[1])] + " "
					input = input[1:]
				else:
					output += reference["tens"][int(input[0])] + " "
			elif len(input) % 3 == 1:
				output += reference["ones"][int(input[0])] + " "
		if len(input) % 3 == 1 and len(input) > 3:
			output += reference["names"][(len(input) // 3)-1] + " "
			if any(input):
				output += "and "

		input = input[1:]

	if output:
		return output
	else:
		return "Bad Input."

while 1:
	print(processNum(input("num: ")))