import torch
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('data.csv')
data.drop(columns=['Unnamed: 0'], inplace=True)
y = pd.DataFrame(data['price'])
data.drop(columns=['price'], inplace=True)
x = pd.DataFrame(data)

x_train = torch.tensor(x[:-500].values, dtype=torch.float)
y_train = torch.tensor(y[:-500].values, dtype=torch.float)
x_test = torch.tensor(x[-500:].values, dtype=torch.float)
y_test = torch.tensor(y[-500:].values, dtype=torch.float)

import torch
import torch.nn as nn
x = x - np.min(x) / (np.max(x) - np.min(x))

class Net(nn.Module):
    def __init__(self, D_in, H1, H2, H3, D_out):
        super(Net, self).__init__()

        self.linear1 = nn.Linear(D_in, H1)
        self.linear2 = nn.Linear(H1, H2)
        self.linear3 = nn.Linear(H2, H3)
        self.linear4 = nn.Linear(H3, D_out)

    def forward(self, x):
        y_pred = self.linear1(x).clamp(min=0)
        y_pred = self.linear2(y_pred).clamp(min=0)
        y_pred = self.linear3(y_pred).clamp(min=0)
        y_pred = self.linear4(y_pred)

        return y_pred




H1, H2, H3 = 30, 30, 30
criterion = nn.MSELoss()

D_in, D_out = x.shape[1], y.shape[1]
model = Net(D_in, H1, H2, H3, D_out)
optimizer = torch.optim.Adagrad(model.parameters(), lr=1e-3)
losses = []

for t in range(5000):
    y_pred = model(x_train)
    if not t % 100:
        print(t)
    loss = criterion(y_pred, y_train)
    losses.append(loss.item())

    if torch.isnan(loss):
        break

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

plt.figure(figsize=(12, 10))
plt.plot(range(len(losses[:])), losses[:], label='Error')
plt.legend(loc='upper right')
plt.show()

result = model(x_test)
result = pd.DataFrame(result.data.numpy(), columns=['price'])
result['price'].fillna(0)
test_y = pd.DataFrame(y_test, columns=['price'])
sum = 0
maxa = 0
mina = 100000
for i in range(500):
    temp = (abs(result['price'].iloc[i] - test_y['price'].iloc[i])/test_y['price'].iloc[i] * 100)
    sum += temp
    if temp < mina:
        mina = temp
    if temp > maxa:
        maxa = temp
print(sum/500, mina, maxa)

script_model = torch.jit.trace(model, torch.Tensor(2, ))
script_model.save("model.pt")
