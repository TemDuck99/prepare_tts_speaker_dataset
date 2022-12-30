import os
from os import path
import argparse

import pandas as pd

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
    female_df = pd.DataFrame()
    male_df = pd.DataFrame()
    all_df = pd.DataFrame()
    for speaker_path, basename in speakers_paths:
        audios_path = path.join(speaker_path, TARGET_DIRS[0])
        texts_path = path.join(speaker_path, TARGET_DIRS[1])
        df = create_df(audios_path=audios_path, texts_path=texts_path)
        if "M" in basename:
            out_path = path.join(os.getcwd(), "datasets/Male")
            save_result(df=df, out_path=out_path, basename=basename)
            df["speaker"] = basename
            male_df = pd.concat([df, male_df])
            df["male"] = "Male"
            all_df = pd.concat([df, all_df])
        if "F" in basename:
            out_path = path.join(os.getcwd(), "datasets/Female")
            save_result(df=df, out_path=out_path, basename=basename)
            df["speaker"] = basename
            female_df = pd.concat([df, female_df])
            df["male"] = "female"
            all_df = pd.concat([df, all_df])
    out_path = path.join(os.getcwd(), "datasets/all")
    save_result(df=male_df, out_path=out_path, basename="all_male")
    save_result(df=female_df, out_path=out_path, basename="all_female")
    save_result(df=all_df, out_path=out_path, basename="all")


def main():
    prepare_datasets(speakers_dir_path=args.speakers_path)


if __name__ == "__main__":
    main()
