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


class Env(_ENV):
    @classmethod
    def read_env(
        cls,
        root_loc: FileLoc,
        env_file: FileLoc = None,
        overwrite: bool = False,
        **overrides
    ):
        env_file = pathlib.Path(root_loc) / pathlib.Path(env_file)
        current_dir = env_file.resolve().parent
        try:
            with open(str(env_file)) as f:
                content = f.read()
        except FileNotFoundError:
            return

        for line in content.splitlines():
            match = re.match(r"\A(?:export )?([A-Za-z_0-9]+)=(.*)\Z", line)
            if match:
                _import_from_env_using_regex_match(m1=match, overrides=overrides)
            elif line.startswith("-e"):
                env_file = _get_nested_ebv_file(line)
                if env_file:
                    cls.read_env(
                        root_loc=root_loc,
                        env_file=current_dir / env_file,
                        overwrite=overwrite,
                    )
            elif not line or line.startswith("#"):
                # ignore warnings for empty line-breaks or comments
                pass

        def set_environ(envval):
            """Return lambda to set environ.

            Use setdefault unless overwrite is specified.
            """

            if overwrite:
                return lambda k, v: envval.update({k: str(v)})
            return lambda k, v: envval.setdefault(k, str(v))

        setenv = set_environ(cls.ENVIRON)

        for key, value in overrides.items():
            setenv(key, value)
