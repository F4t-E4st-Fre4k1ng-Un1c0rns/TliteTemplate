from dataclasses import dataclass, asdict

from transformers.models.auto.configuration_auto import AutoConfig
from transformers.utils.quantization_config import BitsAndBytesConfig
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.models.auto.modeling_auto import AutoModelForCausalLM
import torch


@dataclass
class Message:
    content: str
    role: str


class Tlite:
    def __init__(self, model_id: str = "t-tech/T-lite-it-1.0") -> None:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        tlite_config = AutoConfig.from_pretrained(model_id)

        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            config=tlite_config,
            trust_remote_code=True,
            quantization_config=bnb_config,
            torch_dtype=torch.bfloat16,
            offload_folder="/tmp/tlite-offload",
            cache_dir="/tmp/tlite-cache",
            attn_implementation="flash_attention_2",
            device_map="cuda",
        )


    def answer(self, messages: list[Message]) -> str:
        new_text = self.tokenizer.apply_chat_template(
            [asdict(m) for m in messages], tokenize=False, add_generation_prompt=True
        )
        model_inputs = self.tokenizer([new_text], return_tensors="pt").to(self.model.device)
    
        with torch.inference_mode():
            generated_ids = self.model.generate(**model_inputs, max_new_tokens=256)
    
        torch.cuda.empty_cache()
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        outputs = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return outputs
