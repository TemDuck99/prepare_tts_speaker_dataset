import os
from os import path
import argparse
from tqdm import tqdm

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
    speakers_group_by_gender = {"male": [], "female": []}
    for speaker_path, basename, gender in tqdm(speakers_paths):
        audios_path = path.join(speaker_path, TARGET_DIRS[0])
        texts_path = path.join(speaker_path, TARGET_DIRS[1])
        out_file = path.join(os.getcwd(), "datasets", gender,
                             f"{basename}.json")
        speakers_group_by_gender[gender].append((out_file, basename))
        if not os.path.exists(out_file):
            df = create_df(audios_path=audios_path, texts_path=texts_path)
            save_result(df=df, out_json=out_file)
    return speakers_group_by_gender


def concat_gender(gender_with_path: dict) -> None:
    all_df = pd.DataFrame()
    for gender in gender_with_path:
        temp_df = pd.DataFrame()
        for filepath, basename in gender_with_path[gender]:
            df = pd.read_json(filepath, orient="records", lines=True)
            df["speaker"] = basename
            temp_df = pd.concat([temp_df, df])
        out_file = os.path.join(os.getcwd(), "datasets/all",
                                f"{gender}_all.json")
        save_result(df=temp_df, out_json=out_file)
        temp_df["gender"] = gender
        all_df = pd.concat([temp_df, all_df])
    out_file = os.path.join(os.getcwd(), "datasets/all/all.json")
    save_result(df=all_df, out_json=out_file)
    return all_df


def main():
    paths_with_gender_split = prepare_datasets(speakers_dir_path=args.speakers_path)
    concat_gender(paths_with_gender_split)


if __name__ == "__main__":
    main()
