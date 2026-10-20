import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def calculate(a: float, b: float, operation: str) -> float:
    """Execute a simple mathematical operation."""
    operations = {
        "add": lambda: a + b,
        "subtract": lambda: a - b,
        "multiply": lambda: a * b,
        "divide": lambda: a / b if b != 0 else (_ for _ in ()).throw(ValueError("Cannot divide by zero.")),
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    return operations[operation]()


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical operation using two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                    },
                },
                "required": ["a", "b", "operation"],
                "additionalProperties": False,
            },
        },
    }
]


def ask_llm(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        messages=messages,
        tools=TOOLS,
    )

    assistant_message = response.choices[0].message
    messages.append(assistant_message)

    if not assistant_message.tool_calls:
        return assistant_message.content or ""

    for tool_call in assistant_message.tool_calls:
        if tool_call.function.name != "calculate":
            raise ValueError(f"Unsupported tool: {tool_call.function.name}")

        arguments = json.loads(tool_call.function.arguments)
        result = calculate(**arguments)

        print(f"Tool call: calculate({arguments})")
        print(f"Tool result: {result}")

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            }
        )

    final_response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        messages=messages,
        tools=TOOLS,
    )

    return final_response.choices[0].message.content or ""


if __name__ == "__main__":
    question = input("Zadej otázku pro LLM: ")
    print("\nOdpověď:")
    print(ask_llm(question))
