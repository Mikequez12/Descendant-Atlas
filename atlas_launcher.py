from pathlib import Path
import json
import platform
import os
import re

VAR_RE = re.compile(r"\$\{([^}]+)\}")



def build_launch_command(
    versions_dir: Path,
    version_id: str,
    game_dir: Path,
    assets_dir: Path,
    java: str = "java",
    java_args: list[str] | None = None,
    auth: dict | None = None,
) -> list[str]:
    version = load_version(versions_dir, version_id)

    classpath = build_classpath(version, versions_dir)

    jvm_args = build_jvm_args(
        version,
        classpath,
        game_dir,
        assets_dir,
        auth,
    )

    game_args = build_game_args(
        version,
        game_dir,
        assets_dir,
        auth,
    )

    return [
        java,
        *(java_args or []),
        *jvm_args,
        version["mainClass"],
        *game_args,
    ]

def deep_merge(parent: dict, child: dict) -> dict:
    result = parent.copy()

    for k, v in child.items():
        if (
            k in result
            and isinstance(result[k], dict)
            and isinstance(v, dict)
        ):
            result[k] = deep_merge(result[k], v)

        elif (
            k in result
            and isinstance(result[k], list)
            and isinstance(v, list)
        ):
            result[k] = result[k] + v

        else:
            result[k] = v

    return result


def load_version(versions_dir: Path, version_id: str) -> dict:
    path = versions_dir / version_id / f"{version_id}.json"

    with path.open(encoding="utf-8") as f:
        version = json.load(f)

    parent = version.get("inheritsFrom")
    if not parent:
        return version

    parent_version = load_version(versions_dir, parent)

    return deep_merge(parent_version, version)

def build_classpath(version: dict, versions_dir: Path) -> str:
    cp = []

    for lib in version.get("libraries", []):
        if not library_allowed(lib):
            continue

        downloads = lib.get("downloads", {})
        artifact = downloads.get("artifact")

        if artifact:
            cp.append(str(versions_dir.parent / "libraries" / artifact["path"]))

    version_id = version["id"]
    cp.append(str(versions_dir / version_id / f"{version_id}.jar"))

    return os.pathsep.join(cp)

def library_allowed(lib: dict) -> bool:
    rules = lib.get("rules")

    if not rules:
        return True

    os_name = {
        "Windows": "windows",
        "Linux": "linux",
        "Darwin": "osx",
    }[platform.system()]

    allowed = False

    for rule in rules:
        match = rule.get("os", {}).get("name") == os_name if "os" in rule else True

        if match:
            allowed = (rule["action"] == "allow")

    return allowed


def build_jvm_args(
    version: dict,
    classpath: str,
    game_dir,
    assets_dir,
    auth=None,
):
    args = []

    variables = {
        "classpath": classpath,
        "classpath_separator": os.pathsep,
        "natives_directory": str(game_dir / "natives"),
        "library_directory": str(game_dir.parent / "libraries"),
        "launcher_name": "Atlas",
        "launcher_version": "1.0",

        "version_name": version["id"],
    }

    if auth:
        variables.update(auth)

    for arg in version.get("arguments", {}).get("jvm", []):

        if isinstance(arg, str):
            args.append(expand_variables(arg, variables))

        elif isinstance(arg, dict):
            if not rules_match(arg.get("rules"), features={}):
                continue

            value = arg["value"]

            if isinstance(value, str):
                args.append(expand_variables(value, variables))
            else:
                args.extend(
                    expand_variables(v, variables)
                    for v in value
                )

    return expand_arguments(args, variables)

def expand_variables(text: str, variables: dict):
    return VAR_RE.sub(
        lambda m: str(variables.get(m.group(1), m.group(0))),
        text,
    )

import shlex

def build_game_args(version, game_dir, assets_dir, auth=None):
    variables = {
        "game_directory": str(game_dir),
        "assets_root": str(assets_dir),
        "assets_index_name": version.get("assets", ""),
        "version_name": version["id"],

        "auth_player_name": "Player",
        "auth_uuid": "00000000-0000-0000-0000-000000000000",
        "auth_access_token": "",
        "clientid": "",
        "user_type": "legacy",
        "version_type": version.get("type", "release"),
        "user_properties": "{}",
        "auth_xuid": "",
    }

    if auth:
        variables.update(auth)

    if "arguments" in version:
        args = []

        for arg in version["arguments"].get("game", []):

            if isinstance(arg, str):
                args.append(expand_variables(arg, variables))

            elif isinstance(arg, dict):
                if not rules_match(arg.get("rules"), features={}):
                    continue

                value = arg["value"]

                if isinstance(value, str):
                    args.append(expand_variables(value, variables))
                else:
                    args.extend(
                        expand_variables(v, variables)
                        for v in value
                    )

        return expand_arguments(args, variables)

    return [
        expand_variables(x, variables)
        for x in shlex.split(version["minecraftArguments"])
    ]

def rules_match(rules, features=None):

    if not rules:
        return True

    if features is None:
        features = {}

    os_name = {
        "Windows": "windows",
        "Linux": "linux",
        "Darwin": "osx",
    }[platform.system()]

    allowed = False

    for rule in rules:
        # ¿La regla aplica al SO?
        if "os" in rule:
            os_rule = rule["os"]

            if "name" in os_rule and os_rule["name"] != os_name:
                continue

            if "arch" in os_rule:
                arch = "x86" if platform.architecture()[0] == "32bit" else "x86_64"
                if os_rule["arch"] != arch:
                    continue

        if "features" in rule:
            ok = True

            for key, value in rule["features"].items():
                if features.get(key, False) != value:
                    ok = False
                    break

            if not ok:
                continue

        allowed = (rule["action"] == "allow")

    return allowed

def expand_arguments(args, variables):
    out = []

    i = 0
    while i < len(args):
        arg = args[i]

        if i + 1 < len(args):
            m = VAR_RE.fullmatch(args[i + 1])

            if m:
                name = m.group(1)

                value = variables.get(name)

                if value is None or value == "":
                    i += 2
                    continue

                out.extend((arg, str(value)))
                i += 2
                continue

        out.append(arg)
        i += 1

    return out