"""Link repository hooks into Codex home without replacing existing entries."""

import argparse
import os
from pathlib import Path


def install(codex_dir):
    repo = Path(__file__).resolve().parent.parent
    pairs = [(repo / "hooks/hooks.json", codex_dir / "hooks.json"),
             (repo / "hooks/scripts", codex_dir / "hooks"),
             (repo / "policies", codex_dir / "policies")]
    # Preflight all destinations before making any changes.
    missing = []
    for source, target in pairs:
        if not source.exists():
            raise FileNotFoundError(f"Missing source: {source}")
        if target.is_symlink() and target.resolve() == source.resolve():
            continue
        if os.path.lexists(target):
            raise FileExistsError(f"Not overwritten: {target}; merge or move it manually")
        missing.append((source, target))
    codex_dir.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for source, target in missing:
            target.symlink_to(source, target_is_directory=source.is_dir())
            created.append(target)
    except OSError:
        for target in reversed(created):
            target.unlink()
        raise
    for source, target in pairs:
        print(f"Linked: {target} -> {source}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path,
                        default=Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex"))
    args = parser.parse_args()
    try:
        install(args.codex_home.expanduser().absolute())
    except OSError as error:
        parser.exit(1, f"{error}\nOn Windows, symbolic links require Developer Mode or elevation.\n")
