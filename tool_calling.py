import ollama

inventory_db = {
    "laptop": {"stock": 6, "base_price": 12000},
    "monitor": {"stock": 0, "base_price": 3000},
    "keyboard": {"stock": 4, "base_price": 5000}
}

def check_inventory(product_name):
    product_name = product_name.lower()
    return inventory_db.get(product_name) if product_name in inventory_db else {"stock": 0, "base_price": None}

def calculate_loyality_discount(base_price, years_as_customer):
    discount = min(years_as_customer*0.05, 0.3)
    final_price = base_price*(1-discount)
    return round(final_price, 2)

available_functions = {
    "check_inventory": check_inventory,
    "calculate_loyality_discount": calculate_loyality_discount
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": "Get the price and available stock of a product",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"}
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_loyality_discount",
            "description": "Calculate final price for a customer, based on how many years he is a customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_price": {"type": "number"},
                    "years_as_customer": {"type": "integer"},
                },
                "required": ["base_price" ,"years_as_customer"]
            }
        }
    }
]

message = [
    {"role": "user", "content": "Hello, I am Rajat, I would like to buy a keyboard. Could you please check the price"}
]

response = ollama.chat(
    model="qwen3:8b",
    messages=message,
    tools=tools
)

# print(response)

tool_calls = response["message"].get("tool_calls")

if tool_calls:
    for tool_call in tool_calls:
        tool_name = tool_call["function"]["name"]
        tool_args = tool_call["function"]["arguments"]

        function_to_call = available_functions[tool_name]

        result = function_to_call(**tool_args)

        message.append(response["message"])

        message.append(
            {
                "role": "tool",
                "content": str(result)
            }
        )

final_response = ollama.chat(
    model="qwen3:8b",
    messages=message
)

print(final_response["message"]["content"])