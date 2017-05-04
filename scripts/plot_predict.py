import pickle
import matplotlib.pyplot as plt


with open ('mu_', 'rb') as fp:
	mu = pickle.load(fp)
with open ('sigma_', 'rb') as fp:
	sigma = pickle.load(fp)
with open ('true_target_', 'rb') as fp:
	target = pickle.load(fp)

plt.figure(1)

plt.subplot(211)
for i in range(0,len(mu)):
	#if testX[i] < 50:
	plt.subplot(211)
	plt.scatter(i,mu[i],color='black')
	plt.scatter(i,target[i],color='red')
	plt.subplot(212)
	error = abs(mu[i] - target[i])
	plt.errorbar(i, mu[i], error, linestyle='None', marker='^',ecolor='g')
plt.xlabel('Predict sample number')
plt.ylabel('Predicted reward (black) and True Reward')

plt.grid()
plt.show()
