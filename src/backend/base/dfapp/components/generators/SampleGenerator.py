from dfapp.base.models.model import LCModelComponent
from dfapp.field_typing import BaseLanguageModel
from datasets import DatasetDict, Dataset
from tqdm import tqdm
import random
import pandas as pd
import asyncio
from langdetect import detect

class SampleGeneratorComponent(LCModelComponent):
    display_name = "Sample Generator"
    description = "Generate a specified number of samples based on user input"

    def build_config(self):
        return {
            "System Prompt": {"display_name": "System Prompt", "multiline": True},
            "Question Column": {"display_name": "Question Column Name"},
            "Target Sample Count": {"display_name": "Target Sample Count"},
            "max_requests": {
                "display_name": "Max Requests per Minute",
                "advanced": True,
            },
            "max_attempts": {
                "display_name": "Max Attempts",
                "info": "Max retry attempts to make if api call fails",
                "advanced": True,
            }
        }

    def build(
        self,
        dataset: DatasetDict,
        model: BaseLanguageModel,
        question_column: str = "Sample",
        target_sample_count: int = 100,
        system_prompt: str = "",
        max_requests: int = 20,
        max_attempts: int = 3,
    ) -> DatasetDict:
        df = dataset["train"].to_pandas()
        seed_samples = list(df[question_column])
        data_instructions = []
        system_prompt = f"You are an advanced AI assistant. Extract keywords from the provided context and generate a sample using them. Output only, no additional instructions needed. {system_prompt}"
        while len(data_instructions) <= target_sample_count:
            seed_sample = random.choice(seed_samples)
            prompt = f"Generate a new sample that mirrors the content and style of the following input:\n\n{seed_sample}\n\nEnsure the new sample is coherent, relevant, and consistent in tone and writing style throughout. Do not include any additional instructions or explanations."
            data_instructions.append(prompt)
        loop = asyncio.get_event_loop()
        answers = loop.run_until_complete(self.datagen_bulk(model, data_instructions, system_prompt, max_requests, max_attempts))
        for i in range(len(data_instructions)):
            seed_samples.append(answers[i])
        instruction_answer_pairs = [(seed_samples[i], detect(seed_samples[i])) for i in range(len(seed_samples))]
        new_df = pd.DataFrame(instruction_answer_pairs, columns=[f'{question_column}','lang'])
        new_dataset = Dataset.from_pandas(new_df)
        new_dataset_dict = DatasetDict({"train": new_dataset})
        return new_dataset_dict
