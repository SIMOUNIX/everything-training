# Federated Learning

This folder contains the code for my own implementation of Federated Learning. The model uses the lightning framework and is trained on the MNIST dataset. Using lightning framework is purely optional, I only wanted to try it out.

## Installation

To install the required packages, run the following command:

1. Install uv on your machine by running the following command:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install the required packages:
```bash
uv sync && source ../../.venv/bin/activate
```

3. Start the training:
```bash
python train.py
```

## Results

The model is trained on the MNIST dataset and achieves a high accuracy depending on the number of clients and the number of epochs. Look for `global_model_accuracy.png` to visualize graphics of the model's training accuracy.
