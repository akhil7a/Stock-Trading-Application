import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
lookup = [0.003621716499, 0.0033086180685, 0.004634446303333, 0.0046081125735, 0.00584614610672]
trade = [0.006194574833, 0.006037627697, 0.006707204755333, 0.006810895800591, 0.009016548156738]

lookup_doc = [0.004210524559, 0.004427136182785, 0.006327067375183, 0.006956152915955, 0.008504873752594]
trade_doc = [0.005142300129, 0.005289080476761, 0.009030936686198, 0.009507216215134, 0.011966516494751]
plt.figure(1)
plt.xlabel('No of clients')
plt.ylabel('Latency in sec')
plt.title('Lookup latency without docker')
plt.plot(x, lookup)

plt.figure(2)
plt.xlabel('No of clients')
plt.ylabel('Latency in sec')
plt.title('Trade latency without docker')
plt.plot(x, trade)

plt.figure(3)
plt.xlabel('No of clients')
plt.ylabel('Latency in sec')
plt.title('Lookup latency with docker')
plt.plot(x, lookup_doc)

plt.figure(4)
plt.xlabel('No of clients')
plt.ylabel('Latency in sec')
plt.title('Trade latency with docker')
plt.plot(x, trade_doc)

plt.xticks(x)
plt.show()