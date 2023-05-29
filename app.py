import os
import openai

# Morning page components:
# Tasks summary (ystersay and today)
# Journal summary (from?)
# Habits summary
# Weight and exercise and food?


def get_apikey():
    try:
        with open('apikeys.txt', 'r') as f:
            for line in f.readlines():
                if line.startswith('openai'):
                    return line.split(':')[1].strip()
    except Exception as e:
        print(e)
        return None
    
def get_prompt_temporary():
    """
    This is a temporary function that fetches most of the prompt
    from the config file. This will obviously be way more sophisticated.
    """
    with open('config.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'prompt_start' in line:
                start_index = lines.index(line)
            if 'prompt_end' in line:
                end_index = lines.index(line)
    prompt = ''.join(lines[start_index+1:end_index])
    return prompt

API_KEY = get_apikey()
P = get_prompt_temporary()

openai.api_key = API_KEY

#model_engine = "gpt-3.5-turbo"
model_engine = "gpt-4"

response = openai.ChatCompletion.create(
    model=model_engine,
    messages=[
        {"role": "system", "content": "You are an assistant, a coach, an accountability partner."},
            {"role": "user", "content": P},
    ])

#BLA
message = response.choices[0]['message']
print("{}: {}".format(message['role'], message['content']))
  
  



  