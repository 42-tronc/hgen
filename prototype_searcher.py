#!/usr/bin/env python3

from pathlib import Path
from prototypes_container import Protos
from colors import cstr, cprint


def crawl_prototypes(src_dir: Path) -> list[Protos]:
    results: list[Protos] = []
    cprint("magenta", f">> from {src_dir}")
    for src in src_dir.glob("**/*.c"):
        status, res = "green", ""
        try:
            target = Protos(src)
            results.append(target)
            res = f"(x{len(target)})"
        except AssertionError:
            status, res = "yellow", "none"
        finally:
            print(f"{cstr(status, f'{res} in')} {cstr('blue', src.name)}")
    if not len(results):
        raise ValueError(
            cstr(
                "red",
                f"no function prototypes found in {src_dir}",
            )
        )
    return results


def align_protos_indentation(protolist: list[Protos]):
    def before_len(proto):
        return len(proto.split("\t")[0])

    def get_longest_prototype_len():
        result = 0
        for container in protolist:
            for proto in container:
                result = max(result, before_len(proto))

        return result + 4  # tabs

    longest = get_longest_prototype_len()

    for container in protolist:
        results = []
        for proto in container:
            to_pad = longest // 4 - before_len(proto) // 4 + 1
            types, name_params = proto.split("\t")
            results.append(types + "\t" * to_pad + name_params)
            container.prototypes = results
            # print(repr(container).replace("\t", r"<==>"))

    # self.prototypes = results


if __name__ == "__main__":
    try:
        results = crawl_prototypes(Path("../so_long/src"))
    except ValueError as e:
        # print(e, "\n====")
        protolist = crawl_prototypes(Path("../so_long/lib/src"))
        align_protos_indentation(protolist)