import torch
import numpy as np
import math
import matplotlib.pyplot as plt
 
N = 1000

idx = np.array(range(N))
idx = np.random.permutation(idx)

# Create Tensors to hold input and outputs.
X = torch.linspace(-math.pi, math.pi, N, dtype=torch.float32).reshape(-1,1)
Y = (torch.sin(X)).reshape(-1,1)
Y = torch.tensor(Y, dtype=torch.float32)
X = X[idx]
Y = Y[idx]

class Model(torch.nn.Module):

    def __init__(self):
        super(Model, self).__init__()
        self.linear1 = torch.nn.Linear(1, 20, dtype=torch.float32)
        self.activation = torch.nn.Tanh()
        self.linear2 = torch.nn.Linear(20, 1, dtype=torch.float32)

    def forward(self, x):

        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        return x

model=Model()

learning_rate = 1e-2
loss_fn = torch.nn.MSELoss(reduction='sum')

optim = torch.optim.SGD(model.parameters(), lr=learning_rate)

for epoch in range(40):
    loss = 0
    for x,y in zip(X,Y):
        y_pred = model(x)
        loss = loss_fn(y_pred, y)
        optim.zero_grad()
        loss.backward()
        optim.step()

        loss += loss.item()
    print(f"loss: {loss/len(X):>7f}")

plt.plot(X,Y,'ko')

X = torch.linspace(-math.pi, math.pi, 500).reshape(-1,1)
Y=model(X)

plt.plot(X.detach().numpy(),Y.detach().numpy())
plt.show()

torch.save(model.state_dict(), 'sinx.pth')