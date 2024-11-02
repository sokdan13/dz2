import os
import configparser

class DependencyVisualizer:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.visualizer_path = self.config['settings']['visualizer_path']
        self.repository_path = self.config['settings']['repository_path']
        self.output_image_path = self.config['settings']['output_image_path']


if __name__ == '__main__':
    visualizer = DependencyVisualizer('config.ini')

