import os
import configparser

class DependencyVisualizer:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.visualizer_path = self.config['settings']['visualizer_path']
        self.repository_path = self.config['settings']['repository_path']
        self.output_image_path = self.config['settings']['output_image_path']

    def load_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def get_commits_with_parents(self):
        """Получает список коммитов с их родительскими коммитами"""
        os.chdir(self.repository_path)
        result = os.popen('git log --pretty=format:"%H %P"').read()
        commit_data = []
        for line in result.strip().split("\n"):
            parts = line.split()
            commit = parts[0]
            parents = parts[1:]
            commit_data.append((commit, parents))
        return commit_data

    def save_puml_file(self, puml_content, puml_file):
        with open(puml_file, 'w') as f:
            f.write(puml_content)

    def visualize_graph(self):
        commits_with_parents = self.get_commits_with_parents()
        puml_content = self.generate_puml_content(commits_with_parents)
        puml_file = os.path.join(self.repository_path, 'dependency_graph.puml')
        self.save_puml_file(puml_content, puml_file)

        # Генерация графа с использованием PlantUML
        os.system(f'java -jar "{self.visualizer_path}" "{puml_file}" -o "{os.path.dirname(self.output_image_path)}"')

    def run(self):
        self.visualize_graph()
        print(f'Граф зависимостей успешно сохранен в {self.output_image_path}')

if __name__ == '__main__':
    visualizer = DependencyVisualizer('config.ini')
    visualizer.run()
