import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from dotenv import load_dotenv
load_dotenv()

from helpers.helpers import load_config, hydrate_prompt, make_llm_call, setup_user_detail


class Tag(BaseModel):
    sketchpad: str = Field(description='140 character or less thought process for choosing tag')
    tag: Literal["emotional", "physical", "social", "spiritual", "professional", "personal", "financial"]

class Tags(BaseModel):
    tags: List[Tag] = Field(description='List of up to 4 tags that best represent the user\'s input.')


def write_html_tags(tags: List[str]):
    html_tags = ''
    for tag in tags:
        html_tags += f'<span style="background-color: #3b82f6; color: white; border-radius: 4px; margin: 0 2px; padding: 0 8px;">{tag}</span>'
    return html_tags


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

    if submit and user_input:
        response = make_llm_call(
            messages=[{"role": "user", "content": user_input}],
            system_prompt=system_prompt,
            response_model=Tags
        )
        response_tags = [tag.tag for tag in response.tags]
        st.markdown(write_html_tags(response_tags), unsafe_allow_html=True)
if __name__ == "__main__":
    main()


