import csv

def main():
	option_type = "put"
	S0 = 100.00
	prices = []
	with open('PutCallData2JanLast.csv', 'rU') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			j=0
			stock = []
			for i, element in enumerate(row):
				if i == 0:
					stock.append(element)
				else:
					j += 1
					if element == "" or element == " ":
						break
					else:
						if j == 1:
							strike = float(element)
						if j == 2:
							combo = (strike, float(element))
							stock.append(combo)
							j = 0
			prices.append(stock)
	calls = []
	for i in range(len(prices)):
		if i%2 == 0:
			calls.append(prices[i])
	print calls
	"Full list of stuff, and then these stocks are the indexes"
	Amazon = []
	Apple = []
	Bidu = []
	Colgate = []
	Costco = []
	GS = []
	IBM = []
	MasterCard = []
	NTES = []
	Netflix = []
	RalphLauren = []
	WYNN = []
	for i in range(len(prices)):
		if 0 <= i < 10:
			Amazon.append(prices[i])
		elif 10 <= i < 20:
			Apple.append(prices[i])
		elif 20 <= i <= 30:
			Bidu.append(prices[i])
		elif 30 <= i < 40:
			Colgate.append(prices[i])
		elif 40 <= i < 50:
			Costco.append(prices[i])
		elif 50 <= i < 60:
			GS.append(prices[i])
		elif 60 <= i < 70:
			IBM.append(prices[i])
		elif 70 <= i < 80:
			MasterCard.append(prices[i])
		elif 80 <= i < 90:
			NTES.append(prices[i])
		elif 90 <= i < 100:
			Netflix.append(prices[i])
		elif 100 <= i < 110:
			RalphLauren.append(prices[i])
		elif 110 <= i < 120:
			WYNN.append(prices[i])
	result = ""
	for j, date in enumerate(Amazon):
		for i, combo in enumerate(date):
			if i == 0:
				result += '"' + str(combo)+ '":[\n'
			elif i+1 == len(date):
				result += '     {"strike":'+str(combo[0])+', "price":'+str(combo[1])+'}\n],\n'
			else:
				result += '     {"strike":'+str(combo[0])+', "price":'+str(combo[1])+'},\n'
	print result


if __name__ == "__main__":
	main()