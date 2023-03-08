#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""This module's docstring summary line.
Created by Konstantin Kuklin for Technische Hochschule Brandenburg (konstantin.kuklin@th-brandenburg.de)
Version 1.0
With the help of the audio recorder you can record mp3 streams from the Internet.
It should be possible to parameterize / set the following settings:
- URL of the stream
- Duration of the recording
- Filename of the saved stream
- Block size when reading/writing
- Optional: Display of all saved streams
- Display of help/usage info, if applicable
"""
from urllib.error import HTTPError

import click
import re
from urllib import request
from datetime import datetime
from os import listdir
import glob


@click.command()
@click.argument('streaming_url')
@click.option('--filename', default='myRadio', help='Name of mp3 file [Default filename: myRadio].')
@click.option('--duration', default=30, help='Duration of the recording in seconds [Default: 0] [Min = 0]')
@click.option('--blocksize', default=64, help='Block size for read/write in audio recording [Default: 64] [Min = 1].')
def record_stream(streaming_url, filename, duration, blocksize):
    """
    Module opens url and writes the audio recording into a mp3 file for set duration and set blocksize.
    You can find an overview of radio streams on https://wiki.ubuntuusers.de/Internetradio/Stationen/
    :param streaming_url: url with audio stream
    :param filename: mp3 to save the recording into
    :param duration: recording duration
    :param blocksize: size of the recording in byte
    :return: none
    """
    start_time = datetime.now()
    try:
        # Check if blocksize and duration are positive integers
        if duration <= 0:
            click.echo(click.style('Duration of at least zero required!', fg='red'))
            exit()
        if blocksize <= 0:
            click.echo(click.style('Blocksize must be at least 1 byte!', fg='red'))
            exit()
        # Check if url includes the http or https protocol if not concat protocol to url
        if not re.match('(http|https)://', streaming_url):
            streaming_url = 'http://{}'.format(streaming_url)
        # Add file format mp3 if filename doesn't include it already
        if not filename.endswith(".mp3"):
            filename = filename + '.mp3'
        stream = request.urlopen(streaming_url)
        with open(filename, 'wb') as audio_recording:
            while (datetime.now() - start_time).total_seconds() < duration:
                audio_recording.write(stream.read(blocksize))
        click.echo(click.style(f'Audio stream successfully saved in {filename}', fg='green'))
        # Prepare a list of all mp3 files in the current category
        stream_list = [stream for stream in glob.glob("*.mp3")]
        click.echo(click.style(f'Currently saved audio streams: {stream_list}', fg='green'))
        exit()
    except (HTTPError):
        click.echo(click.style('Requested URL could not be accessed. Please try different internet radio!', fg='red'))
        exit()


if __name__ == '__main__':
    record_stream()
