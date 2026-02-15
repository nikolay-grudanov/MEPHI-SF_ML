#!/usr/bin/env python3
"""
Скрипт автоматической проверки качества проекта "Сравнение BC и DAgger"

Использование:
    python check_project.py

Проверки:
1. Количество заглушек в блокноте (должно быть 0)
2. Структура директорий (models/, data/, logs/, plots/)
3. Наличие ключевых файлов
4. Структура датасетов HDF5
5. Наличие графиков
6. Функциональность GPU/CPU

Дата: 2026-02-02
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Цвета для вывода
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class ProjectChecker:
    """Класс для проверки качества проекта"""

    def __init__(self, project_root: str | None = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.notebook_path = self.project_root / "HW3_BC_GNA.ipynb"
        self.total_checks = 0
        self.passed_checks = 0
        self.failed_checks = 0

    def print_header(self, text: str):
        """Вывести заголовок"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")

    def print_result(self, check_name: str, passed: bool, details: str = ""):
        """Вывести результат проверки"""
        self.total_checks += 1
        if passed:
            self.passed_checks += 1
            print(f"{Colors.GREEN}✓ PASS{Colors.END} {check_name}")
        else:
            self.failed_checks += 1
            print(f"{Colors.RED}✗ FAIL{Colors.END} {check_name}")
        if details:
            print(f"      {Colors.YELLOW}{details}{Colors.END}")

    def check_notebook_placeholders(self) -> bool:
        """Проверка: все заглушки отмечены чекбоксом [v]"""
        self.print_header("1. Проверка заполнения заглушек")

        if not self.notebook_path.exists():
            self.print_result(
                "Файл HW3_BC_GNA.ipynb существует",
                False,
                f"Файл не найден по пути: {self.notebook_path}"
            )
            return False

        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)

        unfilled_count = 0
        filled_count = 0
        cells_info = []

        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                lines = source.split('\n')

                for line_idx, line in enumerate(lines):
                    if 'ВАШ КОД' in line:
                        # Проверяем чекбокс
                        if '[v]' in line:
                            filled_count += 1
                        elif '[ ]' in line or ('ВАШ КОД' in line and '[' not in line):
                            # [ ] - не заполнено
                            # Нет чекбокса - считаем не заполненным
                            unfilled_count += 1
                            cells_info.append((i, line_idx, line.strip()))

        total_placeholders = filled_count + unfilled_count
        all_passed = (unfilled_count == 0)

        self.print_result(
            f"Заглушки заполнены ({unfilled_count} незаполненных)",
            all_passed,
            f"Заполнено: {filled_count}/{total_placeholders}"
        )

        if unfilled_count > 0:
            print(f"\n{Colors.YELLOW}Незаполненные заглушки (нет [v]):{Colors.END}")
            for cell_idx, line_idx, line in cells_info[:5]:
                print(f"  - Cell {cell_idx}, Line {line_idx}: {line[:80]}")
            if len(cells_info) > 5:
                print(f"  ... и еще {len(cells_info) - 5} строк")
            print(f"\n{Colors.YELLOW}Как исправить:{Colors.END}")
            print(f"  Замените '[ ]' на '[v]' или добавьте '[v]' после 'ВАШ КОД'")
            print(f"  Пример: #### ВАШ КОД [v] ####")
            all_passed = False

        return all_passed

    def check_directory_structure(self) -> bool:
        """Проверка: структура директорий"""
        self.print_header("2. Проверка структуры директорий")

        required_dirs = {
            'models': 'Папка для сохраненных моделей (.pt)',
            'data': 'Папка для датасетов (.h5)',
            'logs': 'Папка для логов (.csv/.json)',
            'plots': 'Папка для графиков (.png)'
        }

        all_passed = True
        for dir_name, description in required_dirs.items():
            dir_path = self.project_root / dir_name
            exists = dir_path.exists() and dir_path.is_dir()
            self.print_result(
                f"Директория {dir_name}/ существует",
                exists,
                description
            )
            if not exists:
                all_passed = False

        return all_passed

    def check_key_files(self) -> bool:
        """Проверка: наличие ключевых файлов"""
        self.print_header("3. Проверка наличия файлов")

        # Проверяем, что директории существуют, перед поиском файлов
        models_dir = self.project_root / 'models'
        data_dir = self.project_root / 'data'
        logs_dir = self.project_root / 'logs'
        plots_dir = self.project_root / 'plots'

        expected_files = {
            'models/bc_model.pt': 'Обученная политика BC',
            'models/dagger_model.pt': 'Обученная политика DAgger',
            'data/expert_data.h5': 'Датасет эксперта',
            'data/dagger_data.h5': 'Агрегированный датасет DAgger',
            'logs/bc_training.csv': 'Лог обучения BC',
            'logs/dagger_training.csv': 'Лог обучения DAgger',
            'plots/bc_dagger_comparison.png': 'График сравнения BC и DAgger',
            'plots/dagger_convergence.png': 'График сходимости DAgger',
            'plots/bc_data_scaling.png': 'График зависимости BC от объема данных'
        }

        all_passed = True
        for file_path, description in expected_files.items():
            full_path = self.project_root / file_path
            exists = full_path.exists()
            self.print_result(
                f"Файл {file_path} существует",
                exists,
                description
            )
            if not exists:
                all_passed = False

        return all_passed

    def check_hdf5_structure(self) -> bool:
        """Проверка: структура датасетов HDF5"""
        self.print_header("4. Проверка структуры датасетов HDF5")

        try:
            import h5py
        except ImportError:
            self.print_result(
                "Библиотека h5py установлена",
                False,
                "Не удалось импортировать h5py. Установите: pip install h5py"
            )
            return False

        # Поддерживаем обе структуры данных:
        # 1. Плоская структура: observations, actions, rewards, dones
        # 2. Индексированные группы: 0, 1, 2, ... (каждая содержит states, actions)
        all_passed = True
        for file_path in ['data/expert_data.h5', 'data/dagger_data.h5']:
            full_path = self.project_root / file_path

            if not full_path.exists():
                self.print_result(
                    f"Структура {file_path}",
                    False,
                    "Файл не существует"
                )
                all_passed = False
                continue

            try:
                with h5py.File(full_path, 'r') as f:
                    keys = list(f.keys())

                    if len(keys) == 0:
                        self.print_result(
                            f"Структура {file_path} корректна",
                            False,
                            "Нет данных в файле"
                        )
                        all_passed = False
                        continue

                    # Проверяем, какая структура используется
                    # Если первый ключ — это группа, то это индексированная структура
                    first_key = keys[0]
                    is_flat_structure = not isinstance(f[first_key], h5py.Group)

                    if is_flat_structure:
                        # Плоская структура: observations, actions, rewards, dones
                        required_keys = ['observations', 'actions', 'rewards', 'dones']
                        missing_keys = [k for k in required_keys if k not in f]

                        self.print_result(
                            f"Структура {file_path} корректна",
                            len(missing_keys) == 0,
                            f"Плоская структура; " +
                            f"Отсутствуют ключи: {missing_keys}" if missing_keys else
                            f"Все ключи присутствуют"
                        )

                        if len(missing_keys) > 0:
                            all_passed = False
                    else:
                        # Индексированная структура: 0, 1, 2, ...
                        first_traj = f[first_key]
                        required_in_traj = ['states', 'actions']
                        missing_keys = [k for k in required_in_traj if k not in first_traj]

                        self.print_result(
                            f"Структура {file_path} корректна",
                            len(missing_keys) == 0,
                            f"Индексированная структура; Траекторий: {len(keys)}; " +
                            f"Отсутствуют ключи в траектории: {missing_keys}" if missing_keys else
                            f"Все ключи присутствуют ({len(keys)} траекторий)"
                        )

                        if len(missing_keys) > 0:
                            all_passed = False
            except Exception as e:
                self.print_result(
                    f"Чтение {file_path}",
                    False,
                    f"Ошибка: {str(e)}"
                )
                all_passed = False

        return all_passed

    def check_logs_format(self) -> bool:
        """Проверка: формат лог-файлов (CSV)"""
        self.print_header("5. Проверка формата лог-файлов")

        try:
            import pandas as pd
        except ImportError:
            self.print_result(
                "Библиотека pandas установлена",
                False,
                "Не удалось импортировать pandas. Установите: pip install pandas"
            )
            return False

        log_files = {
            'logs/bc_training.csv': ['timestamp', 'epoch', 'loss', 'learning_rate'],
            'logs/dagger_training.csv': ['iteration', 'mean_reward']
        }

        all_passed = True
        for file_path, expected_columns in log_files.items():
            full_path = self.project_root / file_path

            if not full_path.exists():
                self.print_result(
                    f"Формат {file_path}",
                    False,
                    "Файл не существует"
                )
                all_passed = False
                continue

            try:
                df = pd.read_csv(full_path)
                missing_cols = [col for col in expected_columns if col not in df.columns]

                self.print_result(
                    f"Формат {file_path} корректен",
                    len(missing_cols) == 0,
                    f"Отсутствуют колонки: {missing_cols}" if missing_cols else f"Строк: {len(df)}"
                )

                if len(missing_cols) > 0:
                    all_passed = False
            except Exception as e:
                self.print_result(
                    f"Чтение {file_path}",
                    False,
                    f"Ошибка: {str(e)}"
                )
                all_passed = False

        return all_passed

    def check_gpu_utils(self) -> bool:
        """Проверка: наличие и импорт gpu_utils.py"""
        self.print_header("6. Проверка GPU/CPU поддержки")

        gpu_utils_path = self.project_root / 'gpu_utils.py'

        # Проверка существования файла
        exists = gpu_utils_path.exists()
        self.print_result(
            "Файл gpu_utils.py существует",
            exists,
            "Модуль для работы с GPU/CPU"
        )

        if not exists:
            return False

        # Проверка наличия функции get_device
        try:
            with open(gpu_utils_path, 'r', encoding='utf-8') as f:
                content = f.read()
                has_get_device = 'def get_device' in content
                self.print_result(
                    "Функция get_device() реализована",
                    has_get_device,
                    "Проверка доступности GPU с фолбэком на CPU"
                )
        except Exception as e:
            self.print_result(
                "Чтение gpu_utils.py",
                False,
                f"Ошибка: {str(e)}"
            )
            return False

        # Проверка импорта в блокноте
        if self.notebook_path.exists():
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                nb = json.load(f)

            has_import = False
            for cell in nb['cells']:
                if cell['cell_type'] == 'code':
                    source = ''.join(cell['source'])
                    if 'from gpu_utils import' in source or 'import gpu_utils' in source:
                        has_import = True
                        break

            self.print_result(
                "gpu_utils.py импортирован в блокнот",
                has_import,
                "Инструкция: from gpu_utils import get_device"
            )
        else:
            self.print_result(
                "Проверка импорта gpu_utils",
                False,
                "Блокнот не найден"
            )
            return False

        return exists

    def run_all_checks(self) -> bool:
        """Запустить все проверки"""
        print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
        print(f"{Colors.BOLD}АВТОМАТИЧЕСКАЯ ПРОВЕРКА ПРОЕКТА{Colors.END}")
        print(f"{Colors.BOLD}Сравнение алгоритмов BC и DAgger{Colors.END}")
        print(f"{Colors.BOLD}{'=' * 70}{Colors.END}")

        # Запускаем проверки
        self.check_notebook_placeholders()
        self.check_directory_structure()
        self.check_key_files()
        self.check_hdf5_structure()
        self.check_logs_format()
        self.check_gpu_utils()

        # Итоговый отчет
        self.print_header("ИТОГОВЫЙ ОТЧЕТ")

        success_rate = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0

        print(f"{Colors.BOLD}Всего проверок:{Colors.END} {self.total_checks}")
        print(f"{Colors.GREEN}{Colors.BOLD}Пройдено:{Colors.END} {self.passed_checks}")
        print(f"{Colors.RED}{Colors.BOLD}Провалено:{Colors.END} {self.failed_checks}")
        print(f"{Colors.BOLD}Успешность:{Colors.END} {success_rate:.1f}%")

        if success_rate >= 90:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ОТЛИЧНО! Проект готов к сдаче.{Colors.END}")
            return True
        elif success_rate >= 70:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ ХОРОШО, но есть недочеты.{Colors.END}")
            print(f"{Colors.YELLOW}Рекомендуется исправить проваленные проверки.{Colors.END}")
            return False
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ ПРОЕКТ ТРЕБУЕТ ДОРАБОТКИ.{Colors.END}")
            print(f"{Colors.RED}Необходимо исправить проваленные проверки.{Colors.END}")
            return False


def main():
    """Точка входа"""
    parser = argparse.ArgumentParser(
        description='Автоматическая проверка проекта "Сравнение BC и DAgger"'
    )
    parser.add_argument(
        '--project-root',
        type=str,
        default=None,
        help='Корневая директория проекта (по умолчанию: текущая директория)'
    )
    args = parser.parse_args()

    checker = ProjectChecker(args.project_root)
    success = checker.run_all_checks()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    import argparse
    main()
