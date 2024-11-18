import streamlit as st
from enum import Enum
from pydantic import BaseModel, Field, create_model
from typing import List, Optional, Literal
from dotenv import load_dotenv
load_dotenv()

from helpers.helpers import load_config, hydrate_prompt, make_llm_call, setup_user_detail


def write_html_tags(tags: List[str]):
    html_tags = ''
    for tag in tags:
        html_tags += f'<span style="background-color: #3b82f6; color: white; border-radius: 4px; margin: 0 2px; padding: 0 8px;">{tag}</span>'
    return html_tags


def create_enum(values: list):
    return Enum('TagEnum', {v.upper(): v for v in values})

def choose_tags() -> Enum:
    with open('tags.txt', 'r') as f:
        TAGS = [i.strip() for i in f.readlines()]
    tags = st.sidebar.text_input('Tag', placeholder='Enter tags, separated by commas')
    add_tag = st.sidebar.button('Add Tag')

    if add_tag:
        TAGS.extend([i.strip() for i in tags.split(',')])
    st.sidebar.write(TAGS)
    TAGS = list(set(TAGS))
    with open('tags.txt', 'w') as f:
        f.write('\n'.join(TAGS))
    return create_enum(TAGS)


def main():
    config = load_config("config.yml")
    system_prompt_template = config['config']['system_prompt_template']
    system_prompt = hydrate_prompt(
        system_prompt_template,
        tags=config['config']['tags'],
        user_detail=setup_user_detail(config['config']['user_detail'])
    )
    st.title('Tag Picker')
    user_input = st.text_area('User Input', height=200)

    submit = st.button('Submit')
    tag_enum = choose_tags()
    # print([i for i in tag_enum])
    # class TagEnum(Enum):
    #     __members__ = tag_enum.__members__
    
    Tag = create_model(
        'Tag',
        tag=(tag_enum, ...)  # (type, default_value)
    )
    
    Tags = create_model(
        'Tags',
        tags=(List[Tag], ...)  # (type, default_value)
    )

    if submit and user_input:
        response = make_llm_call(
            messages=[{"role": "user", "content": user_input}],
            system_prompt=system_prompt,
            response_model=Tags
        )
        print(response)
        response_tags = [tag.tag.value for tag in response.tags]
        st.markdown(write_html_tags(response_tags), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
