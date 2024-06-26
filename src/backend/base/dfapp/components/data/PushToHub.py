from dfapp.custom import CustomComponent
from datasets import DatasetDict


class PushToHubComponent(CustomComponent):
    display_name = "Push Dataset to HuggingFace Hub"
    description = "Pushes a dataset to the Hugging Face Hub."

    def build_config(self):
        return {
            "user_name": {"display_name": "hf user name", "info": "Hugging Face username."},
            "dataset_name": {
                "display_name": "hf dataset name",
                "info": "Name of the dataset to push. Specify username in user_name column if not included here.",
                "required": True
                },
            "huggingface_token": {
                "display_name": "Hugging Face Token",
                "password": True,
                "info": "Token for Hugging Face API authentication.",
                "required": True,
            },
        }

    def build(self, dataset: DatasetDict, dataset_name: str, huggingface_token: str, user_name: str = None):
        if '/' in dataset_name:
            repo_id = dataset_name
        else:
            repo_id = f"{user_name}/{dataset_name}"
        dataset.push_to_hub(repo_id, token=huggingface_token)
