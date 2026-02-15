#!/usr/bin/env python3
"""
Скрипт проверки окружения для проекта BC vs DAgger.

Проверяет:
- Версию Python (3.10.x)
- Активное conda окружение (rocm)
- Наличие необходимых пакетов
- Доступность GPU/ROCm
- Структуру директорий
- Установку Jupyter

Использование:
    python check_environment.py

Exit codes:
    0 - все проверки пройдены
    1 - есть критические ошибки
"""

import importlib
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union



# Цветовые коды ANSI
class Colors:
    """Цветовые коды для форматирования вывода."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


@dataclass
class CheckResult:
    """Результат проверки компонента окружения."""

    name: str
    passed: bool
    message: str
    is_warning: bool = False

    def format(self) -> str:
        """Форматирует результат проверки для вывода."""
        if self.passed:
            symbol = f"{Colors.GREEN}[✓]{Colors.RESET}"
        elif self.is_warning:
            symbol = f"{Colors.YELLOW}[!]{Colors.RESET}"
        else:
            symbol = f"{Colors.RED}[✗]{Colors.RESET}"
        return f"{symbol} {self.name}: {self.message}"


class EnvironmentChecker:
    """Класс для проверки окружения проекта BC vs DAgger."""

    REQUIRED_PYTHON_MAJOR = 3
    REQUIRED_PYTHON_MINOR = 10

    REQUIRED_PACKAGES: Dict[str, Tuple[str, Optional[str]]] = {
        "torch": ("2.0.0", None),
        "gymnasium": ("1.0.0", None),
        "numpy": ("1.21.0", None),
        "matplotlib": ("3.5.0", None),
        "seaborn": ("0.11.0", None),
        "h5py": ("3.7.0", None),
        "tqdm": ("4.60.0", None),
        "stable_baselines3": ("2.0.0", "stable_baselines3"),
        "ipywidgets": ("7.6.0", None),
        "packaging": ("20.0", None),  # Required for version comparison
    }

    REQUIRED_DIRS = ["models", "data", "logs", "plots"]

    def __init__(self) -> None:
        """Инициализирует чекер окружения."""
        self.results: List[CheckResult] = []
        self.has_errors = False
        self.has_warnings = False

    def _print_header(self, title: str) -> None:
        """Выводит заголовок секции."""
        width = 50
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * width}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{title.center(width)}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * width}{Colors.RESET}\n")

    def _print_section(self, title: str) -> None:
        """Выводит название секции проверок."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}▶ {title}{Colors.RESET}")

    def check_python_version(self) -> CheckResult:
        """Проверяет версию Python."""
        major = sys.version_info.major
        minor = sys.version_info.minor
        micro = sys.version_info.micro
        version_str = f"{major}.{minor}.{micro}"

        if major == self.REQUIRED_PYTHON_MAJOR and minor == self.REQUIRED_PYTHON_MINOR:
            return CheckResult(
                "Python версия",
                True,
                f"{version_str} (требуется 3.10.x)",
            )
        elif major == self.REQUIRED_PYTHON_MAJOR and minor > self.REQUIRED_PYTHON_MINOR:
            self.has_warnings = True
            return CheckResult(
                "Python версия",
                False,
                f"{version_str} (рекомендуется 3.10.x, но может работать)",
                is_warning=True,
            )
        else:
            self.has_errors = True
            return CheckResult(
                "Python версия",
                False,
                f"{version_str} (требуется 3.10.x)",
            )

    def check_conda_environment(self) -> CheckResult:
        """Проверяет активное conda окружение."""
        conda_prefix = os.environ.get("CONDA_PREFIX")
        conda_default_env = os.environ.get("CONDA_DEFAULT_ENV", "unknown")

        if not conda_prefix:
            self.has_warnings = True
            return CheckResult(
                "Conda окружение",
                False,
                "Conda не активна (возможно, используется venv или системный Python)",
                is_warning=True,
            )

        if conda_default_env == "rocm":
            return CheckResult(
                "Conda окружение",
                True,
                f"rocm ({conda_prefix})",
            )
        else:
            self.has_warnings = True
            return CheckResult(
                "Conda окружение",
                False,
                f"{conda_default_env} (рекомендуется 'rocm', но может работать)",
                is_warning=True,
            )

    def _get_package_version(self, package_name: str) -> Optional[str]:
        """Получает версию установленного пакета."""
        try:
            module = importlib.import_module(package_name)
            return getattr(module, "__version__", None)
        except ImportError:
            return None

    def _compare_versions(self, installed: str, required: str) -> bool:
        """Сравнивает версии пакетов."""
        try:
            from packaging.version import parse as parse_version
            return parse_version(installed) >= parse_version(required)
        except ImportError:
            # Fallback: сравнение по компонентам версии
            try:
                installed_parts = [int(x) for x in installed.split('.')[:3]]
                required_parts = [int(x) for x in required.split('.')[:3]]
                return installed_parts >= required_parts
            except (ValueError, AttributeError):
                return False
        except Exception:
            # Любая другая ошибка парсинга версии
            return False

    def check_packages(self) -> List[CheckResult]:
        """Проверяет наличие и версии необходимых пакетов."""
        results = []

        for package, (min_version, import_name) in self.REQUIRED_PACKAGES.items():
            module_name = import_name or package
            version = self._get_package_version(module_name)

            if version is None:
                self.has_errors = True
                results.append(
                    CheckResult(
                        package,
                        False,
                        f"не установлен (требуется >={min_version})",
                    )
                )
            elif self._compare_versions(version, min_version):
                results.append(CheckResult(package, True, f"{version}"))
            else:
                self.has_warnings = True
                results.append(
                    CheckResult(
                        package,
                        False,
                        f"{version} (требуется >={min_version})",
                        is_warning=True,
                    )
                )

        return results

    def check_gpu_rocm(self) -> List[CheckResult]:
        """Проверяет доступность GPU и ROCm."""
        results = []

        try:
            import torch

            # Проверка CUDA/ROCm доступности
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                results.append(CheckResult("GPU доступность", True, "да"))
                results.append(CheckResult("GPU устройство", True, gpu_name))

                # Проверка версии ROCm/HIP
                if hasattr(torch, "_C"):
                    rocm_version = getattr(torch._C, "_rocm_version", None)
                    if rocm_version:
                        results.append(
                            CheckResult("ROCm версия", True, f"{rocm_version}")
                        )
                elif hasattr(torch.version, "hip") and torch.version.hip:
                    results.append(
                        CheckResult("HIP версия", True, f"{torch.version.hip}")
                    )
                else:
                    results.append(
                        CheckResult(
                            "ROCm/HIP",
                            False,
                            "не определена (возможно CUDA)",
                            is_warning=True,
                        )
                    )

                # Проверка версии PyTorch
                if "rocm" in torch.__version__:
                    results.append(
                        CheckResult("PyTorch бэкенд", True, "ROCm")
                    )
                elif "cuda" in torch.__version__:
                    results.append(
                        CheckResult(
                            "PyTorch бэкенд",
                            False,
                            "CUDA (ожидался ROCm)",
                            is_warning=True,
                        )
                    )
                else:
                    results.append(
                        CheckResult("PyTorch бэкенд", True, "CPU")
                    )
            else:
                self.has_warnings = True
                results.append(
                    CheckResult(
                        "GPU доступность",
                        False,
                        "нет (будет использован CPU)",
                        is_warning=True,
                    )
                )
                results.append(
                    CheckResult(
                        "CPU fallback",
                        True,
                        "доступен",
                    )
                )

        except ImportError:
            self.has_errors = True
            results.append(
                CheckResult(
                    "PyTorch", 
                    False, 
                    "не установлен (pip install torch --index-url https://download.pytorch.org/whl/rocm5.7)"
                )
            )

        return results

    def check_directories(self) -> List[CheckResult]:
        """Проверяет и создаёт необходимые директории."""
        results = []

        for dir_name in self.REQUIRED_DIRS:
            dir_path = Path(dir_name)
            try:
                # Используем exist_ok=True для атомарного создания
                dir_path.mkdir(parents=True, exist_ok=True)
                # Проверяем, была ли директория создана или уже существовала
                if any(dir_path.iterdir()):
                    results.append(CheckResult(f"Директория {dir_name}/", True, "существует (не пуста)"))
                else:
                    results.append(CheckResult(f"Директория {dir_name}/", True, "существует (пуста)"))
            except OSError as e:
                self.has_errors = True
                results.append(
                    CheckResult(
                        f"Директория {dir_name}/",
                        False,
                        f"ошибка: {e}",
                    )
                )

        return results

    def check_jupyter(self) -> List[CheckResult]:
        """Проверяет установку Jupyter."""
        results = []

        # Проверка наличия jupyter
        try:
            result = subprocess.run(
                ["jupyter", "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                results.append(CheckResult("Jupyter", True, "установлен"))
            else:
                self.has_warnings = True
                results.append(
                    CheckResult(
                        "Jupyter",
                        False,
                        "не найден (установите: pip install jupyter)",
                        is_warning=True,
                    )
                )
        except FileNotFoundError:
            self.has_warnings = True
            results.append(
                CheckResult(
                    "Jupyter",
                    False,
                    "не найден (установите: pip install jupyter)",
                    is_warning=True,
                )
            )

        # Проверка nbextensions для ipywidgets
        try:
            import ipywidgets
            results.append(CheckResult("ipywidgets", True, f"{ipywidgets.__version__}"))
        except ImportError:
            self.has_warnings = True
            results.append(
                CheckResult(
                    "ipywidgets",
                    False,
                    "не установлен (виджеты не будут работать)",
                    is_warning=True,
                )
            )

        return results

    def print_summary(self) -> int:
        """Выводит итоговую сводку и возвращает exit code."""
        self._print_header("ИТОГОВАЯ СВОДКА")

        if not self.has_errors and not self.has_warnings:
            print(
                f"{Colors.GREEN}{Colors.BOLD}"
                f"✓ Все проверки пройдены успешно!"
                f"{Colors.RESET}"
            )
            print(f"\n{Colors.CYAN}Можно запускать Jupyter notebook!{Colors.RESET}")
            return 0
        elif not self.has_errors:
            print(
                f"{Colors.YELLOW}{Colors.BOLD}"
                f"! Проверки пройдены с предупреждениями"
                f"{Colors.RESET}"
            )
            print(
                f"\n{Colors.YELLOW}"
                f"Проект может работать, но рекомендуется устранить предупреждения."
                f"{Colors.RESET}"
            )
            return 0
        else:
            print(
                f"{Colors.RED}{Colors.BOLD}"
                f"✗ Обнаружены критические ошибки!"
                f"{Colors.RESET}"
            )
            print(
                f"\n{Colors.RED}"
                f"Пожалуйста, установите недостающие зависимости:"
                f"{Colors.RESET}"
            )
            print(f"  {Colors.BOLD}pip install -r requirements.txt{Colors.RESET}")
            print(
                f"\n{Colors.YELLOW}"
                f"Или создайте conda окружение:"
                f"{Colors.RESET}"
            )
            print(f"  {Colors.BOLD}conda env create -f environment.yml{Colors.RESET}")
            return 1

    def run_all_checks(self) -> int:
        """Запускает все проверки окружения."""
        self._print_header("Проверка окружения: BC vs DAgger")

        # Python версия
        self._print_section("Версия Python")
        result = self.check_python_version()
        print(result.format())
        self.results.append(result)

        # Conda окружение
        self._print_section("Conda окружение")
        result = self.check_conda_environment()
        print(result.format())
        self.results.append(result)

        # Пакеты
        self._print_section("Необходимые пакеты")
        for result in self.check_packages():
            print(result.format())
            self.results.append(result)

        # GPU/ROCm
        self._print_section("GPU и ROCm")
        for result in self.check_gpu_rocm():
            print(result.format())
            self.results.append(result)

        # Директории
        self._print_section("Структура директорий")
        for result in self.check_directories():
            print(result.format())
            self.results.append(result)

        # Jupyter
        self._print_section("Jupyter Notebook")
        for result in self.check_jupyter():
            print(result.format())
            self.results.append(result)

        # Итог
        return self.print_summary()


def main() -> int:
    """Главная функция скрипта."""
    try:
        checker = EnvironmentChecker()
        exit_code = checker.run_all_checks()
        return exit_code
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Проверка прервана пользователем.{Colors.RESET}")
        return 130
    except Exception as e:
        print(f"\n{Colors.RED}Критическая ошибка: {e}{Colors.RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
