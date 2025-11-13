from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "microsoft/phi-2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

prompt = """You are an estimator that predicts how many materials are needed based on project size.
Respond ONLY with a single valid JSON object. No explanations, no text, no markdown, no labels.

Examples:
Q: small shipyard
A: {"pumps": 50, "pipes": 100}

Q: big shipyard
A: {"pumps": 120, "pipes": 250}

Now estimate for a new project:
Q: medium shipyard
A:
"""

# Generar respuesta
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(
    **inputs,
    max_new_tokens=60,
    temperature=0.5,
    top_p=0.9,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)

respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(respuesta)