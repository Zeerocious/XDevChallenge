import asyncio
import xai_sdk
# import os
# os.environ['XAI_API_KEY'] = 'YOUR_KEY_GOES_HERE'


async def main():
    client = xai_sdk.Client()
    sampler = client.sampler

    FIRST_PREAMBLE = """\
This is a conversation between a human user and a highly intelligent AI. The AI's name is Grok and it makes every effort to truthfully answer a user's questions. It always responds politely but is not shy to use its vast knowledge in order to solve even the most difficult problems. The conversation begins.

Human: I want you to find the three main qualities or focus of these set of tweets.

Please format your answer as a valid JSON. For eg. if your qualities are (price, comfort, peaceful) your output should be.

{
    quality1: "price",
    quality2: "comfort",
    quality3: "peaceful"
}<|separator|>

Assistant: Understood! Please provide the list of tweets as a list of strings."""

    text = input("Write a message ")

    prompt = FIRST_PREAMBLE + f"<|separator|>\n\nHuman: {text}<|separator|>\n\nAssistant: " + "{\n"
    print(prompt)
    async for token in  sampler.sample(
        prompt=prompt,
        max_len=1024,
        stop_tokens=["<|separator|>"],
        temperature=0.5,
        nucleus_p=0.95):
        print(token.token_str, end="")
    print()

if __name__ == '__main__':
    asyncio.run(main())
