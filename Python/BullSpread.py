from matplotlib import pyplot, pylab
import math
import numpy as np
import scipy.stats as ss
import time
import csv
import random

def CallSpread(K1, P1, T1, K2, P2, T2, S0):
	"""
	K1,P1 : Strike and price of long call
	K2,P2 : Strike and price of short call
	S0: stock price at t=0
	T = time untill expiration
	"""
	lay_in = P1-P2
	long = []
	short = []
	spot_range = []
	for St in range(min(K1,K2)-20, max(K1,K2)+20):
		spot_range.append(St)
		if St < K1:
			long.append(-P1)
		else:
			long.append(-P1+100*(St-K1))

		if St < K2:
			short.append(P2)
		else:
			short.append(P2 - 100*(St-K2))
	profit = [long[i]+short[i] for i in range(len(long))]
	print "Maximum loss/profit: ",profit[0], profit[-1]
	root = 0
	for i in range(len(profit)-1):
		if profit[i] <= 0 and profit[i+1] >= 0:
			root = min(K1,K2)-20+i-profit[i]/(profit[i+1]-profit[i])
			print "Break even at ", root
			break
		elif profit[i] >= 0 and profit[i+1] <= 0:
			root = min(K1,K2)-20+i-profit[i]/(profit[i+1]-profit[i])
			print "Break even at ", root
			break

	plotIt(short, long, profit, spot_range, S0, root)

def BullPutSpread(K1, P1, T1, K2, P2, T2, S0):
	lay_in = P2-P1
	long = []
	short = []
	spot_range = []
	for St in range(K1-20, K2+20):
		spot_range.append(St)
		if St > K1:
			long.append(-P1)
		else:
			long.append(-P1+100*(K1-St))

		if St > K2:
			short.append(P2)
		else:
			short.append(P2 - 100*(K2-St))

	profit = [long[i]+short[i] for i in range(len(long))]
	print "Maximum loss/profit: ",profit[0], profit[-1]
	plotIt(short, long, profit, spot_range, S0)

def butterflySpread(K1, P1, T1, K2, P2, T2, K3, P3, T3, S0):
	"K2 is short"
	long1 = []
	long2 = []
	short = []
	spot_range = []
	for St in range(K1-5, K3+5):
		spot_range.append(St)
		if St < K1:
			long1.append(-P1)
		else:
			long1.append(-P1+100*(St-K1))

		if St < K2:
			short.append(2*P2)
		else:
			short.append(2*(P2 - 100*(St-K2)))

		if St < K3:
			long2.append(-P3)
		else:
			long2.append(-P3+100*(St-K3))
	profit = [long1[i]+long2[i]+short[i] for i in range(len(long1))]
	print "Maximum loss/profit: ",min(profit), max(profit)
	plotIt(short, long1, profit, spot_range, S0, 0, long2)



def plotIt(short, long, profit, spot_range, spot, root, third = None):
	maximum = max(profit)
	minimum = min(profit)
	pyplot.figure
	pyplot.xlabel('Stock price at expiration date')
	pyplot.ylabel('Profit')
	pyplot.title('Profit of a bull spread')
	pyplot.text(S0-1, maximum+maximum/10, 'S0')
	pyplot.vlines(x=spot, ymin=minimum, ymax=maximum)
	pyplot.vlines(x=root, ymin=minimum, ymax=maximum)
	#pyplot.text(K1-0.5, 0.5, 'K1')
	#pyplot.text(K2-0.5, 0.5, 'K2')
	#pyplot.vlines(x=K1, ymin=0, ymax=0.3)
	#pyplot.vlines(x=K2, ymin=0, ymax=0.3)
	pyplot.plot(spot_range, short, 'b--', label="Short Call")
	pyplot.plot(spot_range, long, 'g--', label="Long Call")
	if third != None:
		pyplot.plot(spot_range, third, 'y--', label="Long Call")
	pyplot.plot(spot_range, profit, 'r', label="Profit")
	pyplot.plot(spot_range, [0]*len(spot_range), 'black')
	pylab.xlim([spot_range[0],spot_range[-1]])
	pylab.ylim(2*minimum,2*maximum)

	pyplot.legend(loc=2)
	pyplot.show()


