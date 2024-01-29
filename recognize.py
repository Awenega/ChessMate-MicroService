#!/usr/bin/env python3

import numpy as np
import os
import PIL.Image
import tensorflow as tf
from tensorflow.keras import models
from io import BytesIO
from functools import reduce

USE_GRAYSCALE = True
NN_MODEL_PATH = './nn/model.tf'
FEN_CHARS = '1RNBQKPrnbqkp'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def _chessboard_tiles_img_data(img):
    """ Given a file path to a chessboard PNG image, returns a
        size-64 array of 32x32 tiles representing each square of a chessboard
    """

    n_channels = 1 if USE_GRAYSCALE else 3
    tiles = get_chessboard_tiles(img, use_grayscale=USE_GRAYSCALE)
    img_data_list = []
    for i in range(64):
        buf = BytesIO()
        tiles[i].save(buf, format='PNG')
        img_data = tf.image.decode_image(buf.getvalue(), channels=n_channels)
        img_data = tf.image.convert_image_dtype(img_data, tf.float32)
        img_data = tf.image.resize(img_data, [32, 32])
        img_data_list.append(img_data)
    return img_data_list

def get_chessboard_tiles(img, use_grayscale=True):
    """ chessboard_img_path = path to a chessboard image
        use_grayscale = true/false for whether to return tiles in grayscale

        Returns a list (length 64) of 32x32 image data
    """
    img_data_tmp = img.convert('RGB')
    img_data = img_data_tmp.resize([256, 256], PIL.Image.BILINEAR)
    if use_grayscale:
        img_data = img_data.convert('L', (0.2989, 0.5870, 0.1140, 0))
    chessboard_256x256_img = np.asarray(img_data, dtype=np.uint8)
    # 64 tiles in order from top-left to bottom-right (A8, B8, ..., G1, H1)
    tiles = [None] * 64
    for rank in range(8): # rows/ranks (numbers)
        for file in range(8): # columns/files (letters)
            sq_i = rank * 8 + file
            tile = np.zeros([32, 32, 3], dtype=np.uint8)
            for i in range(32):
                for j in range(32):
                    if use_grayscale:
                        tile[i, j] = chessboard_256x256_img[
                            rank*32 + i,
                            file*32 + j,
                        ]
                    else:
                        tile[i, j] = chessboard_256x256_img[
                            rank*32 + i,
                            file*32 + j,
                            :,
                        ]
            tiles[sq_i] = PIL.Image.fromarray(tile, 'RGB')
    return tiles

def compressed_fen(fen):
    """ From: 11111q1k/1111r111/111p1pQP/111P1P11/11prn1R1/11111111/111111P1/R11111K1
        To: 5q1k/4r3/3p1pQP/3P1P2/2prn1R1/8/6P1/R5K1
    """
    for length in reversed(range(2,9)):
        fen = fen.replace(length * '1', str(length))
    return fen

def predict_tile(tile_img_data, model):
    """ Given the image data of a tile, try to determine what piece
        is on the tile, or if it's blank.

        Returns a tuple of (predicted FEN char, confidence)
    """
    probabilities = list(model.predict(np.array([tile_img_data]))[0])
    max_probability = max(probabilities)
    i = probabilities.index(max_probability)
    return (FEN_CHARS[i], max_probability)

def predict_chessboard(img):
    """ Given a file path to a chessboard PNG image,
        Returns a FEN string representation of the chessboard
    """
    model = models.load_model(NN_MODEL_PATH)
    img_data_list = _chessboard_tiles_img_data(img)
    predictions = []
    confidence = 1
    for i in range(64):
        tile_img_data = img_data_list[i]
        (fen_char, probability) = predict_tile(tile_img_data, model)
        predictions.append((fen_char, probability))
    predicted_fen = compressed_fen('/'.join([''.join(r) for r in np.reshape([p[0] for p in predictions], [8, 8])]))

    confidence = reduce(lambda x,y: x*y, [p[1] for p in predictions])
    print("Confidence: {}".format(confidence))
    print("https://lichess.org/editor/{}".format(predicted_fen))
    return predicted_fen

