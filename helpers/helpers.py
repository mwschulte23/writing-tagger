import yaml
import anthropic
import instructor


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def hydrate_prompt(prompt: str, **kwargs) -> str:
    return prompt.format(**kwargs)


def setup_user_detail(user_detail: dict) -> str:
    return f'''
    User is 
    - {user_detail['age']} year old {user_detail['gender']}
    - works as an {user_detail['occupation']}
    - lives in {user_detail['location']}
    - is {user_detail['relationship']}
    - has {user_detail['kids']} kids
    - has {user_detail['pets']} pet
    - makes ${user_detail['income']: ,.0f} per year
    '''


def make_llm_call(messages, system_prompt, response_model, model='claude-3-5-sonnet-latest'):
    client = instructor.from_anthropic(anthropic.Anthropic())
    return client.chat.completions.create(
        model=model,
        response_model=response_model,
        max_tokens=8192,
        system=system_prompt,
        messages=messages
    )