import os
from os import path
import argparse

from utils.find_speakers_dirs import get_speakers
from utils.prepare_speaker_df import create_df, save_result


TARGET_DIRS = ("Audios", "Transcripts")
parser = argparse.ArgumentParser(
                    prog="Prepare",
                    description="Prepare manifest file, using TTS_speaker dir",
                    )
parser.add_argument("speakers_path")
args = parser.parse_args()


def prepare_datasets(speakers_dir_path):
    speakers_paths = get_speakers(speakers_dirs_path=speakers_dir_path)
    print(*speakers_paths, sep="\n")
    for speaker_path, basename in speakers_paths:
        audios_path = path.join(speaker_path, TARGET_DIRS[0])
        texts_path = path.join(speaker_path, TARGET_DIRS[1])
        df = create_df(audios_path=audios_path, texts_path=texts_path)
        out_path = path.join(os.getcwd(), "datasets/manifest")
        save_result(df=df, out_path=out_path, basename=basename)


def main():
    prepare_datasets(speakers_dir_path=args.speakers_path)


if __name__ == "__main__":
    main()
