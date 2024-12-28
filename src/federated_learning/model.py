from torch import optim, nn, Tensor
import lightning as L

class Model(L.LightningModule):
    def __init__(self, num_classes: int, input_channels: int, loss: nn.Module = nn.CrossEntropyLoss()) -> None:
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Conv2d(input_channels, 32, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64 * 5 * 5, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

        self.loss = loss

    def training_step(self, batch: Tensor, batch_idx: int) -> Tensor:
        x, y = batch
        logits = self.backbone(x)
        loss = self.loss(logits, y)
        # self.log('train_loss', loss) # log the loss to tensorboard (from the documentation of lightning)
        return loss

    def configure_optimizers(self) -> optim.Optimizer:
        return optim.Adam(self.parameters(), lr=1e-3)
