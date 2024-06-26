from typing import Optional

from langchain.agents.mrkl import prompt

from dfapp.template.field.base import TemplateField
from dfapp.template.frontend_node.base import FrontendNode
from dfapp.template.frontend_node.constants import DEFAULT_PROMPT, HUMAN_PROMPT, SYSTEM_PROMPT
from dfapp.template.template.base import Template


class PromptFrontendNode(FrontendNode):
    @staticmethod
    def format_field(field: TemplateField, name: Optional[str] = None) -> None:
        FrontendNode.format_field(field, name)
        # if field.field_type  == "StringPromptTemplate"
        # change it to str
        PROMPT_FIELDS = [
            "template",
            "suffix",
            "prefix",
            "examples",
            "format_instructions",
        ]
        key = field.name or ""
        if field.field_type == "StringPromptTemplate" and "Message" in str(name):
            field.field_type = "prompt"
            field.multiline = True
            field.value = HUMAN_PROMPT if "Human" in key else SYSTEM_PROMPT
        if key == "template" and field.value == "":
            field.value = DEFAULT_PROMPT

        if key and key in PROMPT_FIELDS:
            field.field_type = "prompt"
            field.advanced = False

        if "Union" in field.field_type and "BaseMessagePromptTemplate" in field.field_type:
            field.field_type = "BaseMessagePromptTemplate"

        # All prompt fields should be password=False
        field.password = False
        field.dynamic = True


class PromptTemplateNode(FrontendNode):
    name: str = "PromptTemplate"
    template: Template
    description: str
    base_classes: list[str] = ["BasePromptTemplate"]

    @staticmethod
    def format_field(field: TemplateField, name: Optional[str] = None) -> None:
        FrontendNode.format_field(field, name)

        if (field.name or "") == "examples":
            field.advanced = False


class BasePromptFrontendNode(FrontendNode):
    name: str
    template: Template
    description: str
    base_classes: list[str]


class ZeroShotPromptNode(BasePromptFrontendNode):
    name: str = "ZeroShotPrompt"
    template: Template = Template(
        type_name="ZeroShotPrompt",
        fields=[
            TemplateField(
                field_type="str",
                required=False,
                placeholder="",
                is_list=False,
                show=True,
                multiline=True,
                value=prompt.PREFIX,
                name="prefix",
            ),
            TemplateField(
                field_type="str",
                required=True,
                placeholder="",
                is_list=False,
                show=True,
                multiline=True,
                value=prompt.FORMAT_INSTRUCTIONS,
                name="format_instructions",
            ),
            TemplateField(
                field_type="str",
                required=True,
                placeholder="",
                is_list=False,
                show=True,
                multiline=True,
                value=prompt.SUFFIX,
                name="suffix",
            ),
        ],
    )
    description: str = "Prompt template for Zero Shot Agent."
    base_classes: list[str] = ["BasePromptTemplate"]

    @staticmethod
    def format_field(field: TemplateField, name: Optional[str] = None) -> None:
        PromptFrontendNode.format_field(field, name)
