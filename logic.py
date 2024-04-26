import google.generativeai as genai

import configure

def check(prompt, model):
  response = model.generate_content(prompt,
    generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=['x'],
        max_output_tokens=1000,
        temperature=0))
  #print(response._result)
  return response.text

def logic(prompt, model):
  response = model.generate_content(prompt,
    generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        #stop_sequences=['\n'],
        max_output_tokens=2048,
        temperature=0))
  print(response._result)
  return response.text

genai.configure(api_key=configure.API_KEY)

for m in genai.list_models():
  if 'GenerationConfig' in m.supported_generation_methods:
    print(m.name)

prompt1 = "give true if the below given prompt is code of any programming language else give false \n"

prompt ="""
#include <stdio.h>

int main() {

  int n, i, flag = 0;
  printf("Enter a positive integer: ");
  scanf("%d", &n);

  // 0 and 1 are not prime numbers
  // change flag to 1 for non-prime number
  if (n == 0 || n == 1)
    flag = 1;

  for (i = 2; i <= n / 2; ++i) {

    // if n is divisible by i, then n is not prime
    // change flag to 1 for non-prime number
    if (n % i == 0) {
      flag = 1;
      break;
    }
  }

  // flag is 0 for prime numbers
  if (flag == 0)
    printf("%d is a prime number.", n);
  else
    printf("%d is not a prime number.", n);

  return 0;
}
 """

model = genai.GenerativeModel('gemini-pro')

res = check(prompt1 + prompt, model)
if res == "true":
  # prompt2 = "give block by block EXPLANATION BRIEFLY in possible flow diagram for the following code which is necessary to understand the code\n"
  prompt2 = f"""I have a code snippet, and I'd like to understand its logic using the Gemini API.  To achieve this, I need your assistance in creating a well-structured prompt that effectively communicates the following requirements:

Functionality: Briefly explain what the code does and its overall purpose. (This will be a hyphen-_______ box in the flowchart)

Flowchart: Generate a flowchart using basic symbols (rectangles, diamonds, arrows) to represent the code's execution flow.  Here's the key point: Within the prompt, describe the meaning of each symbol directly beside the corresponding box in the flowchart using hyphen-_______ boxes.  For example:

    ┌───────────────┐     ┌───────────────┐
    | Functionality  | (Hyphen-_______ box) |
    └───────────────┘     └───────────────┘

                ↓ (arrow)

    ┌───────────────┐     ┌───────────────┐
    |  Rectangle     | (Process)          |  Diamond      | (Decision)
    | (Process name)  |                   | (Decision text) |
    └───────────────┘     └───────────────┘

                ↓ (arrow) based on decision

    ... (similar boxes for further steps) ...
Step-by-Step Explanation: Provide a clear and concise explanation of the code's execution sequence, outlining what happens at each stage.

Additional Considerations:

Maintain a clear and easy-to-understand tone.
Avoid overly technical jargon that might be difficult for non-programmers.
Focus on the core logic and functionality of the code.
By providing this information, I'll be able to formulate a comprehensive prompt for the Gemini API, ultimately leading to a better understanding of the code's logic through a flowchart and step-by-step explanation.\n"""
  print(logic(prompt2+prompt, model))
else:
  print("Enter a valid code")
