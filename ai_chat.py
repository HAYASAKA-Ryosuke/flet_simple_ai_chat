from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer, TextIteratorStreamer
import asyncio
from threading import Thread


class AiChat:

    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained("cyberagent/calm2-7b-chat", device_map="auto", torch_dtype="auto")
        self.tokenizer = AutoTokenizer.from_pretrained("cyberagent/calm2-7b-chat")
        self.text_streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

    async def send(self, message: str) -> str:
        prompt = f"""USER: {message}
        ASSISTANT: """
        token_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        thread = Thread(
            target=self.model.generate,
            kwargs=dict(
                input_ids=token_ids.to(self.model.device),
                max_new_tokens=300,
                do_sample=True,
                temperature=0.8,
                streamer=self.text_streamer,
            )
        )
        thread.start()
        for output in self.text_streamer:
            if not output:
                continue
            await asyncio.sleep(0)
            print(output)
            yield output


async def main():
    ai_chat = AiChat()
    async for response in ai_chat.send('hello'):
        print(response)

if __name__ == '__main__':
    asyncio.run(main())
