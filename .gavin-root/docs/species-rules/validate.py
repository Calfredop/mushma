"""Lint the draft species rule config until M3's real loader replaces it.

Run from the repo root:
    uv run --with pyyaml --with jsonschema --with referencing \
        python .gavin-root/docs/species-rules/validate.py
"""

import json
import pathlib
import sys

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match

HERE = pathlib.Path(__file__).parent
SPECIES_SCHEMA = json.loads((HERE / "species.schema.json").read_text())
REFS_SCHEMA = json.loads((HERE / "references.schema.json").read_text())
KINDS = [r["$ref"].split("f_", 1)[1] for r in SPECIES_SCHEMA["$defs"]["factor"]["oneOf"]]
AVAILABLE = set(SPECIES_SCHEMA["$defs"]["daily_variable_available"]["enum"]) | set(
    SPECIES_SCHEMA["$defs"]["static_attribute_available"]["enum"]
)


def trapezoid_ordered(t: list) -> bool:
    known = [v for v in t if v is not None]
    return known == sorted(known)


def check_species(path: pathlib.Path, refs: dict) -> list[str]:
    errors = []
    doc = yaml.safe_load(path.read_text())
    for e in Draft202012Validator(SPECIES_SCHEMA).iter_errors(doc):
        kind = e.instance.get("kind") if isinstance(e.instance, dict) else None
        if e.context and kind:
            # oneOf over factor kinds: report the branch for this factor's own kind
            branch = [c for c in e.context if c.relative_schema_path[0] == KINDS.index(kind)]
            # a failing allOf marks every property unevaluated; prefer the underlying error
            specific = [c for c in branch if c.validator != "unevaluatedProperties"] or branch
            e = best_match(specific) or e
        errors.append(f"schema: {'/'.join(map(str, e.absolute_path))}: {e.message[:200]}")
    if errors:
        return errors
    if doc["key"] != path.stem:
        errors.append(f"key {doc['key']!r} does not match file name")
    ids = [f["id"] for f in doc["factors"]]
    if len(ids) != len(set(ids)):
        errors.append(f"duplicate factor ids: {ids}")
    roles = {f["role"] for f in doc["factors"] if f.get("enabled", True)}
    if "driver" not in roles:
        errors.append("no enabled driver factor")
    for f in doc["factors"]:
        where = f"factor {f['id']}"
        for s in f["source"]:
            if s not in refs:
                errors.append(f"{where}: unknown source {s!r}")
        response = f.get("response", {})
        for name, t in response.items():
            if not trapezoid_ordered(t):
                errors.append(f"{where}: {name} trapezoid not ordered: {t}")
        inp = f.get("input", {})
        uses = inp.get("variable") or inp.get("attribute")
        if f.get("enabled", True) and uses and uses not in AVAILABLE:
            errors.append(f"{where}: enabled but uses unavailable input {uses!r}")
        if f.get("enabled", True) is False and f["data"] != "missing" and not f.get("notes"):
            errors.append(f"{where}: disabled without notes")
    return errors


def main() -> int:
    refs_doc = yaml.safe_load((HERE / "references.yaml").read_text())
    errors = [f"references.yaml: {e.message[:200]}" for e in Draft202012Validator(REFS_SCHEMA).iter_errors(refs_doc)]
    refs = refs_doc.get("references", {})
    used: set[str] = set()
    files = sorted(p for p in HERE.glob("*.yaml") if p.name != "references.yaml")
    for path in files:
        errs = check_species(path, refs)
        errors += [f"{path.name}: {e}" for e in errs]
        if not errs:
            used |= {s for f in yaml.safe_load(path.read_text())["factors"] for s in f["source"]}
    unused = sorted(set(refs) - used)
    for e in errors:
        print("ERROR", e)
    print(f"{len(files)} species files, {len(refs)} references ({len(unused)} not cited by any rule: {unused})")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
