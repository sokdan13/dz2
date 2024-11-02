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

    def get_files_changed(self, commit):
        """Получает файлы, измененные в конкретном коммите"""
        result = os.popen(f'git diff-tree --no-commit-id --name-only -r {commit}').read()
        return [os.path.abspath(file_path).replace('\\', '\\\\') for file_path in result.strip().splitlines()]

    def shorten_commit(self, commit_hash):
        """Сокращение хеша коммита до 7 символов"""
        return commit_hash[:7]

    def generate_puml_content(self, commits_with_parents):
        """Генерация содержимого PUML с учетом слияний и ветвлений"""
        puml_lines = ['@startuml']

        for commit, parents in commits_with_parents:
            short_commit = self.shorten_commit(commit)
            files_changed = self.get_files_changed(commit)
            files_content = "\\n".join(files_changed)
            puml_lines.append(f'class Commit_{short_commit} {{')
            puml_lines.append(f'{files_content}')
            puml_lines.append('}')

            for parent in parents:
                short_parent = self.shorten_commit(parent)
                puml_lines.append(f'Commit_{short_parent} --> Commit_{short_commit}')

        puml_lines.append('@enduml')
        return "\n".join(puml_lines)


if __name__ == '__main__':
    visualizer = DependencyVisualizer('config.ini')

