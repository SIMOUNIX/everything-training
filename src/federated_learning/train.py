from typing import Iterable, List

import lightning as L
import matplotlib.pyplot as plt
from torchvision import datasets, transforms

import torch
from model import Model
from torch import nn
from torch.utils.data import DataLoader, random_split

NB_CLIENTS = 2
NUM_ROUNDS = 5
NUM_EPOCHS = 5

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using {device} device')

# mnist transform
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# import mnist dataset
dataset = datasets.MNIST(root='~/data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='~/data', train=False, download=True, transform=transform)

# split dataset
train_sizes = [int(len(dataset) * 0.8 // NB_CLIENTS)] * NB_CLIENTS
val_size = int(len(dataset) - sum(train_sizes))

print(f'Train sizes: {train_sizes}')
print(f'Validation size: {val_size}')

splited_datasets = random_split(dataset, train_sizes + [val_size])

# last dataset is the validation dataset
train_datasets = splited_datasets[:-1]
val_dataset = splited_datasets[-1]

# create dataloaders
train_loaders = [DataLoader(train_dataset, batch_size=64, shuffle=True) for train_dataset in train_datasets]
val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)


def average_model_parameters(models: Iterable[nn.Module], avg_weights: list[float] = [1/2, 1/2]) -> dict:
    model_params = [model.state_dict() for model in models]
    avg_params = {}
    for k in model_params[0].keys():
        avg_params[k] = sum([model_params[i][k] * avg_weights[i] for i in range(len(model_params))])

    return avg_params

def update_model(model: nn.Module, new_params: dict):
    model.load_state_dict(new_params)

model = Model(num_classes=10, input_channels=1)

def evaluate(model: nn.Module, data_loader: DataLoader) -> float:
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for data, target in data_loader:
            data, target = data.to(device), target.to(device)
            outputs = model.backbone(data)
            _, predicted = torch.max(outputs, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
    return 100 * correct / total

# federated learning simulation
def federated_learning(
    num_rounds: int,
    train_loaders: List[DataLoader],
    val_loader: DataLoader,
    global_model: nn.Module,
    num_epochs: int,
    lr: float = 1e-3,
) -> List[float]:

    global_model.to(device)
    global_params = global_model.state_dict()
    local_models = [Model(num_classes=10, input_channels=1).to(device) for _ in train_loaders]

    global_accuracies = []

    for round_idx in range(num_rounds):
        print(f"Round {round_idx + 1}/{num_rounds}")

        # each client trains locally
        local_params = []
        for client_idx, train_loader in enumerate(train_loaders):
            local_model = local_models[client_idx]
            local_model.load_state_dict(global_params)
            trainer = L.Trainer(max_epochs=num_epochs)
            trainer.fit(local_model, train_dataloaders=train_loader)

            local_params.append(local_model.state_dict())

        # average parameters to update the global model
        avg_weights = [1 / NB_CLIENTS] * NB_CLIENTS # equal weights
        global_params = average_model_parameters(local_models, avg_weights)
        update_model(global_model, global_params)

        # evaluate the global model on the validation set
        global_accuracy = evaluate(global_model, val_loader)
        global_accuracies.append(global_accuracy)
        print(f"Global model accuracy after round {round_idx + 1}: {global_accuracy:.2f}%")

    return global_accuracies

global_model = Model(num_classes=10, input_channels=1)
global_accuracies = federated_learning(
    num_rounds=NUM_ROUNDS,
    train_loaders=train_loaders,
    val_loader=val_loader,
    global_model=global_model,
    num_epochs=NUM_EPOCHS,
)

# save the final plot
plt.plot(global_accuracies)
plt.xlabel('Round')
plt.ylabel('Accuracy (%)')
plt.title('Global model accuracy over rounds')
plt.savefig('global_model_accuracy.png')
