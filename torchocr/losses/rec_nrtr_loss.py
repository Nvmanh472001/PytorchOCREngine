import torch
from torch import nn
import torch.nn.functional as F


class NRTRLoss(nn.Module):
    def __init__(self, smoothing=True, ignore_index=0, **kwargs):
        super(NRTRLoss, self).__init__()
        if ignore_index >= 0 and not smoothing:
            self.loss_func = nn.CrossEntropyLoss(
                reduction='mean', ignore_index=ignore_index)
        self.smoothing = smoothing

    def forward(self, pred, batch):
        max_len = batch[2].max()
        tgt = batch[1][:, 1:2 + max_len]
        pred = pred.reshape([-1, pred.shape[2]])
        tgt = tgt.reshape([-1])
        if self.smoothing:
            eps = 0.1
            n_class = pred.shape[1]
            one_hot = F.one_hot(tgt.long(), num_classes=pred.shape[1])
            one_hot = one_hot * (1 - eps) + (1 - one_hot) * eps / (n_class - 1)
            log_prb = F.log_softmax(pred, dim=1)
            non_pad_mask = torch.not_equal(
                tgt, torch.zeros(
                    tgt.shape, dtype=tgt.dtype))
            loss = -(one_hot * log_prb).sum(dim=1)
            loss = loss.masked_select(non_pad_mask).mean()
        else:
            loss = self.loss_func(pred, tgt)
        return {'loss': loss}
