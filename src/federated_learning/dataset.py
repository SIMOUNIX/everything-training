from torchvision import datasets, transforms

from torch.utils.data import random_split
from torch.utils.data.dataloader import DataLoader


# mnist transform
def mnist_transform():
    return transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )


def pull_mnist_dataset() -> tuple[datasets.MNIST, datasets.MNIST]:
    # import mnist dataset
    dataset = datasets.MNIST(
        root="~/data", train=True, download=True, transform=mnist_transform()
    )
    test_dataset = datasets.MNIST(
        root="~/data", train=False, download=True, transform=mnist_transform()
    )

    return dataset, test_dataset


def get_dataset(nb_clients: int) -> tuple[list[DataLoader], DataLoader]:
    dataset, test_dataset = pull_mnist_dataset()

    # split dataset
    train_sizes = [int(len(dataset) * 0.8 // nb_clients)] * nb_clients
    val_size = int(len(dataset) - sum(train_sizes))

    print(f"Train sizes: {train_sizes}")
    print(f"Validation size: {val_size}")

    splited_datasets = random_split(dataset, train_sizes + [val_size])

    # last dataset is the validation dataset
    train_datasets = splited_datasets[:-1]
    val_dataset = splited_datasets[-1]

    # create dataloaders
    train_loaders = [
        DataLoader(train_dataset, batch_size=64, shuffle=True)
        for train_dataset in train_datasets
    ]
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)

    return train_loaders, val_loader
