# Phi-3 Mini 128k Instruct Pyomo Code Generation

## Overview

This repository contains the code and resources used to fine-tune the `microsoft/Phi-3-mini-128k-instruct` model to specialize in generating Python code for Pyomo models. The goal is to create an AI assistant capable of generating complete Python code based on user input questions and provided code snippets. The fine-tuning was performed using QLoRA with 4-bit quantization. The resulting model is available at [wickes1/Phi-3-mini-128k-instruct-pyomo](https://huggingface.co/wickes1/Phi-3-mini-128k-instruct-pyomo).

## Dataset

The dataset used for training and evaluation was generated using GPT-4o.

This synthetic dataset was created using a 2-step generation process: first generating a list of questions, then generating the corresponding context Pyomo code and target Pyomo code. The dataset is structured as follows:

- **Train Dataset:** 72 examples
- **Eval Dataset:** 8 examples (10% split from training set)
- **Test Dataset:** 20 examples

Each example contains:

- `input`: The user question
- `context`: The existing Pyomo code
- `output`: The AI assistant's response

The dataset is hosted on Hugging Face and can be found here: [wickes1/pyomo-100](https://huggingface.co/datasets/wickes1/pyomo-100).

## Training

The fine-tuning process utilizes Quantized LoRA (QLoRA) for efficient memory usage and the final model is saved and evaluated based on metrics such as faithfulness, answer relevancy, and code quality.

- LoRA configuration with `r=8`, `lora_alpha=16`, and `lora_dropout=0.05`
- TrainingArguments with 3 epochs, a learning rate of 2e-4, and a batch size of 1
- Gradient checkpointing and accumulation for efficient memory usage

## Folder Structure

The project directory is organized as follows:

- `datasets/test`: Contains the test dataset.
- `datasets/train`: Contains the training and evaluation datasets.
- `checkpoints`: Stores the fine-tuned model checkpoints (`pyomo_adapter`).
- `merged_model`: Contains the PEFT model merged with the original Phi-3 model.

## Usage

To use the fine-tuned model for generating Pyomo code, follow these steps:

1. **Load the Model:**

    ```python
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_name = "wickes1/Phi-3-mini-128k-instruct-pyomo"
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    ```

2. **Generate Code:**

    ```python
    from transformers import TextStreamer

    input_text = "Add a constraint to ensure variable Q is at least 10."
    context_text = "from pyomo.environ import *\n\nmodel = ConcreteModel()\nmodel.Q = Var(domain=NonNegativeReals)\nmodel.obj = Objective(expr=2 * model.Q, sense=maximize)\n\n# Define constraints\nmodel.constraint1 = Constraint(expr=model.Q <= 8)\n\n# Solve the model\nsolver = SolverFactory('glpk')\nresult = solver.solve(model)"
    prompt = "<|system|>\nYou are a highly knowledgeable AI assistant specializing in Python programming and Pyomo models. Based on the user input question and the provided code snippet, your task is to generate the complete Python code needed to address the user's query.\n\nInstructions:\n1. Review the user input question carefully.\n2. Analyze the provided code snippet within the context given.\n3. Generate the full Python code required to answer the user's question, ensuring the code is functional and correctly formatted.\n\nNotes:\n- Ensure that the generated code is properly indented and follows Python best practices.\n- Include necessary import statements and any relevant comments to enhance code readability.\n- Verify that the code aligns with the user's specific requirements as described in the input and context.\n<|end|>\n<|user|>\nInput:\n{input}\n\nContext:\n{context}\n\nComplete Python Code:\n<|end|>\n<|assistant|>"

    # Tokenize input
    model_input = tokenizer(
        prompt.format(input=input_text, context=context_text), return_tensors="pt"
    ).to(device)

    text_streamer = TextStreamer(tokenizer, skip_prompt=True)
    _ = model.generate(
        model_input.input_ids,
        streamer=text_streamer,
        max_new_tokens=512,
    )
    ```

### Evaluation

The evaluation was performed using the Ragas framework, focusing on key metrics such as faithfulness and answer similarity. The evaluation was conducted with `gpt-4-32k` on the test dataset, which contains 20 samples.

| Metric            | Pretrained   | Fine-Tuned   |
| ----------------- | ------------ | ------------ |
| Faithfulness      | 0.6728300866 | 0.8494444444 |
| Answer Relevancy  | 0.624790472  | 0.5696892031 |
| Answer Similarity | 0.9494069926 | 0.9994273988 |
| Correctness       | 0.95         | 0.9          |
| Code Quality      | 0.95         | 0.9          |

### Troubleshooting and Comments

#### Phi-3 EOS Token

The EOS token in Phi-3 was found to be somewhat confusing:

- The model card suggests using `<|end|>` as the EOS token.
- In the `tokenizer_config.json`, `<|endoftext|>` was identified.
- The `generation_config.json` included `"eos_token_id": [32000, 32001, 32007]`, referring to `<|endoftext|>`,`<|assistant|>`, and `<|end|>` respectively.

Given these findings, `<|endoftext|>` was chosen as the EOS token for the final training prompt, while other parts of the prompt utilized `<|end|>`.

#### Evaluation with Ragas

- For this task, since the LLM functions as a code completion tool, the primary focus was on faithfulness and answer similarity.
- Initial evaluation with `gpt-35-turbo-16k` showed poorer performance for the fine-tuned model compared to the base model. Switching to `gpt-4-32k` yielded more reasonable evaluation scores.

#### ROCm Compatibility

- Life with ROCm is not easy. You shall not try on `poetry` for version control the dependencies, instead just use `pip` and often you have to build your own wheel.

## FAQ

**Q: What's the target for this fine-tune?**
A: The goal is to create a Language Model (LLM) that acts as a specialized agent or tool for tasks related to modifying Pyomo code. Based on user inputs regarding any type of modification to Pyomo code, the fine-tuned LLM in this repository should function effectively between question-answering and text completion, generating ready-to-use code based on the existing code.

**Q: Why Phi-3?**
A: There are several reasons for choosing Phi-3:

- Phi-3 is currently state-of-the-art among "small" parameter LLMs (<7B), and it's a popular choice.
- The latest update with 128K tokens further enhances its performance. Given that my prompt requires inputting the full code as context, long context handling significantly benefits the LLM's code generation performance in production.
- Phi-3 is based on the LLaMA family, which is known for being easy to fine-tune.
- With `4-bit` quantization, Phi-3 only requires ~2GB of VRAM to run in production.
- Comparative tests with models like `meta-llama/Llama-2-7b-chat-hf`, `meta-llama/Meta-Llama-3-8B-Instruct`, `codellama/CodeLlama-7b-hf`, and `microsoft/Phi-3-mini-4k-instruct` showed that Phi-3 with 3.8B parameters performs as well as 7B models for this task.
- Smaller models like Phi-3 offer lower training costs, faster inference, and less demanding hardware requirements.
- When merging the adapters back to the base model, I had to load Phi-3 in `float16`, which just fits within my 16GB AMD GPU.

**Q: How about Retrieval-Augmented Generation (RAG)?**
A: With the RAG approach, you can use an existing vector database like `pgvector` to store datasets similar to your current training data. When a user asks a question, you retrieve the `top_k` similar samples from the database and use them with few-shot prompting on your LLM. This method allows for the generation of more accurate and relevant code snippets.

The benefits of this approach include:

- Having an up-to-date database with the latest code snippets from your codebase.
- Eliminating the need to fine-tune the model, which allows you to switch to another model easily, including third-party models.
- Requiring only a good retrieval system and a well-crafted prompt to fit the pretrained model.

The downsides of this approach are:

- Increased token usage, leading to higher costs and slower inference.
- Potential complexity in model inference with a higher number of tokens.
- Limited to models with long context capabilities since few-shot prompting requires more tokens.

**Q: What's the next step?**
A:

- Utilize the fine-tuned model as a Pyomo code generation agent in any LLM framework, such as LangChain or LlamaIndex.
- Implement a RAG agent to retrieve code snippets from your internal codebase based on user input questions.
- Integrate a code runner agent to execute the generated code and report the results to the user.

**Q: How can I use this model in my project?**
A: You can load the fine-tuned model from the Hugging Face model repository (`wickes1/Phi-3-mini-128k-instruct-pyomo`) and integrate it into your existing Pyomo-based workflows or LLM frameworks. For LlamaIndex, you may use `HuggingFaceLLM`.

**Q: What kind of hardware do I need to run this model?**
A: Thanks to the `4-bit` quantization, the model can run on hardware with as little as 2GB of VRAM, making it accessible for use on consumer-grade GPUs.

**Q: How do I contribute to this project?**
A: Contributions are welcome! You can fork the repository, make your changes, and submit a pull request. Please ensure your code follows the repository's guidelines and includes appropriate tests.

**Q: Who can benefit from this fine-tuned model?**
A: This model is beneficial for developers and researchers working with Pyomo for optimization problems, especially those looking for automated code generation and modification based on user inputs.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you encounter any problems or have suggestions for improvements.

## Acknowledgments

Special thanks to the Hugging Face community for providing the tools and resources that made this project possible.
