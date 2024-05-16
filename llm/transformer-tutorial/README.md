# Huggingface Transformer Tutorial

> This tutorial using AMD ROCm instead of CUDA

```bash
# Find latest version here: https://pytorch.org/

# poetry resolve error
# poetry source add --priority=explicit pytorch-gpu-src https://download.pytorch.org/whl/rocm6.0
# poetry add --source pytorch-gpu-src torch torchvision torchaudio

poetry install

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0

```

## Import model from Huggingface to Ollama

```bash
pipx install huggingface-hub

huggingface-cli download  \
  microsoft/Phi-3-mini-4k-instruct-gguf \
  Phi-3-mini-4k-instruct-q4.gguf

ollama create phi3 -f Modelfile
ollama show phi3 --modelfile
ollama run phi3
```

```modelfile
FROM ./downloads/Phi-3-mini-4k-instruct-q4.gguf

TEMPLATE """<s>{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
{{ end }}<|assistant|>
{{ .Response }}<|end|>"""
PARAMETER stop <|endoftext|>
PARAMETER stop <|assistant|>
PARAMETER stop <|end|>
PARAMETER num_ctx 4096
```
