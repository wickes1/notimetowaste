<!-- /* cSpell:disable */ -->

# Huggingface Transformer Tutorial

> This tutorial using AMD ROCm(gfx1030) instead of CUDA

```bash
# Find latest version here: https://pytorch.org/
poetry install

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0
pip install peft evaluate
pip install accelerate -U
pip install trl tensorboard
pip install ragas

pip install llama-index llama-index-llms-huggingface llama-index-llms-huggingface-api
pip install llama-index-llms-ollama llama-index-embeddings-ollama
pip install llama-index-vector-stores-postgres

pip install 'arize-phoenix[evals]'

# poetry export --without-hashes --format=requirements.txt > requirements.txt
```

## Bitsandbytes ROCm

```bash
git clone --depth 1 -b multi-backend-refactor https://github.com/TimDettmers/bitsandbytes.git && cd bitsandbytes/
pip install -r requirements-dev.txt

cmake -DCOMPUTE_BACKEND=hip -DBNB_ROCM_ARCH="gfx1030" -S .
make

# back to current transformer-tutorial directory
pip install your/path/to/bitsandbytes
```

## Flash Attention ROCm

```bash
# NOT WORKING, hopefully they will support GFX1030 one day
git clone --recursive https://github.com/ROCmSoftwarePlatform/flash-attention.git
# export GPU_ARCHS="gfx1030"
pip install wheel
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

## Huggingface model to GGUF

```bash
MODEL_DIR=your/model/dir
cp $MODEL_DIR/tokenizer.json $MODEL_DIR/tokenizer.model
python convert_hf_to_gguf.py $MODEL_DIR --outfile output_file.gguf --outtype q8_0 --verbose
```
