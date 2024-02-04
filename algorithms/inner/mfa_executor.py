import os
import json

from montreal_forced_aligner.command_line.mfa import create_parser
from montreal_forced_aligner.alignment import PretrainedAligner


class MFAExecutor:
    def __init__(
        self,
        corpus_directory: str,
        output_directory: str = "./asr/result",
        dictionary_path: str = "./algorithms/inner/mfa/mandarin_pinyin.dict",
        acoustic_model_path: str = "./algorithms/inner/mfa/mandarin.zip",
    ) -> None:
        parser = create_parser()
        self.args, unknown_args = parser.parse_known_args(
            args=[
                "align",
                corpus_directory,
                dictionary_path,
                acoustic_model_path,
                output_directory,
            ]
        )

        self.aligner = PretrainedAligner(
            acoustic_model_path=self.args.acoustic_model_path,
            corpus_directory=self.args.corpus_directory,
            dictionary_path=self.args.dictionary_path,
            temporary_directory=self.args.temporary_directory,
            **PretrainedAligner.parse_parameters(
                self.args.config_path, self.args, unknown_args
            ),
        )

    def __call__(self, file_name: str) -> list:
        """
        return list(sTime, eTime, pinyin)
        """
        try:
            self.aligner.align()
            self.aligner.export_files(
                self.args.output_directory,
                output_format="json",
                include_original_text=False,
            )
        except Exception:
            self.aligner.dirty = True
            raise
        finally:
            self.aligner.cleanup()

        return self.__read_result(file_name)

    def __read_result(self, file_name: str) -> list:
        result = json.load(
            open(os.path.join(self.args.output_directory, file_name + ".json"))
        )
        return result["tiers"]["words"]["entries"]


if __name__ == "__main__":
    mfa = MFAExecutor(
        corpus_directory="./asr/data",
        output_directory="./asr/result",
    )
    mfa("1")
