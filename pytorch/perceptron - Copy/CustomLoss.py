import torch
import torch.nn as nn

from constants import constants


class CustomLoss(nn.Module):
    def __init__(self, evaluations, evalWeight, regularWeight):
        super(CustomLoss, self).__init__()
        self.evaluations = evaluations
        self.evalWeight = evalWeight
        self.regularWeight = regularWeight

    def forward(self, predictions, targets):
        # Use BCELoss to calculate the loss
        reg = self.regularWeight * nn.BCELoss()(predictions, targets)

        evaluation = self.evalWeight * nn.BCELoss()(self.evaluations,
                                                    torch.ones(self.evaluations.size(0)).to(
                                                        constants.device))

        total = reg + evaluation

        return total
