#!/usr/bin/env python3
import argparse
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--endpoint", default="http://localhost:8080/v1/chat/completions")
    parser.add_argument("--model", default="phi-3.5-mini-instruct")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max_tokens", type=int, default=256)
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as fin, open(args.output, "w", encoding="utf-8") as fout:
        for line in fin:
            header = line.strip()
            if not header:
                continue
            prompt_for_header = f"{args.prompt}\nInput: {header}\nOutput:"
            payload = {
                "model": args.model,
                "messages": [{"role": "user", "content": prompt_for_header}],
                "temperature": args.temperature,
                "max_tokens": args.max_tokens
            }
            response = requests.post(args.endpoint, json=payload)
            response_json = response.json()
            if "choices" in response_json and response_json["choices"]:
                model_answer = response_json["choices"][0]["message"]["content"]
            else:
                model_answer = "Error: No valid response from model."
            if args.verbose:
                print(model_answer.strip())
            fout.write(model_answer.strip() + "\n")

if __name__ == "__main__":
    main()
