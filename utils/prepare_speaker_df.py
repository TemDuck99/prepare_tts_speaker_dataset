import os

import pandas as pd
import librosa
import ndjson
from loguru import logger


logger.add("logs/error.log", format="{time}{level}{message}")


def get_transcribe(audio_filepath, text_path):
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


def create_df(audios_path, texts_path):
    audio_filepaths = pd.Series(
        os.path.join(audios_path, file) for file in os.listdir(audios_path)
    )
    df = pd.DataFrame(audio_filepaths, columns=["audio_filepath"])
    df["text"] = df["audio_filepath"].apply(
        lambda x: get_transcribe(x, text_path=texts_path)
    )
    df["duration"] = df["audio_filepath"].apply(lambda x: get_duration(x))
    df["audio_filepath"] = df["audio_filepath"].apply(
        lambda x: os.path.join(*x.split("/")[-4:]))
    return df


def save_result(df, out_path, basename):
    out_csv = os.path.join(out_path, basename+".csv")
    out_json = os.path.join(out_path, basename+".json")
    df.to_csv(out_csv, index=False)
    with open(out_json, "w") as file:
        dict_records = df.to_dict(orient="records")
        ndjson.dump(dict_records, file, ensure_ascii=False)
