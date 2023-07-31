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
        # Lets check all evaluations are between 0 and 1 if they are not show a warning
        # with the value of the evaluation
        if torch.any(self.evaluations < 0) or torch.any(self.evaluations > 1):
            print("Warning: Evaluation outside of bounds")
            print(self.evaluations)
            
        evaluation = self.evalWeight * nn.BCELoss()(self.evaluations,
                                                    torch.ones(self.evaluations.size(0)).to(
                                                        constants.device))

        total = reg + evaluation

        return total
