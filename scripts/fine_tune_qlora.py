from __future__ import annotations

import argparse


PROMPT_TEMPLATE = """Generate a SQLite SQL query for the user question.
Use only the provided schema. Return SQL only.

Schema:
{schema}

Question:
{question}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune CodeLlama with QLoRA for text-to-SQL.")
    parser.add_argument("--train", required=True)
    parser.add_argument("--eval", required=True)
    parser.add_argument("--base-model", default="codellama/CodeLlama-7b-Instruct-hf")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-seq-length", type=int, default=2048)
    parser.add_argument("--epochs", type=float, default=2.0)
    args = parser.parse_args()

    try:
        from datasets import load_dataset
        from peft import LoraConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
        from trl import SFTTrainer
    except ImportError as exc:
        raise SystemExit("Install ML dependencies with: pip install -e \".[ml]\"") from exc

    quantization = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype="bfloat16")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.base_model, quantization_config=quantization, device_map="auto")
    dataset = load_dataset("json", data_files={"train": args.train, "eval": args.eval})
    dataset = dataset.map(lambda row: {"text": format_example(row)})

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        learning_rate=2e-4,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=25,
        bf16=True,
        report_to="none",
    )
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset["eval"],
        peft_config=lora_config,
        args=training_args,
        dataset_text_field="text",
        max_seq_length=args.max_seq_length,
    )
    trainer.train()
    trainer.save_model(args.output_dir)


def format_example(row: dict) -> str:
    prompt = PROMPT_TEMPLATE.format(schema=row["schema"], question=row["question"])
    return f"{prompt}\n{row['sql']}"


if __name__ == "__main__":
    main()

