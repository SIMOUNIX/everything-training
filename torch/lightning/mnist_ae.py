# train a basic autoencoder on MNIST using torch lightnin
# only testing purposes

import logging

import lightning as L
from torchvision import transforms
from torchvision.datasets import MNIST

import torch
from torch import nn
from torch.utils.data import DataLoader


# the input dimension is 28*28 = 784
# image from mnist are 28x28 (in our case)
# the hidden dimension can be anything
# the latent dimension is the dimension of the bottleneck
class Encoder(nn.Module):
    def __init__(self, input_dim, hidden_dim, latent_dim):
        super().__init__()
        self.l1 = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, latent_dim),
        )

    def forward(self, x):
        # just return the forward pass
        return self.l1(x)


# the input dimension is the latent dimension
class Decoder(nn.Module):
    def __init__(self, latent_dim, hidden_dim, output_dim):
        super().__init__()
        self.l1 = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x):
        # return the forward pass
        return self.l1(x)


class LightningAE(L.LightningModule):
    def __init__(self, encoder, decoder, loss, optimizer):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.loss = loss
        self.optimizer = optimizer

    # training step function from the lightning module
    # we simply override it to match our needs
    def training_step(self, batch, batch_idx):
        x, _ = batch  # get the input data, we do not need the labels
        x = x.view(x.size(0), -1)  # flatten the input data
        z = self.encoder(x)
        x_hat = self.decoder(z)
        loss = self.loss(x_hat, x)
        return loss

    # configure the optimizer
    def configure_optimizers(self):
        if self.optimizer == "adam":
            optimizer = torch.optim.Adam(params=self.parameters(), lr=1e-3)
        else:
            optimizer = torch.optim.SGD(params=self.parameters(), lr=1e-3)
        return optimizer


# the main function
def main():
    logging.log(level=logging.INFO, msg="Downloading the MNIST dataset")
    # get the train_data and test_data
    train_data = MNIST(
        root="/data", train=True, download=True, transform=transforms.ToTensor()
    )
    test_data = MNIST(
        root=".", train=False, download=True, transform=transforms.ToTensor()
    )

    # data loaders
    train_loader = DataLoader(train_data, batch_size=32, num_workers=7)
    test_loader = DataLoader(test_data, batch_size=32, num_workers=7)

    # hyperparameters
    input_dim = 28 * 28  # from the mnist dataset
    hidden_dim = 128
    latent_dim = 32
    output_dim = 28 * 28

    # model
    encoder = Encoder(input_dim, hidden_dim, latent_dim)
    decoder = Decoder(latent_dim, hidden_dim, output_dim)
    loss = nn.MSELoss()

    # lightning model
    model = LightningAE(encoder, decoder, loss, "adam")

    # trainer
    trainer = L.Trainer(max_epochs=20)
    trainer.fit(
        model=model, train_dataloaders=train_loader, val_dataloaders=test_loader
    )


if __name__ == "__main__":
    main()
