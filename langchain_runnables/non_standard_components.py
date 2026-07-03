import random


class FakeLLM:
    def __init__(self):
        print("LLM created")

    def predict(self, prompt):
        response_list = [
            "Response 1",
            "Response 2",
            "Response 3",
            "Response 4",
            "Response 5",
        ]
        return {"response": prompt + " --- " + random.choice(response_list)}


class FakePromptTemplate:
    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables

    def format(self, input_dict):
        return self.template.format(**input_dict)


class FakeLLMChain:
    def __init__(self, llm, template):
        self.llm: FakeLLM = llm
        self.template: FakePromptTemplate = template

    def run(self, input_dict):
        final_prompt = self.template.format(input_dict)
        result = self.llm.predict(final_prompt)
        return result["response"]


llm = FakeLLM()
template = FakePromptTemplate(
    template="Write a {length} poem about {topic}",
    input_variables=["topic", "length"],
)
chain = FakeLLMChain(llm, template)
print(chain.run({"length": "short", "topic": "football"}))
