import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm
import pickle


DATADIR = "X:/Datasets/PetImages"

CATEGORIES = ["halls", "stairs", "wallOnLeft", "wallOnRight"]