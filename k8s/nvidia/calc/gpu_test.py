import torch, time

print("CUDA Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))
    print("Starting GPU computation...")
    a = torch.randn(10000, 10000, device='cuda')
    b = torch.randn(10000, 10000, device='cuda')
    c = torch.matmul(a, b)
    torch.cuda.synchronize()
    print("Matrix multiplication completed on GPU.")
else:
    print("No CUDA device detected.")
time.sleep(30)