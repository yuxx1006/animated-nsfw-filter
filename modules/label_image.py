"""label_image for tflite."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from PIL import Image
import tensorflow as tf  # TF2
import urllib.request
from urllib.error import URLError, HTTPError
import smartcrop

# constant
MODEL_PATH = './model/saved_model.tflite'
LABEL_PATH = './model/class_labels.txt'
IMAGE_LOCAL = 'local-filename.jpg'

INPUT_MEAN = 127.5
INPUT_STD = 127.5


class Filter:
    def __init__(self, image_id, image_source, image_url):
        self.image_id = image_id
        self.image_source = image_source
        self.image_url = image_url

    """
	* Load labels for model
	* @param filename (String)
	*
	* @return
	*   $final (ARRAY)
	"""

    def load_labels(self, filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]

    """
	* Load images
	* @param image (RGB)
	*
	* @return
	*   $image_np (ARRAY)
	"""

    def load_images(self, image_input, width, height):
        # check image.open
        img = Image.open(image_input).resize((width, height)).convert('RGB')
        # add N dim
        input_data = np.expand_dims(img, axis=0)

        return img, input_data

    """
	* Sort and store results with labels in db
	* @param results (Array)
	*
	* @return
	*   $results (Json)
	"""

    def format_results(self, results, labels):
        image = {'_id': self.image_id, 'source': self.image_source}
        top_k = results.argsort()[-5:][::-1]
        labels = self.load_labels(labels)
        for i in top_k:
            image[labels[i]] = '{:08.6f}'.format(float(results[i]))
        return image

    def format_results_volc(self, results, labels, crop_r, crop_s):
        image = {}
        top_k = results.argsort()[-5:][::-1]
        labels = self.load_labels(labels)
        for i in top_k:
            image[labels[i]] = '{:08.6f}'.format(float(results[i]))
        image['crop_r'] = crop_r
        image['crop_s'] = crop_s
        return image

    """
	* download and label the image
	* @param photo(Url)
	*
	* @return
	*   $results (Json)
	"""

    def label_image(self):
        # download images
        try:
            urllib.request.urlretrieve(self.image_url, IMAGE_LOCAL)
        except (URLError, HTTPError):
            raise RuntimeError("Failed to download '{}'".format(self.image_url))

        # Load TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(MODEL_PATH)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # NxHxWxC, H:1, W:2
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]
        input_data = self.load_images(IMAGE_LOCAL, height, width)
        input_data = (np.float32(input_data) - INPUT_MEAN) / INPUT_STD

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        results = np.squeeze(output_data)

        results = self.format_results(results, LABEL_PATH)
        return results

    def label_image_volc(self):
        # download images
        try:
            urllib.request.urlretrieve(self.image_url, IMAGE_LOCAL)
        except (URLError, HTTPError):
            raise RuntimeError("Failed to download '{}'".format(self.image_url))

        # Load TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(MODEL_PATH)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # NxHxWxC, H:1, W:2
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]
        img, input_data = self.load_images(IMAGE_LOCAL, height, width)
        # crop image for best display
        sc = smartcrop.SmartCrop()
        crop_r = sc.crop(img, 160, 90)
        crop_r['top_crop'].pop('score')
        crop_s = sc.crop(img, 100, 100)
        crop_s['top_crop'].pop('score')

        input_data = (np.float32(input_data) - INPUT_MEAN) / INPUT_STD

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        results = np.squeeze(output_data)

        results = self.format_results_volc(results, LABEL_PATH, crop_r['top_crop'], crop_s['top_crop'])
        return results
