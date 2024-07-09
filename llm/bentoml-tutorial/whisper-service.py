import os
import typing as t
from pathlib import Path

import bentoml

# # for ROCm, 10.3.0 is gfx1030
# os.environ["HSA_OVERRIDE_GFX_VERSION"] = "10.3.0"
# # for multiple GPUs ,e.g. you have GPU + iGPU/APU
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# export HSA_OVERRIDE_GFX_VERSIONPGHOST="10.3.0"
# export CUDA_VISIBLE_DEVICES="0"

LANGUAGE_CODE = "en"


@bentoml.service(
    traffic={"timeout": 30},
    resources={
        "gpu": 1,
        "memory": "16Gi",
    },
)
class WhisperX:
    """
    This class is inspired by the implementation shown in the whisperX project.
    Source: https://github.com/m-bain/whisperX
    """

    def __init__(self):
        import torch
        import whisperx

        print("CUDA available: ", torch.cuda.is_available())
        print("CUDA device name: ", torch.cuda.get_device_name(0))

        self.batch_size = 16  # reduce if low on GPU mem
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # compute_type = "float16" if torch.cuda.is_available() else "int8"

        self.device = "cpu"
        compute_type = "int8"
        self.model = whisperx.load_model(
            "large-v3", self.device, compute_type=compute_type, language=LANGUAGE_CODE
        )
        self.model_a, self.metadata = whisperx.load_align_model(
            language_code=LANGUAGE_CODE, device=self.device
        )

    @bentoml.api
    def transcribe(self, audio_file: Path) -> t.Dict:
        import whisperx

        audio = whisperx.load_audio(audio_file)
        result = self.model.transcribe(audio, batch_size=self.batch_size)
        result = whisperx.align(
            result["segments"],
            self.model_a,
            self.metadata,
            audio,
            self.device,
            return_char_alignments=False,
        )

        return result
