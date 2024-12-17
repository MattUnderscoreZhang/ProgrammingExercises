import torch


device = "mps"
a = torch.rand(3_000_000, 12).to(device) > 0.5
b = torch.rand(3_000_000, 12).to(device) > 0.5
c = torch.rand(3_000_000, 12).to(device) > 0.5
d = torch.rand(3_000_000, 12).to(device) > 0.5


blah = (a & b & c & d)
bloo = (a * b * c * d)


assert torch.all(blah == bloo)
breakpoint()
