import os
import openai

# Morning page components:
# Tasks summary (ystersay and today)
# Journal summary (from?)
# Habits summary
# Weight and exercise and food?

API_KEY = ''
openai.organization = "org-W6nwVASQcVbcXRhmAMLdLRuL"

openai.api_key = API_KEY

model_engine = "gpt-3.5-turbo"
model_engine = "gpt-4"

response = openai.ChatCompletion.create(
    model=model_engine,
    messages=[
        {"role": "system", "content": "You are an assistant, a coach, an accountability partner."},
        {"role": "user", "content": """
Motivate me."""},
    ])

message = response.choices[0]['message']
print("{}: {}".format(message['role'], message['content']))
  
  



  