if __name__ == '__main__':
	bullCall = True
	S0 = 85.2
	calls = [['CALL AMZN January 2', (250.0, 60.7), (265.0, 33.8), (275.0, 35.8), (277.5, 33.3), (280.0, 31.65), (282.5, 21.25), (287.5, 14.65), (290.0, 20.47), (292.5, 15.5), (295.0, 13.7), (297.5, 14.05), (300.0, 9.2), (302.5, 5.2), (305.0, 3.0), (307.5, 1.25), (310.0, 0.4), (312.5, 0.12), (315.0, 0.06), (317.5, 0.02), (320.0, 0.01), (322.5, 0.02), (325.0, 0.01), (327.5, 0.03), (330.0, 0.03), (332.5, 0.02), (335.0, 0.01), (337.5, 0.01), (340.0, 0.01), (342.5, 0.01), (345.0, 0.01), (347.5, 0.06), (350.0, 0.05), (352.5, 0.04), (355.0, 0.01), (357.5, 0.71), (360.0, 0.06), (362.5, 0.48), (365.0, 0.44), (367.5, 1.06), (370.0, 0.12), (372.5, 0.34), (375.0, 0.05), (377.5, 0.43), (380.0, 0.04), (382.5, 0.2), (385.0, 0.03), (390.0, 0.03), (395.0, 0.16), (400.0, 0.15), (405.0, 0.26), (410.0, 0.17), (415.0, 0.14), (420.0, 0.17), (425.0, 0.18), (430.0, 0.24), (450.0, 0.07), (465.0, 0.1), (470.0, 0.08), (475.0, 0.07)], ['CALL AMZN January 9', (270.0, 33.2), (275.0, 29.9), (280.0, 30.93), (285.0, 16.0), (290.0, 23.5), (292.5, 16.0), (295.0, 19.5), (297.5, 14.4), (300.0, 10.0), (302.5, 8.5), (305.0, 6.92), (307.5, 7.0), (310.0, 4.1), (312.5, 3.18), (315.0, 2.4), (317.5, 2.1), (320.0, 1.26), (322.5, 0.91), (325.0, 0.65), (327.5, 0.54), (330.0, 0.4), (332.5, 0.23), (335.0, 0.21), (337.5, 0.25), (340.0, 0.22), (342.5, 0.09), (345.0, 0.14), (347.5, 0.15), (350.0, 0.07), (352.5, 0.34), (355.0, 0.09), (357.5, 0.65), (360.0, 0.08), (365.0, 0.47), (367.5, 0.26), (370.0, 0.05), (372.5, 0.16), (375.0, 0.74), (385.0, 0.2), (390.0, 0.2), (395.0, 0.17), (400.0, 0.27), (405.0, 0.19)], ['CALL AMZN January 17', (115.0, 195.0), (120.0, 193.09), (125.0, 188.45), (130.0, 172.75), (135.0, 205.9), (140.0, 172.0), (145.0, 253.85), (150.0, 161.18), (155.0, 139.2), (160.0, 150.1), (165.0, 145.9), (170.0, 128.14), (175.0, 149.0), (180.0, 137.0), (185.0, 129.25), (190.0, 122.5), (195.0, 101.95), (200.0, 111.0), (205.0, 90.0), (210.0, 106.0), (215.0, 82.2), (220.0, 92.34), (225.0, 86.36), (230.0, 81.2), (235.0, 73.18), (240.0, 65.25), (245.0, 53.25), (250.0, 61.32), (255.0, 57.3), (260.0, 49.71), (265.0, 32.15), (270.0, 41.0), (275.0, 35.26), (280.0, 32.0), (285.0, 28.25), (290.0, 19.65), (292.5, 19.3), (295.0, 15.7), (297.5, 16.2), (300.0, 12.1), (302.5, 11.2), (305.0, 8.7), (307.5, 7.1), (310.0, 5.95), (312.5, 5.13), (315.0, 3.9), (317.5, 3.3), (320.0, 2.53), (322.5, 2.17), (325.0, 1.6), (327.5, 1.54), (330.0, 1.21), (332.5, 1.26), (335.0, 0.68), (337.5, 0.56), (340.0, 0.52), (342.5, 0.37), (345.0, 0.33), (347.5, 0.4), (350.0, 0.26), (352.5, 0.33), (355.0, 0.21), (357.5, 0.2), (360.0, 0.17), (365.0, 0.07), (370.0, 0.1), (372.5, 0.18), (375.0, 0.08), (377.5, 0.16), (380.0, 0.08), (382.5, 0.07), (385.0, 0.09), (390.0, 0.06), (395.0, 0.05), (400.0, 0.01), (405.0, 0.01), (410.0, 0.02), (415.0, 0.1), (420.0, 0.03), (425.0, 0.04), (430.0, 0.01), (435.0, 0.02), (440.0, 0.01), (445.0, 0.18), (450.0, 0.01), (455.0, 0.11), (460.0, 0.01), (465.0, 0.18), (470.0, 0.01), (475.0, 0.01), (480.0, 0.06), (485.0, 0.12), (490.0, 0.09), (495.0, 0.03), (500.0, 0.01), (505.0, 0.08), (510.0, 0.09), (515.0, 0.1), (520.0, 0.02), (525.0, 0.04), (530.0, 0.05), (535.0, 0.05), (540.0, 0.04), (545.0, 0.04), (550.0, 0.04), (555.0, 0.04), (560.0, 0.03), (565.0, 0.03), (570.0, 0.03), (575.0, 0.03), (580.0, 0.03), (585.0, 0.03), (590.0, 0.03), (595.0, 0.03), (600.0, 0.02)], ['CALL AMZN January 23', (250.0, 64.5), (255.0, 44.6), (260.0, 40.3), (265.0, 38.2), (270.0, 36.79), (272.5, 37.15), (275.0, 34.77), (277.5, 31.65), (280.0, 35.0), (282.5, 30.5), (285.0, 23.43), (287.5, 19.5), (290.0, 26.6), (292.5, 21.65), (295.0, 19.7), (297.5, 16.4), (300.0, 15.5), (302.5, 13.55), (305.0, 13.99), (307.5, 11.3), (310.0, 7.7), (312.5, 9.15), (315.0, 7.85), (317.5, 5.65), (320.0, 3.75), (322.5, 3.05), (325.0, 2.64), (327.5, 2.16), (330.0, 1.87), (332.5, 1.72), (335.0, 1.77), (337.5, 1.73), (340.0, 1.39), (342.5, 0.93), (345.0, 1.65), (347.5, 1.28), (350.0, 0.62), (355.0, 1.8), (360.0, 0.31), (365.0, 0.94), (380.0, 0.58), (385.0, 0.7), (390.0, 0.38), (395.0, 0.5), (400.0, 0.38)], ['CALL AMZN January 30', (255.0, 54.45), (260.0, 53.35), (270.0, 41.65), (272.5, 40.75), (275.0, 34.5), (280.0, 38.0), (282.5, 25.25), (285.0, 21.7), (287.5, 29.2), (290.0, 28.2), (295.0, 23.55), (297.5, 17.2), (300.0, 20.87), (302.5, 21.1), (305.0, 18.1), (307.5, 15.25), (310.0, 15.0), (312.5, 16.04), (315.0, 14.86), (317.5, 12.47), (320.0, 11.8), (322.5, 11.3), (325.0, 9.0), (327.5, 8.6), (330.0, 6.85), (332.5, 7.0), (335.0, 6.7), (340.0, 5.5), (342.5, 4.09), (345.0, 3.9), (350.0, 3.27), (355.0, 2.8), (360.0, 2.3), (365.0, 2.13), (370.0, 1.5), (375.0, 1.09), (380.0, 1.04), (400.0, 0.6)], ['CALL AAPL January 2', (90.0, 17.95), (95.0, 12.95), (96.0, 14.45), (97.0, 11.45), (98.0, 12.85), (99.0, 13.6), (100.0, 8.2), (101.0, 8.01), (102.0, 6.05), (103.0, 4.94), (104.0, 4.0), (105.0, 3.05), (106.0, 2.31), (107.0, 1.29), (108.0, 0.62), (109.0, 0.24), (110.0, 0.07), (111.0, 0.03), (112.0, 0.03), (113.0, 0.02), (114.0, 0.01), (115.0, 0.01), (116.0, 0.01), (117.0, 0.01), (118.0, 0.01), (119.0, 0.01), (120.0, 0.01), (121.0, 0.01), (122.0, 0.01), (123.0, 0.01), (124.0, 0.01), (125.0, 0.02), (126.0, 0.01), (127.0, 0.01), (128.0, 0.01), (129.0, 0.01), (130.0, 0.01), (131.0, 0.01), (132.0, 0.01), (133.0, 0.04), (134.0, 0.01), (135.0, 0.01), (136.0, 0.02), (137.0, 0.01), (140.0, 0.01), (145.0, 0.06), (150.0, 0.03), (155.0, 0.03), (170.0, 0.03)], ['CALL AAPL January 9', (90.0, 18.05), (95.0, 18.22), (100.0, 8.59), (103.0, 5.5), (104.0, 5.55), (105.0, 4.15), (106.0, 3.32), (107.0, 2.61), (108.0, 2.01), (109.0, 1.51), (110.0, 1.08), (111.0, 0.78), (112.0, 0.56), (113.0, 0.38), (114.0, 0.26), (115.0, 0.16), (116.0, 0.11), (117.0, 0.09), (118.0, 0.07), (119.0, 0.05), (120.0, 0.04), (121.0, 0.03), (122.0, 0.03), (123.0, 0.02), (124.0, 0.03), (125.0, 0.02), (126.0, 0.02), (127.0, 0.01), (128.0, 0.01), (129.0, 0.01), (130.0, 0.01), (131.0, 0.01), (133.0, 0.13), (134.0, 0.23), (135.0, 0.08), (140.0, 0.01), (175.0, 0.01)], ['CALL AAPL January 17', (27.86, 82.74), (28.57, 82.02), (29.29, 84.75), (30.0, 81.2), (30.71, 83.2), (31.43, 79.75), (32.14, 87.75), (32.86, 76.38), (33.57, 75.0), (34.29, 78.45), (35.71, 73.95), (37.14, 75.25), (37.86, 71.6), (38.57, 76.85), (39.29, 69.65), (40.0, 77.8), (40.71, 67.95), (41.43, 73.5), (42.14, 66.61), (42.86, 67.6), (43.57, 68.75), (44.29, 65.35), (45.0, 62.3), (45.71, 65.5), (46.43, 62.4), (47.14, 65.5), (47.86, 63.35), (48.57, 62.2), (49.29, 69.18), (50.0, 58.05), (50.71, 67.32), (51.43, 57.82), (52.14, 57.15), (52.86, 61.4), (53.57, 53.9), (54.29, 55.0), (55.0, 60.95), (55.71, 56.15), (56.43, 56.64), (57.14, 50.7), (57.86, 57.0), (58.57, 53.84), (59.29, 53.15), (60.0, 48.3), (60.71, 48.0), (61.43, 46.5), (62.14, 46.75), (62.86, 45.15), (63.57, 48.35), (64.29, 44.2), (65.0, 48.3), (65.71, 42.35), (66.43, 44.05), (67.14, 40.65), (67.86, 43.4), (68.57, 39.5), (69.29, 39.8), (70.0, 38.46), (70.71, 37.4), (71.43, 36.62), (72.14, 40.5), (72.86, 35.2), (73.57, 37.4), (74.29, 33.25), (75.0, 33.0), (75.71, 32.3), (76.43, 31.71), (77.14, 32.4), (77.86, 30.52), (78.57, 29.45), (79.29, 29.0), (80.0, 27.8), (80.71, 27.0), (81.43, 27.04), (82.14, 27.2), (82.86, 25.5), (83.57, 28.1), (84.29, 23.8), (85.0, 23.3), (85.71, 22.5), (86.43, 21.82), (87.14, 20.95), (87.86, 23.3), (88.57, 22.1), (89.29, 20.54), (90.0, 18.15), (90.71, 17.9), (91.43, 19.15), (92.14, 16.47), (92.86, 15.6), (93.57, 15.08), (94.0, 19.24), (94.29, 13.95), (95.0, 13.3), (95.71, 12.6), (96.43, 12.25), (97.14, 11.8), (97.86, 10.8), (98.57, 9.5), (99.0, 9.95), (99.29, 9.45), (100.0, 8.58), (100.71, 8.1), (101.0, 7.83), (101.43, 7.65), (102.0, 7.9), (102.14, 6.9), (102.86, 6.48), (103.0, 6.75), (103.57, 5.45), (104.0, 5.9), (104.29, 5.35), (105.0, 4.56), (105.71, 4.25), (106.0, 4.0), (106.43, 3.75), (107.0, 3.3), (107.14, 3.25), (107.86, 2.68), (108.0, 2.69), (108.57, 2.38), (109.0, 2.15), (109.29, 2.12), (110.0, 1.75), (110.71, 1.5), (111.0, 1.38), (111.43, 1.21), (112.0, 1.06), (112.14, 1.03), (112.86, 0.89), (113.0, 0.83), (113.57, 0.77), (114.0, 0.65), (114.29, 0.58), (115.0, 0.47), (115.71, 0.42), (116.0, 0.39), (116.43, 0.33), (117.0, 0.3), (117.14, 0.3), (117.86, 0.25), (118.0, 0.22), (118.57, 0.19), (119.0, 0.2), (119.29, 0.17), (120.0, 0.13), (120.71, 0.11), (121.0, 0.11), (121.43, 0.11), (122.0, 0.09), (122.14, 0.1), (122.86, 0.1), (123.0, 0.09), (124.0, 0.09), (124.29, 0.07), (125.0, 0.07), (125.71, 0.07), (126.0, 0.06), (127.0, 0.06), (127.14, 0.04), (128.0, 0.05), (128.57, 0.04), (129.0, 0.08), (130.0, 0.04), (131.0, 0.03), (131.43, 0.02), (132.86, 0.02), (134.0, 0.04), (134.29, 0.05), (135.0, 0.04), (135.71, 0.03), (137.14, 0.04), (138.57, 0.02), (140.0, 0.02), (141.43, 0.02), (142.86, 0.01), (144.29, 0.01), (145.0, 0.01), (145.71, 0.03), (147.14, 0.02), (148.57, 0.02), (150.0, 0.01), (155.0, 0.01), (160.0, 0.01), (165.0, 0.01), (170.0, 0.01), (175.0, 0.04)], ['CALL AAPL January 23', (80.0, 32.79), (85.0, 29.59), (90.0, 24.0), (95.0, 13.53), (96.0, 12.9), (99.0, 11.99), (100.0, 8.95), (101.0, 11.91), (102.0, 7.65), (103.0, 6.6), (104.0, 5.85), (105.0, 5.1), (106.0, 4.5), (107.0, 3.9), (108.0, 3.27), (109.0, 2.8), (110.0, 2.35), (111.0, 1.85), (112.0, 1.55), (113.0, 1.33), (114.0, 1.02), (115.0, 0.81), (116.0, 0.63), (117.0, 0.52), (118.0, 0.44), (119.0, 0.42), (120.0, 0.3), (121.0, 0.23), (122.0, 0.19), (123.0, 0.19), (124.0, 0.25), (125.0, 0.11), (126.0, 0.13), (127.0, 0.14), (128.0, 0.1), (129.0, 0.19), (130.0, 0.08), (135.0, 0.04), (140.0, 0.05)], ['CALL AAPL January 30', (80.0, 31.0), (90.0, 18.6), (95.0, 15.0), (98.0, 14.74), (100.0, 9.6), (101.0, 8.81), (102.0, 8.0), (103.0, 12.4), (104.0, 7.45), (105.0, 6.0), (106.0, 5.4), (107.0, 5.0), (108.0, 4.3), (109.0, 3.8), (110.0, 3.4), (111.0, 2.99), (112.0, 2.58), (113.0, 2.29), (114.0, 2.03), (115.0, 1.7), (116.0, 1.35), (117.0, 1.28), (118.0, 1.14), (119.0, 1.0), (120.0, 0.78), (121.0, 0.97), (122.0, 0.59), (123.0, 0.57), (124.0, 0.61), (125.0, 0.38), (126.0, 0.4), (127.0, 0.55), (128.0, 0.37), (130.0, 0.19), (135.0, 0.11), (140.0, 0.12)], ['CALL BIDU January 2', (200.0, 35.16), (210.0, 19.6), (212.5, 13.6), (215.0, 17.2), (217.5, 17.5), (220.0, 4.35), (222.5, 1.59), (225.0, 0.6), (227.5, 0.11), (230.0, 0.06), (232.5, 0.02), (235.0, 0.02), (237.5, 0.01), (240.0, 0.01), (242.5, 0.02), (245.0, 0.02), (247.5, 0.02), (250.0, 0.01), (252.5, 0.02), (255.0, 0.03), (257.5, 0.01), (260.0, 0.01), (262.5, 0.12), (265.0, 0.01), (267.5, 0.25), (270.0, 0.07), (272.5, 0.26), (275.0, 0.2), (277.5, 2.4), (280.0, 2.5), (287.5, 0.01), (310.0, 0.01)], ['CALL BIDU January 9', (200.0, 25.1), (205.0, 25.16), (207.5, 15.5), (210.0, 16.1), (212.5, 13.2), (215.0, 10.5), (217.5, 11.8), (220.0, 6.52), (222.5, 5.0), (225.0, 3.45), (227.5, 2.6), (230.0, 1.75), (232.5, 1.1), (235.0, 0.64), (237.5, 0.41), (240.0, 0.24), (242.5, 0.11), (245.0, 0.13), (247.5, 0.26), (250.0, 0.04), (252.5, 0.03), (255.0, 0.05), (257.5, 0.19), (260.0, 0.05), (262.5, 0.05), (270.0, 1.06), (285.0, 0.1)], ['CALL BIDU January 17', (42.5, 171.3), (45.0, 170.91), (47.5, 123.35), (50.0, 195.2), (55.0, 103.5), (60.0, 139.7), (65.0, 121.68), (70.0, 164.94), (75.0, 144.58), (77.5, 96.3), (80.0, 149.0), (82.5, 76.36), (85.0, 144.79), (87.5, 148.34), (90.0, 136.2), (92.5, 142.14), (95.0, 130.34), (97.5, 153.0), (100.0, 128.5), (105.0, 122.59), (110.0, 110.0), (115.0, 128.49), (120.0, 108.1), (125.0, 105.0), (130.0, 93.45), (135.0, 99.6), (140.0, 91.2), (145.0, 80.25), (150.0, 78.29), (155.0, 73.03), (160.0, 69.9), (165.0, 70.99), (170.0, 59.5), (175.0, 50.0), (180.0, 48.0), (185.0, 43.0), (190.0, 38.4), (195.0, 32.5), (200.0, 24.5), (210.0, 18.65), (215.0, 11.9), (220.0, 8.3), (222.5, 7.79), (225.0, 4.89), (227.5, 4.4), (230.0, 2.95), (232.5, 2.32), (235.0, 1.61), (237.5, 1.27), (240.0, 0.94), (242.5, 0.63), (245.0, 0.43), (247.5, 0.58), (250.0, 0.24), (252.5, 0.38), (255.0, 0.1), (257.5, 0.12), (260.0, 0.08), (262.5, 0.09), (265.0, 0.03), (267.5, 0.05), (270.0, 0.04), (272.5, 0.15), (275.0, 0.03), (277.5, 0.15), (280.0, 0.01), (290.0, 0.03), (295.0, 0.04), (297.5, 0.06), (300.0, 0.04), (310.0, 0.09), (320.0, 0.05), (330.0, 0.01), (340.0, 0.04)], ['CALL BIDU January 23', (185.0, 41.79), (202.5, 20.76), (212.5, 23.65), (215.0, 12.1), (217.5, 10.35), (220.0, 9.35), (222.5, 7.35), (225.0, 7.65), (227.5, 7.35), (230.0, 4.1), (232.5, 3.96), (235.0, 4.4), (237.5, 2.01), (240.0, 1.8), (242.5, 2.64), (245.0, 1.54), (247.5, 1.26), (250.0, 1.15), (252.5, 1.94), (255.0, 0.39), (257.5, 1.74), (260.0, 0.59), (265.0, 0.51), (280.0, 0.42), (285.0, 0.07), (290.0, 0.22)], ['CALL BIDU January 30', (200.0, 36.0), (202.5, 24.7), (210.0, 23.0), (220.0, 10.2), (222.5, 9.3), (227.5, 9.83), (230.0, 6.0), (232.5, 6.87), (235.0, 4.5), (237.5, 3.09), (240.0, 3.78), (242.5, 2.02), (245.0, 2.56), (250.0, 1.18), (252.5, 2.56), (255.0, 0.78), (257.5, 2.0), (270.0, 1.23)], ['CALL CL January 2', (65.0, 4.32), (66.0, 5.11), (67.0, 3.69), (67.5, 2.66), (68.0, 0.8), (68.5, 0.9), (69.0, 1.71), (69.5, 0.71), (70.0, 1.23), (70.5, 0.16), (71.0, 0.39), (71.5, 0.01), (72.0, 0.15), (72.5, 0.08), (77.0, 0.01)], ['CALL CL January 9', (60.0, 10.0), (65.0, 5.5), (66.5, 2.18), (67.0, 1.84), (67.5, 1.48), (68.0, 3.34), (68.5, 1.31), (69.0, 0.83), (69.5, 1.05), (70.0, 0.41), (70.5, 0.74), (71.0, 0.5), (71.5, 0.16), (72.0, 0.28), (72.5, 0.19), (73.0, 0.03)], ['CALL CL January 17', (27.5, 39.45), (40.0, 28.15), (42.5, 15.3), (45.0, 22.8), (47.5, 22.07), (48.75, 19.15), (50.0, 18.63), (52.5, 16.55), (55.0, 13.85), (57.5, 13.09), (60.0, 10.88), (62.5, 5.95), (65.0, 4.63), (67.5, 2.64), (70.0, 0.37), (70.5, 0.29), (71.0, 0.18), (71.5, 0.39), (72.0, 0.36), (72.5, 0.08), (73.5, 0.2), (74.5, 0.06), (75.0, 0.05), (77.5, 0.04), (80.0, 0.04), (82.5, 0.02), (85.0, 0.04)], ['CALL CL January 23', (65.5, 3.35), (68.0, 1.26), (69.0, 1.95), (69.5, 1.77), (70.0, 0.75), (71.0, 0.72), (72.5, 0.3), (73.0, 0.23)], ['CALL CL January 30', (69.5, 0.86), (70.0, 1.4), (71.0, 0.76), (71.5, 0.52), (72.0, 0.8)], ['CALL COST January 2', (115.0, 27.65), (125.0, 17.8), (130.0, 13.6), (132.0, 13.05), (133.0, 9.8), (134.0, 8.8), (135.0, 7.95), (137.0, 5.8), (138.0, 5.4), (139.0, 3.7), (140.0, 3.0), (141.0, 0.8), (142.0, 0.27), (143.0, 0.1), (144.0, 0.04), (145.0, 0.01), (146.0, 0.5), (147.0, 0.08), (148.0, 0.09), (149.0, 0.23), (150.0, 0.3), (152.5, 0.16)], ['CALL COST January 9', (125.0, 17.05), (130.0, 14.83), (134.0, 5.75), (135.0, 7.8), (136.0, 7.6), (137.0, 6.98), (138.0, 6.2), (139.0, 3.9), (140.0, 2.95), (141.0, 2.27), (142.0, 1.24), (143.0, 1.07), (144.0, 0.77), (145.0, 0.5), (146.0, 0.44), (147.0, 0.4), (148.0, 0.24), (149.0, 0.66), (150.0, 0.36), (152.5, 0.17), (155.0, 0.15)], ['CALL COST January 17', (50.0, 68.5), (53.0, 85.1), (55.0, 63.95), (58.0, 58.3), (60.0, 79.6), (63.0, 74.57), (65.0, 65.2), (68.0, 44.07), (70.0, 68.18), (73.0, 47.89), (75.0, 29.07), (78.0, 40.9), (80.0, 62.58), (83.0, 59.47), (85.5, 57.04), (88.0, 48.8), (90.5, 52.28), (93.0, 45.6), (95.0, 44.0), (98.0, 38.8), (100.0, 42.75), (103.0, 35.05), (105.0, 38.85), (108.0, 34.25), (110.0, 33.8), (113.0, 29.68), (115.0, 27.75), (118.0, 24.9), (120.0, 22.0), (123.0, 18.8), (125.0, 17.43), (126.0, 18.45), (128.0, 15.47), (130.0, 12.62), (133.0, 10.25), (135.0, 9.05), (138.0, 4.9), (139.0, 4.8), (140.0, 2.83), (141.0, 2.47), (142.0, 2.29), (143.0, 1.84), (144.0, 1.01), (145.0, 0.7), (146.0, 0.65), (147.0, 0.41), (148.0, 0.3), (149.0, 0.15), (150.0, 0.11), (152.5, 0.07), (155.0, 0.04), (160.0, 0.05), (165.0, 0.18), (170.0, 0.2), (175.0, 0.1), (180.0, 0.09), (210.0, 0.02)], ['CALL COST January 23', (130.0, 9.2), (133.0, 6.75), (134.0, 5.95), (135.0, 6.38), (136.0, 4.16), (137.0, 5.8), (138.0, 5.0), (139.0, 4.8), (140.0, 3.55), (141.0, 3.0), (142.0, 2.49), (143.0, 1.99), (144.0, 1.58), (145.0, 1.19), (146.0, 1.17), (147.0, 1.0), (148.0, 0.64), (149.0, 0.56), (150.0, 0.35), (152.5, 0.2), (167.5, 0.06)], ['CALL COST January 30', (125.0, 17.6), (135.0, 6.15), (136.0, 7.15), (137.0, 4.8), (138.0, 5.8), (139.0, 3.6), (140.0, 5.54), (141.0, 4.25), (142.0, 3.65), (143.0, 2.25), (144.0, 1.91), (145.0, 1.7), (146.0, 1.45), (147.0, 1.03), (148.0, 0.81), (149.0, 0.51), (150.0, 0.32), (152.5, 0.18), (160.0, 0.1)], ['CALL GS January 2', (165.0, 26.5), (167.5, 23.5), (170.0, 24.62), (180.0, 14.39), (182.5, 7.8), (185.0, 10.3), (187.5, 7.87), (190.0, 5.34), (192.5, 2.94), (195.0, 0.7), (197.5, 0.04), (200.0, 0.01), (202.5, 0.13), (205.0, 0.05), (210.0, 0.06)], ['CALL GS January 9', (180.0, 13.1), (182.5, 6.55), (185.0, 10.96), (187.5, 8.66), (190.0, 4.15), (192.5, 3.6), (195.0, 2.07), (197.5, 0.9), (200.0, 0.47), (202.5, 0.2), (210.0, 0.1), (212.5, 0.15)], ['CALL GS January 17', (60.0, 106.5), (70.0, 120.5), (75.0, 87.7), (80.0, 108.26), (85.0, 103.19), (90.0, 98.25), (95.0, 93.25), (100.0, 95.0), (105.0, 91.32), (110.0, 78.5), (115.0, 75.0), (120.0, 76.38), (125.0, 61.45), (130.0, 63.21), (135.0, 60.65), (140.0, 53.97), (145.0, 50.5), (150.0, 43.55), (155.0, 39.3), (160.0, 34.24), (165.0, 31.53), (170.0, 25.3), (175.0, 20.54), (180.0, 14.15), (185.0, 9.65), (187.5, 10.12), (190.0, 5.77), (192.5, 5.4), (195.0, 2.68), (197.5, 1.69), (200.0, 1.1), (202.5, 0.8), (205.0, 0.51), (207.5, 0.42), (210.0, 0.2), (215.0, 0.09), (220.0, 0.1), (225.0, 0.22), (230.0, 0.03), (235.0, 0.06), (240.0, 0.09), (245.0, 1.01), (250.0, 0.7), (255.0, 0.02)], ['CALL GS January 23', (150.0, 34.0), (175.0, 22.0), (180.0, 17.0), (182.5, 13.47), (185.0, 11.58), (187.5, 8.4), (190.0, 6.65), (192.5, 5.65), (195.0, 4.45), (197.5, 3.76), (200.0, 2.14), (202.5, 1.77), (205.0, 1.12), (207.5, 0.67), (210.0, 0.31)], ['CALL GS January 30', (180.0, 15.31), (182.5, 6.93), (185.0, 10.5), (187.5, 10.2), (190.0, 7.8), (192.5, 5.88), (195.0, 4.65), (197.5, 3.98), (200.0, 2.32), (202.5, 1.1), (205.0, 0.88), (207.5, 1.14), (210.0, 0.67)], ['CALL IBM January 2', (145.0, 16.1), (146.0, 7.8), (149.0, 13.79), (150.0, 10.51), (152.5, 8.75), (155.0, 5.45), (157.5, 3.62), (160.0, 2.34), (162.5, 0.21), (165.0, 0.03), (167.5, 0.03), (170.0, 0.01), (172.5, 0.04), (175.0, 0.03), (180.0, 0.05), (182.5, 0.08), (195.0, 0.04), (200.0, 0.02)], ['CALL IBM January 9', (144.0, 8.7), (145.0, 15.62), (150.0, 10.0), (152.5, 10.5), (155.0, 7.25), (157.5, 6.0), (160.0, 3.1), (162.5, 1.52), (165.0, 0.5), (167.5, 0.19), (170.0, 0.05), (172.5, 0.06), (175.0, 0.2), (185.0, 0.06)], ['CALL IBM January 17', (90.0, 100.0), (95.0, 66.75), (100.0, 63.0), (105.0, 52.45), (110.0, 51.54), (115.0, 40.64), (120.0, 42.7), (125.0, 30.96), (130.0, 31.2), (135.0, 28.4), (140.0, 22.75), (145.0, 15.39), (150.0, 13.1), (155.0, 8.56), (157.5, 5.45), (160.0, 4.1), (162.5, 2.14), (165.0, 1.02), (167.5, 0.57), (170.0, 0.21), (172.5, 0.11), (175.0, 0.05), (177.5, 0.06), (180.0, 0.02), (185.0, 0.03), (190.0, 0.01), (195.0, 0.01), (200.0, 0.01), (205.0, 0.04), (210.0, 0.05), (215.0, 0.01), (220.0, 0.01), (225.0, 0.05), (230.0, 0.05), (235.0, 0.01), (240.0, 0.02), (245.0, 0.05), (250.0, 0.01), (255.0, 0.03), (260.0, 0.02), (265.0, 0.04), (270.0, 0.02), (275.0, 0.03), (280.0, 0.03), (290.0, 0.01), (300.0, 0.02), (310.0, 0.02), (320.0, 0.02)], ['CALL IBM January 23', (140.0, 20.17), (150.0, 11.28), (152.5, 4.75), (155.0, 7.6), (157.5, 7.3), (160.0, 4.5), (162.5, 3.9), (165.0, 2.8), (167.5, 1.7), (170.0, 1.29), (172.5, 0.65), (175.0, 0.28), (177.5, 0.22), (180.0, 0.15), (185.0, 0.19)], ['CALL IBM January 30', (140.0, 13.5), (150.0, 12.22), (155.0, 8.04), (157.5, 6.96), (160.0, 4.55), (162.5, 3.51), (165.0, 2.97), (167.5, 1.4), (170.0, 1.39), (172.5, 0.91), (175.0, 0.43), (177.5, 0.25)], ['CALL MA January 2', (72.5, 12.1), (75.0, 9.8), (76.0, 10.83), (77.0, 9.92), (78.0, 8.5), (79.0, 7.95), (80.0, 6.5), (81.0, 4.05), (82.0, 3.8), (83.0, 3.85), (84.0, 2.55), (85.0, 1.95), (86.0, 0.22), (87.0, 0.11), (88.0, 0.03), (89.0, 0.02), (90.0, 0.01), (91.0, 0.06), (92.0, 0.1), (94.0, 0.24), (95.0, 0.18), (96.0, 0.1), (100.0, 0.05)], ['CALL MA January 9', (73.5, 11.1), (74.5, 10.05), (76.0, 8.6), (77.0, 7.6), (78.0, 6.15), (81.0, 5.1), (82.0, 5.25), (83.0, 2.75), (84.0, 2.77), (85.0, 2.25), (86.0, 0.83), (87.0, 0.71), (88.0, 0.2), (89.0, 0.14), (90.0, 0.13), (91.0, 0.2), (92.0, 0.13), (93.0, 0.25), (95.0, 0.31)], ['CALL MA January 17', (2.5, 73.95), (23.0, 52.0), (23.5, 33.92), (24.0, 43.87), (25.0, 50.0), (25.5, 38.35), (26.5, 48.5), (27.0, 47.8), (28.0, 27.19), (28.5, 46.3), (29.0, 46.0), (29.5, 45.2), (30.0, 44.19), (31.0, 44.15), (32.0, 28.26), (33.0, 43.0), (34.0, 38.8), (35.0, 48.94), (36.0, 37.43), (36.5, 46.99), (37.0, 34.8), (38.0, 36.85), (39.0, 37.6), (39.5, 42.64), (40.0, 47.65), (40.5, 41.69), (41.0, 43.09), (41.5, 41.97), (42.0, 40.49), (42.5, 34.05), (43.0, 32.6), (44.0, 29.65), (44.5, 29.15), (45.0, 38.7), (45.5, 30.99), (46.0, 37.54), (46.5, 37.47), (47.0, 28.2), (47.5, 28.4), (48.0, 25.8), (48.5, 34.51), (49.0, 40.15), (49.5, 33.8), (50.0, 36.7), (50.5, 32.22), (51.0, 28.8), (51.5, 30.97), (52.0, 25.6), (52.5, 28.5), (53.0, 28.9), (53.5, 29.12), (54.0, 33.05), (54.5, 29.79), (55.0, 31.35), (55.5, 28.39), (56.0, 30.47), (56.5, 17.5), (57.0, 19.05), (57.5, 25.0), (58.0, 29.61), (58.5, 25.35), (59.0, 24.52), (59.5, 12.05), (60.0, 26.5), (60.5, 18.95), (61.0, 20.0), (61.5, 22.76), (62.0, 23.05), (62.5, 19.0), (63.0, 24.3), (63.5, 13.05), (64.0, 20.2), (64.5, 11.13), (65.0, 22.55), (65.5, 23.62), (66.0, 18.5), (66.5, 17.85), (67.0, 20.46), (67.5, 20.2), (68.0, 18.85), (68.5, 19.5), (69.0, 20.17), (69.5, 14.6), (70.0, 17.1), (70.5, 17.6), (71.0, 16.82), (71.5, 16.2), (72.0, 15.8), (72.5, 16.1), (73.0, 12.55), (73.5, 12.75), (74.0, 14.1), (74.5, 12.29), (75.0, 11.2), (75.5, 10.51), (76.0, 10.8), (76.5, 11.5), (77.0, 11.0), (77.5, 9.25), (78.0, 8.65), (78.5, 9.0), (79.0, 7.55), (79.5, 8.55), (80.0, 6.43), (80.5, 6.78), (81.0, 5.9), (81.5, 5.8), (82.0, 5.35), (82.5, 5.3), (83.0, 3.6), (83.5, 4.0), (84.0, 3.1), (84.5, 3.75), (85.0, 1.75), (85.5, 1.45), (86.0, 1.2), (86.5, 1.04), (87.0, 0.73), (87.5, 0.68), (88.0, 0.48), (88.5, 0.44), (89.0, 0.31), (89.5, 0.31), (90.0, 0.21), (90.5, 0.24), (91.0, 0.21), (91.5, 0.17), (92.0, 0.15), (92.5, 0.13), (93.0, 0.19), (93.5, 0.13), (94.0, 0.17), (94.5, 0.24), (95.0, 0.08), (95.5, 0.22), (96.0, 0.36), (96.5, 0.32), (97.0, 0.06), (97.5, 0.06), (98.0, 0.07), (98.5, 0.07), (99.0, 0.06), (99.5, 0.1), (100.0, 0.03), (101.0, 0.12), (102.0, 0.08), (103.0, 0.06), (104.0, 0.96), (105.0, 0.13), (106.0, 0.04), (107.0, 0.05), (108.0, 0.03), (109.0, 0.05), (110.0, 0.03), (111.0, 0.02), (112.0, 0.19), (113.0, 0.01), (114.0, 0.01), (115.0, 0.03), (116.0, 0.01), (117.0, 0.02), (118.0, 0.05), (119.0, 0.03), (120.0, 0.01), (121.0, 0.08), (122.0, 0.2), (123.0, 0.25), (124.0, 0.02), (125.0, 0.01)], ['CALL MA January 23', (82.0, 6.15), (83.0, 5.32), (84.0, 3.8), (85.0, 4.0), (86.0, 2.16), (87.0, 1.64), (88.0, 0.81), (89.0, 0.61), (90.0, 0.8), (92.0, 0.5), (93.0, 0.27), (94.0, 0.25), (95.0, 0.17)], ['CALL MA January 30', (76.0, 11.03), (80.0, 7.45), (82.0, 6.6), (84.0, 4.6), (85.0, 3.6), (86.0, 2.42), (87.0, 1.44), (88.0, 1.12), (89.0, 0.85), (90.0, 0.64), (91.0, 0.49), (92.0, 0.97), (93.0, 0.6), (95.0, 0.38), (98.0, 0.31)], ['CALL NTES January 2'], ['CALL NTES January 9'], ['CALL NTES January 17', (19.0, 71.25), (29.0, 42.2), (39.0, 26.9), (40.0, 34.91), (44.0, 31.87), (45.0, 28.55), (49.0, 51.62), (50.0, 54.0), (51.5, 28.4), (52.5, 22.76), (54.0, 47.0), (55.0, 16.4), (57.5, 32.7), (59.0, 25.5), (60.0, 23.9), (62.5, 22.5), (64.0, 40.2), (65.0, 18.3), (67.5, 19.59), (69.0, 15.2), (70.0, 19.37), (72.5, 29.0), (74.0, 24.0), (75.0, 24.02), (77.5, 23.23), (79.0, 25.5), (80.0, 25.5), (82.5, 12.1), (85.0, 15.9), (87.5, 13.73), (90.0, 11.3), (92.5, 8.9), (95.0, 5.46), (97.5, 2.85), (100.0, 1.8), (105.0, 0.7), (110.0, 0.22), (115.0, 0.25), (120.0, 0.1), (125.0, 0.05)], ['CALL NTES January 23'], ['CALL NTES January 30'], ['CALL NFLX January 2', (280.0, 62.2), (295.0, 33.05), (300.0, 31.6), (305.0, 30.65), (310.0, 30.76), (312.5, 32.29), (315.0, 23.17), (320.0, 21.32), (325.0, 16.4), (327.5, 16.2), (330.0, 17.65), (332.5, 15.97), (335.0, 13.0), (337.5, 10.6), (340.0, 8.2), (342.5, 5.5), (345.0, 3.4), (347.5, 1.63), (350.0, 0.6), (352.5, 0.17), (355.0, 0.11), (357.5, 0.08), (360.0, 0.03), (362.5, 0.03), (365.0, 0.04), (367.5, 0.06), (370.0, 0.06), (372.5, 0.02), (375.0, 0.04), (377.5, 0.02), (380.0, 0.01), (382.5, 0.22), (385.0, 0.01), (387.5, 0.3), (390.0, 0.01), (392.5, 0.15), (395.0, 0.05), (397.5, 0.05), (400.0, 0.02), (402.5, 0.09), (405.0, 0.08), (407.5, 6.85), (410.0, 0.11), (412.5, 0.29), (415.0, 0.01), (417.5, 4.02), (420.0, 0.19), (425.0, 0.34), (430.0, 0.52), (435.0, 1.2), (440.0, 0.01), (445.0, 0.64), (450.0, 0.57), (455.0, 0.22)], ['CALL NFLX January 9', (270.0, 76.6), (290.0, 50.54), (300.0, 40.88), (310.0, 32.05), (320.0, 22.8), (322.5, 11.8), (325.0, 21.15), (327.5, 16.4), (330.0, 17.65), (332.5, 11.75), (335.0, 16.0), (337.5, 11.3), (340.0, 10.51), (342.5, 7.8), (345.0, 7.3), (347.5, 5.9), (350.0, 4.5), (352.5, 2.9), (355.0, 2.6), (357.5, 1.89), (360.0, 1.45), (362.5, 1.05), (365.0, 0.77), (367.5, 0.4), (370.0, 0.25), (372.5, 0.28), (375.0, 0.19), (377.5, 0.13), (380.0, 0.09), (382.5, 0.06), (385.0, 0.12), (387.5, 0.3), (390.0, 0.05), (392.5, 0.2), (395.0, 1.28), (400.0, 0.17), (405.0, 1.0), (410.0, 0.15), (430.0, 0.18)], ['CALL NFLX January 17', (45.0, 313.39), (47.5, 297.35), (50.0, 291.5), (55.0, 282.65), (60.0, 324.6), (65.0, 246.8), (70.0, 356.53), (72.5, 272.55), (75.0, 275.7), (77.5, 308.9), (80.0, 278.4), (82.5, 276.05), (85.0, 301.4), (87.5, 315.95), (90.0, 392.8), (92.5, 315.7), (95.0, 387.8), (97.5, 285.7), (100.0, 268.76), (105.0, 303.71), (110.0, 212.93), (115.0, 290.3), (120.0, 258.5), (125.0, 282.93), (130.0, 294.7), (135.0, 301.83), (140.0, 219.25), (145.0, 197.0), (150.0, 186.6), (155.0, 202.9), (160.0, 208.9), (165.0, 320.33), (170.0, 172.7), (175.0, 142.0), (180.0, 202.79), (185.0, 146.85), (190.0, 187.0), (195.0, 123.95), (200.0, 117.37), (205.0, 181.47), (210.0, 262.81), (215.0, 145.36), (220.0, 104.79), (225.0, 106.5), (230.0, 132.45), (235.0, 102.13), (240.0, 103.5), (245.0, 99.2), (250.0, 92.54), (255.0, 223.0), (260.0, 82.59), (265.0, 126.75), (270.0, 75.2), (275.0, 69.0), (280.0, 61.3), (285.0, 47.65), (290.0, 52.0), (295.0, 44.5), (300.0, 43.85), (302.5, 40.05), (305.0, 41.0), (307.5, 37.15), (310.0, 32.55), (312.5, 30.75), (315.0, 30.95), (317.5, 27.35), (320.0, 29.28), (322.5, 22.65), (325.0, 20.3), (327.5, 18.8), (330.0, 20.14), (332.5, 15.55), (335.0, 15.8), (337.5, 14.2), (340.0, 13.0), (342.5, 11.05), (345.0, 9.5), (347.5, 8.25), (350.0, 6.9), (352.5, 5.21), (355.0, 4.85), (357.5, 3.85), (360.0, 3.2), (362.5, 1.46), (365.0, 2.15), (367.5, 1.47), (370.0, 1.4), (372.5, 1.15), (375.0, 0.74), (377.5, 0.7), (380.0, 0.52), (382.5, 0.41), (385.0, 0.38), (387.5, 0.31), (390.0, 0.27), (392.5, 0.43), (395.0, 0.08), (397.5, 0.18), (400.0, 0.18), (402.5, 0.24), (405.0, 2.43), (407.5, 0.19), (410.0, 0.12), (415.0, 0.14), (417.5, 0.29), (420.0, 0.06), (425.0, 0.14), (430.0, 0.12), (435.0, 0.09), (440.0, 0.02), (445.0, 0.03), (450.0, 0.05), (455.0, 0.01), (460.0, 0.02), (465.0, 0.01), (470.0, 0.05), (475.0, 0.12), (480.0, 0.01), (485.0, 0.01), (490.0, 0.01), (495.0, 0.44), (500.0, 0.01), (505.0, 0.2), (510.0, 0.05), (515.0, 0.54), (520.0, 0.05), (525.0, 0.01), (530.0, 0.08), (535.0, 0.2), (540.0, 0.02), (545.0, 0.01), (550.0, 0.01), (555.0, 0.11), (560.0, 0.4), (565.0, 0.29), (570.0, 0.08), (575.0, 0.3), (580.0, 1.63), (585.0, 0.36), (590.0, 1.15), (595.0, 1.03), (600.0, 0.01), (605.0, 0.77), (610.0, 0.18), (615.0, 0.2), (620.0, 0.17), (625.0, 0.4), (630.0, 0.45), (635.0, 2.32), (640.0, 0.11), (645.0, 1.99), (650.0, 0.08), (655.0, 0.01), (660.0, 0.15), (665.0, 0.01), (670.0, 0.01), (675.0, 0.19), (680.0, 0.2), (685.0, 0.15), (690.0, 0.25), (695.0, 0.35), (700.0, 0.05), (705.0, 0.19), (710.0, 0.61), (715.0, 2.48), (720.0, 1.45), (725.0, 0.15), (730.0, 2.16), (735.0, 0.45), (740.0, 0.4), (745.0, 0.3), (750.0, 0.05), (755.0, 0.01), (760.0, 1.45), (765.0, 0.01), (770.0, 0.01), (775.0, 0.21), (780.0, 0.07), (785.0, 2.42), (790.0, 0.05), (800.0, 0.01), (805.0, 0.25), (810.0, 0.15), (815.0, 0.05), (825.0, 0.1), (830.0, 0.33), (835.0, 0.01), (840.0, 2.7), (845.0, 0.4), (850.0, 0.14), (855.0, 0.28), (860.0, 0.1)], ['CALL NFLX January 23', (250.0, 97.5), (270.0, 60.0), (280.0, 52.34), (295.0, 52.35), (300.0, 50.1), (310.0, 42.0), (317.5, 37.6), (320.0, 20.57), (325.0, 30.8), (327.5, 22.05), (330.0, 26.45), (335.0, 23.35), (337.5, 23.15), (340.0, 24.58), (342.5, 20.39), (345.0, 20.1), (347.5, 19.06), (350.0, 18.65), (352.5, 16.68), (355.0, 14.6), (357.5, 13.75), (360.0, 11.5), (362.5, 13.4), (365.0, 12.5), (367.5, 10.5), (370.0, 9.45), (372.5, 9.6), (375.0, 8.83), (377.5, 8.0), (380.0, 7.27), (382.5, 5.5), (385.0, 6.18), (390.0, 4.36), (395.0, 4.44), (400.0, 3.2), (405.0, 2.38), (410.0, 2.0), (420.0, 1.46), (440.0, 1.6), (450.0, 0.44), (455.0, 0.7)], ['CALL NFLX January 30', (265.0, 71.2), (270.0, 72.75), (275.0, 68.3), (280.0, 66.8), (285.0, 59.75), (300.0, 51.8), (302.5, 31.65), (312.5, 25.95), (315.0, 38.33), (325.0, 26.57), (327.5, 29.8), (330.0, 29.65), (335.0, 23.41), (337.5, 19.65), (340.0, 22.65), (342.5, 21.0), (345.0, 20.05), (347.5, 18.95), (350.0, 20.31), (352.5, 15.8), (355.0, 16.2), (360.0, 14.25), (362.5, 12.5), (365.0, 12.01), (367.5, 9.6), (370.0, 11.3), (372.5, 9.33), (375.0, 9.79), (380.0, 8.55), (385.0, 5.9), (390.0, 6.0), (395.0, 4.85), (400.0, 3.6), (405.0, 3.23), (410.0, 2.62), (415.0, 2.45), (425.0, 1.36), (440.0, 1.35), (445.0, 0.7), (450.0, 0.59)], ['CALL RL January 2'], ['CALL RL January 9'], ['CALL RL January 17', (80.0, 83.5), (90.0, 79.7), (95.0, 85.1), (100.0, 69.9), (110.0, 50.1), (115.0, 47.7), (120.0, 38.4), (125.0, 48.5), (130.0, 49.84), (135.0, 45.0), (140.0, 40.0), (145.0, 35.0), (150.0, 36.0), (155.0, 24.7), (160.0, 22.9), (165.0, 20.5), (170.0, 17.0), (175.0, 11.0), (180.0, 5.2), (185.0, 1.95), (190.0, 0.7), (195.0, 0.6), (200.0, 0.17), (210.0, 0.1), (220.0, 0.25), (230.0, 0.15), (240.0, 0.54), (250.0, 0.05), (260.0, 1.4), (270.0, 0.11)], ['CALL RL January 23'], ['CALL RL January 30'], ['CALL WYNN January 2', (125.0, 24.85), (130.0, 8.8), (135.0, 15.3), (140.0, 9.3), (143.0, 5.45), (144.0, 5.2), (145.0, 0.3), (146.0, 0.35), (147.0, 3.0), (148.0, 0.28), (149.0, 1.15), (150.0, 0.07), (152.5, 0.07), (155.0, 0.03), (157.5, 0.05), (160.0, 0.01), (162.5, 0.24), (165.0, 0.22), (167.5, 0.14), (170.0, 0.08), (172.5, 0.05), (175.0, 0.22), (177.5, 1.69), (180.0, 0.05), (182.5, 0.82), (185.0, 0.05), (187.5, 0.35), (190.0, 0.04), (192.5, 0.46), (195.0, 1.15)], ['CALL WYNN January 9', (120.0, 15.1), (130.0, 13.25), (135.0, 18.4), (140.0, 4.95), (143.0, 9.0), (144.0, 8.9), (145.0, 2.55), (146.0, 8.6), (147.0, 4.7), (148.0, 1.41), (149.0, 3.55), (150.0, 0.94), (152.5, 0.49), (155.0, 0.35), (157.5, 0.24), (160.0, 0.27), (162.5, 0.36), (165.0, 0.01), (167.5, 0.56), (170.0, 0.15), (172.5, 1.99), (175.0, 0.91), (177.5, 0.6), (180.0, 0.46), (182.5, 0.83), (187.5, 0.48)], ['CALL WYNN January 17', (51.0, 150.65), (52.0, 150.65), (56.0, 138.0), (57.0, 138.0), (61.0, 160.11), (62.0, 160.11), (66.0, 59.75), (67.0, 59.75), (71.0, 58.5), (72.0, 58.5), (76.0, 119.9), (77.0, 119.9), (81.0, 39.75), (82.0, 39.75), (86.0, 115.5), (87.0, 115.5), (91.0, 71.27), (92.0, 71.27), (94.0, 104.95), (95.0, 104.95), (96.0, 125.5), (97.0, 125.5), (99.0, 78.5), (100.0, 78.7), (101.0, 76.65), (102.0, 76.65), (104.0, 72.07), (105.0, 72.07), (106.0, 37.67), (107.0, 71.59), (109.0, 58.41), (110.0, 38.5), (111.0, 86.0), (112.0, 86.0), (116.0, 21.11), (117.0, 61.63), (120.0, 20.45), (121.0, 56.55), (122.0, 56.55), (124.0, 16.05), (125.0, 15.2), (126.0, 70.0), (127.0, 70.0), (129.0, 20.35), (130.0, 20.15), (131.0, 18.55), (132.0, 46.8), (134.0, 19.06), (135.0, 19.75), (136.0, 17.1), (137.0, 12.1), (139.0, 11.7), (140.0, 5.95), (141.0, 12.46), (142.0, 11.75), (144.0, 3.4), (145.0, 3.8), (146.0, 6.0), (147.0, 5.15), (148.0, 3.69), (149.0, 1.73), (150.0, 1.71), (151.0, 1.55), (151.5, 1.41), (152.0, 37.0), (152.5, 1.13), (154.0, 0.85), (155.0, 0.71), (156.0, 0.54), (156.5, 2.12), (157.0, 30.3), (157.5, 0.5), (159.0, 0.49), (160.0, 0.3), (161.0, 0.25), (162.0, 18.15), (162.5, 0.27), (164.0, 0.15), (165.0, 0.52), (166.0, 0.42), (166.5, 0.52), (167.0, 15.0), (169.0, 0.16), (170.0, 0.22), (171.0, 0.07), (172.0, 11.4), (174.0, 0.11), (175.0, 0.15), (176.0, 0.24), (177.0, 8.26), (179.0, 0.01), (180.0, 0.06), (181.0, 0.05), (182.0, 6.15), (184.0, 0.06), (185.0, 0.1), (186.0, 0.03), (187.0, 4.65), (189.0, 0.01), (190.0, 0.1), (191.0, 0.05), (192.0, 3.0), (194.0, 0.01), (195.0, 0.1), (196.0, 0.31), (197.0, 2.0), (199.0, 0.02), (200.0, 0.03), (204.0, 0.07), (205.0, 0.03), (206.0, 0.04), (207.0, 0.73), (209.0, 0.03), (210.0, 0.01), (214.0, 0.01), (215.0, 0.17), (216.0, 0.01), (217.0, 0.35), (219.0, 0.08), (220.0, 0.32), (224.0, 0.06), (225.0, 0.21), (226.0, 0.47), (227.0, 0.47), (229.0, 0.01), (230.0, 0.29), (234.0, 0.03), (235.0, 0.06), (236.0, 0.01), (237.0, 0.19), (239.0, 0.01), (240.0, 0.13), (244.0, 0.05), (245.0, 0.05), (246.0, 0.09), (247.0, 0.25), (249.0, 0.02), (250.0, 0.05), (254.0, 0.1), (255.0, 0.1), (259.0, 0.01), (260.0, 0.02), (264.0, 0.01), (265.0, 1.27), (269.0, 0.01), (270.0, 0.04), (274.0, 0.85), (275.0, 0.85), (279.0, 0.03), (280.0, 0.73), (284.0, 0.99), (285.0, 0.99), (289.0, 0.05), (290.0, 0.05), (299.0, 0.02), (300.0, 0.02), (309.0, 0.02), (310.0, 0.02), (319.0, 0.32), (320.0, 0.32), (329.0, 0.03), (330.0, 0.04), (339.0, 0.05), (340.0, 0.05), (349.0, 0.04), (350.0, 0.04), (359.0, 0.02), (360.0, 0.02), (369.0, 0.01), (370.0, 0.03)], ['CALL WYNN January 23', (135.0, 7.25), (138.0, 6.0), (139.0, 13.68), (144.0, 5.5), (146.0, 6.6), (147.0, 3.15), (148.0, 7.37), (149.0, 2.46), (150.0, 2.18), (152.5, 5.3), (155.0, 4.0), (157.5, 2.85), (160.0, 0.5), (162.5, 1.1), (165.0, 1.0), (167.5, 0.85), (170.0, 1.06), (172.5, 0.15), (177.5, 0.9), (180.0, 1.2), (185.0, 0.41)], ['CALL WYNN January 30', (135.0, 12.9), (136.0, 12.8), (138.0, 10.13), (142.0, 8.2), (145.0, 6.75), (147.0, 3.05), (148.0, 3.5), (149.0, 3.72), (150.0, 5.0), (152.5, 3.05), (155.0, 4.0), (160.0, 2.08), (162.5, 2.11), (165.0, 1.29), (167.5, 1.16), (170.0, 0.79), (172.5, 0.72)]]
	call = random.choice(calls)
	print "Selected stock and date", call[0]
	combos = call[1:]
	option_type = "call"
	if option_type == "put":
		K1 = 105
		P1 = 8
		T1 = 1
		K2 = 125
		P2 = 27
		T2 = 1
		PutSpread(K1, P1*100, T1, K2, P2*100, T2, S0)
	elif option_type == "call":
		if bullCall:
			# Bull Call spread
			option1 = random.choice(combos)
			while math.fabs(S0-option1[0]) > 2:
				option1 = random.choice(combos)
			option2 = random.choice(combos)
			while option2[0] < S0+5:
				option2 = random.choice(combos)
		else:
			# Bear Call Spread
			option1 = random.choice(combos)
			while option1[0] < S0:
				option1 = random.choice(combos)
			option2 = random.choice(combos)
			while option2[0] > S0:
				option2 = random.choice(combos)
		print option1
		print option2
		K1 = int(option1[0])
		P1 = option1[1]
		T1 = 1
		K2 = int(option2[0])
		P2 = option2[1]
		T2 = 1
		CallSpread(K1, P1*100, T1, K2, P2*100, T2, S0)
	else:
		# Butterfly Call spread
		option1 = 0
		option3 = 0
		while option1 == 0 or option3 == 0:
			option1 = 0
			option3 = 0
			a = random.randint(5,15)
			option2 = random.choice(combos)
			while math.fabs(S0-option2[0]) > 1:
					option2 = random.choice(combos)
			for combo in combos:
				if combo[0] == option2[0] - a:
					option1 = combo
				elif combo[0] == option2[0] + a:
					option3 = combo
					break
		print option1, option2, option3
		K1 = int(option1[0])
		P1 = option1[1]
		T1 = 1
		K2 = int(option2[0])
		P2 = option2[1]
		T2 = 1
		K3 = int(option3[0])
		P3 = option3[1]
		T3 = 1
		butterflySpread(K1, P1*100, T1, K2, P2*100, T2, K3, P3*100, T3, S0)






