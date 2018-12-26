from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import csv
import tarfile
import subprocess
import progressbar

from glob import glob
from os import path
from sox import Transformer
from threading import RLock
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

from util.downloader import maybe_download, SIMPLE_BAR

from os import walk
import random
import pdb

FIELDNAMES = ['wav_filename', 'wav_filesize', 'transcript']
SAMPLE_RATE = 16000
MAX_SECS = 10
ARCHIVE_DIR_NAME = 'cv_corpus_v1'
ARCHIVE_NAME = ARCHIVE_DIR_NAME + '.tar.gz'
ARCHIVE_URL = 'https://s3.us-east-2.amazonaws.com/common-voice-data-download/' + ARCHIVE_NAME

#COMMAND TO move all the wavs in subdirectories to one directory
# /docker_files/CV_own_3/aws_poly_wav# find ./ -name '*.wav' -exec cp '{}' ../aws_poly_wav2/ \;

def custom_cv_writer(source_dir):
    source_dir = path.abspath(source_dir)
    f = []
    for (dirpath, dirnames, filenames) in walk(source_dir):
        f.extend(filenames)
        #break

    random.shuffle(f)
    wav_files_count = len(f)
    train_wavs_count = int(0.9 * wav_files_count)
    dev_wavs_count = int(0.07 * wav_files_count)
    #test_wavs_count = wav_files_count - (dev_wavs_count + train_wavs_count)
    #slices = slice(train_wavs_count,dev_wavs_count,test_wavs_count)
    train_wavs = f[0:train_wavs_count]
    dev_wavs = f[train_wavs_count:train_wavs_count+dev_wavs_count]
    test_wavs = f[train_wavs_count+dev_wavs_count:wav_files_count]
    pdb.set_trace()
    rows = []

    def create_csv(csv_type,wavs_list):
        with open(csv_type+".csv","w") as target_csv:
            counter = {"too_short":0,"proper":0,"too_long":0}
            for wav_filename in wavs_list:
                wav_filepath = source_dir + '/' + wav_filename
                frames = int(subprocess.check_output(['soxi', '-s', wav_filepath], stderr=subprocess.$
                file_size = path.getsize(wav_filepath)

                if(wav_filename.split('-')[0] != 'noisy'):
                        if(wav_filename.split('-')[-3]) != 'x':
                                transcript = wav_filename.split('-')[:-2]
                        else:
                                transcript = wav_filename.split('-')[:-3]
                        transcript = ' '.join(transcript)
                else:
                        #transcipt = wav_filename
                        if(wav_filename.split('-')[-3]) != 'x':
                                transcript = wav_filename.split('-')[1:-2]
                        else:
                                transcript = wav_filename.split('-')[1:-3]
                        transcript = ' '.join(transcript)
                #pdb.set_trace()

                if int(frames/SAMPLE_RATE*1000/10/2) < len(str(transcript)):
                    # Excluding samples that are too short to fit the transcript
                    counter['too_short'] += 1
                elif frames/SAMPLE_RATE > MAX_SECS:
                    # Excluding very long samples to keep a reasonable batch-size
                    counter['too_long'] += 1
                else:
                    # This one is good - keep it for the target CSV
                    rows.append((wav_filepath, file_size, transcript))
                    counter['proper'] += 1

            writer = csv.DictWriter(target_csv, fieldnames=FIELDNAMES)
            writer.writeheader()
            bar = progressbar.ProgressBar(max_value=len(rows), widgets=SIMPLE_BAR)
            for filename, file_size, transcript in bar(rows):
                writer.writerow({ 'wav_filename': filename, 'wav_filesize': file_size, 'transcript': $

        if counter['too_short'] > 0:
            print('Skipped %d samples that were too short to match the transcript.' % counter['too_sh$
        if counter['too_long'] > 0:
            print('Skipped %d samples that were longer than %d seconds.' % (counter['too_long'], MAX_$

    create_csv(source_dir+"/custom_train",train_wavs)
    create_csv(source_dir+"/custom_dev",dev_wavs)
    create_csv(source_dir+"/custom_test",test_wavs)

if __name__ == "__main__":
    #_download_and_preprocess_data(sys.argv[1])
    custom_cv_writer(sys.argv[1])
