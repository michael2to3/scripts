```bash
python script.py \
    headers_input.txt \
    headers_output.txt \
    "You are a helpful assistant. Your task is to read the given header and respond with the proper output. For example, if the input is 'DOT', the output must be 'DOT: 1'; if the input is 'Transfer-Encoding', the output must be 'Transfer-Encoding: chunked'. For any unknown input, respond with '<header>: ???'."
```
