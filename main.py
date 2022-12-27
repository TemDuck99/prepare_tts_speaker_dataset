import os
import pandas as pd
import librosa
from loguru import logger
import ndjson
import argparse


TARGET_DIRS = ("Audios", "Transcripts")
logger.add("logs/error.log", format="{time}{level}{message}")
parser = argparse.ArgumentParser(
                    prog="Prepare",
                    description="Prepare manifest file, using TTS_speaker dir",
                    )
parser.add_argument("speaker_dir")
parser.add_argument("-o", "--outdir", default="datasets/manifest")
args = parser.parse_args()

SPEAKER_DIR = args.speaker_dir
OUT_DIR = args.outdir

audio_path = os.path.join(SPEAKER_DIR, TARGET_DIRS[0])
text_path = os.path.join(SPEAKER_DIR, TARGET_DIRS[1])


def get_transcribe(audio_filepath):
    filename = os.path.basename(audio_filepath).replace(".wav", ".txt")
    filepath = os.path.join(text_path, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            text = file.readline()
        return text
    else:
        logger.info(f"file not founded: {filename}")
        return None


def get_duration(audio_filepath):
    try:
        duration = librosa.core.get_duration(filename=audio_filepath)
        return duration
    except Exception as ex:
        logger.info(f"audio file broken: {audio_filepath}")
        logger.error(ex)
        return None


def create_df():
    audio_filepaths = pd.Series(
        os.path.join(audio_path, file) for file in os.listdir(audio_path)
    )
    df = pd.DataFrame(audio_filepaths, columns=["audio_filepath"])
    df["text"] = df["audio_filepath"].apply(lambda x: get_transcribe(x))
    df["duration"] = df["audio_filepath"].apply(lambda x: get_duration(x))
    return df


def save_result(df):
    out_csv = os.path.join(OUT_DIR, os.path.basename(SPEAKER_DIR)+".csv")
    out_json = os.path.join(OUT_DIR, os.path.basename(SPEAKER_DIR)+".json")
    df.to_csv(out_csv, index=False)
    with open(out_json, "w") as file:
        dict_records = df.to_dict(orient="records")
        ndjson.dump(dict_records, file, ensure_ascii=False)


def main():
    df = create_df()
    save_result(df)


if __name__ == "__main__":
    main()
