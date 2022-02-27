import pathlib
import re
import typing

from environ import Env as _ENV

FileLoc = typing.Union[str, pathlib.Path]


def _keep_escaped_format_characters(match):
    """Keep escaped newline/tabs in quoted strings"""
    escaped_char = match.group(1)
    if escaped_char in "rnt":
        return "\\" + escaped_char
    return escaped_char


def _import_from_env_using_regex_match(m1, overrides):
    key, val = m1.group(1), m1.group(2)
    m2 = re.match(r"\A'(.*)'\Z", val)
    if m2:
        val = m2.group(1)
    m3 = re.match(r'\A"(.*)"\Z', val)
    if m3:
        val = re.sub(r"\\(.)", _keep_escaped_format_characters, m3.group(1))
    overrides[key] = str(val)


def _get_nested_ebv_file(line: str) -> FileLoc:
    try:
        return line.split("-e ")[1]
    except IndexError:
        return ""


def set_environ(env_holder: dict, overwrite: bool):
    """Return lambda to set environ.

    Use setdefault unless overwrite is specified.
    """
    if overwrite:
        return lambda k, v: env_holder.update({k: str(v)})
    return lambda k, v: env_holder.setdefault(k, str(v))


class Env(_ENV):
    LOCAL_ENVIRON = dict()
    _root_env_file = None
    _root_env_overwrite = None

    @classmethod
    def _read_from_file(
        cls, file_name: str, project_root: FileLoc, current_dir: FileLoc, **overrides
    ):
        env_file_str = _get_nested_ebv_file(file_name)
        if env_file_str:
            cls.read_env_from_file(
                project_root=project_root,
                relative_env_file_path=current_dir / env_file_str,
                overwrite=True,
                **overrides
            )

    @classmethod
    def _analyse_file_content(
        cls, content: str, overrides: dict, project_root: FileLoc, current_dir: FileLoc
    ):
        for line in content.splitlines():
            match = re.match(r"\A(?:export )?([A-Za-z_0-9]+)=(.*)\Z", line)
            if match:
                _import_from_env_using_regex_match(m1=match, overrides=overrides)
            elif line.startswith("-e"):
                cls._read_from_file(
                    file_name=line,
                    project_root=project_root,
                    current_dir=current_dir,
                    **overrides
                )

            elif not line or line.startswith("#"):
                # ignore warnings for empty line-breaks or comments
                pass

    @classmethod
    def read_env_from_file(
        cls,
        project_root: FileLoc,
        relative_env_file_path: FileLoc = None,
        overwrite: bool = False,
        **overrides
    ):
        env_file = pathlib.Path(project_root) / pathlib.Path(relative_env_file_path)

        if cls._root_env_file is None:
            cls._root_env_file = env_file
            cls._root_env_overwrite = overwrite

        current_dir = env_file.resolve().parent
        try:
            with open(str(env_file)) as f:
                content = f.read()
        except FileNotFoundError:
            return

        cls._analyse_file_content(
            content=content,
            overrides=overrides,
            project_root=project_root,
            current_dir=current_dir,
        )

        cls.LOCAL_ENVIRON.update(overrides)  # blindly update values

        # at the end of recursion, check for the actual `overwrite` value and
        # update the `cls.ENVIRON` dict.
        if env_file is cls._root_env_file:
            set_env_function = set_environ(env_holder=cls.ENVIRON, overwrite=overwrite)
            for key, value in cls.LOCAL_ENVIRON.items():
                set_env_function(key, value)
