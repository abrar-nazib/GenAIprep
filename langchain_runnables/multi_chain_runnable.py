import random
from abc import ABC, abstractmethod
import warnings


class Runnable(ABC):
    @abstractmethod
    def invoke(self, input_data):
        pass


class FakeLLM(Runnable):
    def __init__(self):
        print("LLM Created")

    def invoke(self, prompt):
        response_list = ["Response 1", "Response 2", "Response 3"]
        return {"response": f"{prompt} --- {random.choice(response_list)}"}

    def predict(self, prompt):
        warnings.warn(
            "predict() is deprecated; use invoke() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.invoke(prompt)


class FakePromptTemplate(Runnable):
    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables

    def invoke(self, input_data):
        if not isinstance(input_data, dict):
            if len(self.input_variables) != 1:
                raise TypeError("Multiple input variables require a dictionary")
            input_data = {self.input_variables[0]: input_data}

        return self.template.format(**input_data)

    def format(self, input_data):
        warnings.warn(
            "format() is deprecated; use invoke() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.invoke(input_data)


class FakeStrOutputParser(Runnable):
    def invoke(self, input_data: dict):
        return input_data.get("response", "")


class RunnableConnector(Runnable):
    def __init__(self, runnable_list):
        self.runnable_list = runnable_list

    def invoke(self, input_data):
        for runnable in self.runnable_list:
            input_data = runnable.invoke(input_data)
        return input_data


llm = FakeLLM()
template1 = FakePromptTemplate(
    template="Write a joke about {topic}.",
    input_variables=["topic"],
)
template2 = FakePromptTemplate(
    template="Explain the following joke\n{joke}",
    input_variables=["joke"],
)
parser = FakeStrOutputParser()

# The parser normalizes the first model's dictionary output to a string.
# A single-variable template can map that string to its sole input variable.
chain1 = RunnableConnector([template1, llm, parser])
chain2 = RunnableConnector([template2, llm, parser])
final_chain = RunnableConnector([chain1, chain2])
print(final_chain.invoke({"topic": "football"}))
