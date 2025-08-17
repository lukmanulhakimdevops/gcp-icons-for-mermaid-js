#!/usr/bin/env python3
# Copyright (c) 2020 David Holsgrove
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT (For details, see https://github.com/davidholsgrove/gcp-icons-for-plantuml/blob/master/LICENSE-CODE)

"""icon-builder.py: Build GCP Icons for PlantUML"""

import os
import argparse
import sys
import subprocess
import shutil
import multiprocessing
from multiprocessing import Pool
from pathlib import Path
from subprocess import PIPE
from datetime import datetime, timezone
import json
import re
import xml.etree.ElementTree as ET
from lxml import etree
import base64
import yaml

from gcpicons.icon import Icon

# used to inject into gcp-icons-mermaid.json
release_version = "20.0"
release_date_obj = datetime.strptime("2025-02-07", "%Y-%m-%d")
release_utc_seconds = int(release_date_obj.replace(tzinfo=timezone.utc).timestamp())


def verify_environment():
    """Test all dependencies to verify that builder can run correctly"""
    global config
    cur_dir = Path(".")
    if str(cur_dir.absolute()).split("/")[-2:] != ["gcp-icons-for-plantuml", "scripts"]:
        print("Working directory must be gcp-icons-for-plantuml/scripts")
        sys.exit(1)
    try:
        with open("config.yml") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: {e}\ncheck config.yml file")
        sys.exit(1)
    if not Path("../source/GCPCommon.puml").exists():
        print("File GCPCommon.puml not found in source/")
        sys.exit(1)
    if not Path("../source/official").exists():
        print("source/official must contain folders of GCP icons")
        sys.exit(1)
    try:
        subprocess.run(
            ["java", "-jar", "./plantuml.jar", "-version"],
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
    except Exception as e:
        print(f"Error executing plantuml jar file, {e}")
        sys.exit(1)
    if args["check_env"]:
        print("Prerequisites met, exiting")
        exit(0)


def clean_dist():
    path = Path("../dist")
    if path.exists():
        shutil.rmtree(path)
    os.mkdir(path)


def copy_puml():
    for file in Path(".").glob("../source/*.puml"):
        shutil.copy(file, Path("../dist"))


def build_file_list():
    return sorted(Path("../source/official").glob("**/*.png"))


def build_mermaid_icon(mermaid, filename, cat, mermaid_target):
    """add an icon (SVG or PNG) to the mermaid object"""
    body, width, height = None, 64, 64
    if filename.endswith(".svg") and Path(filename).exists():
        try:
            svg_parser = etree.XMLParser(remove_blank_text=True)
            svg_tree = etree.parse(filename, svg_parser)
            svg_root = svg_tree.getroot()
            width = int(svg_root.get("width").strip("px"))
            height = int(svg_root.get("height").strip("px"))
            ET.register_namespace('', "http://www.w3.org/2000/svg")
            ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
            svg_body = ''.join(
                (ET.tostring(child, encoding='unicode', method='xml')
                 for child in svg_root if child.tag != '{http://www.w3.org/2000/svg}title')
            )
            body = re.sub(r'\sxmlns[^"]*"[^"]*"', '', svg_body)
        except Exception as e:
            print(f"Error parsing SVG {filename}: {e}")
            return
    elif filename.endswith(".png") and Path(filename).exists():
        try:
            with open(filename, "rb") as f:
                png_data = f.read()
            body = "data:image/png;base64," + base64.b64encode(png_data).decode("utf-8")
        except Exception as e:
            print(f"Error reading PNG {filename}: {e}")
            return
    else:
        print(f"Unsupported or missing file: {filename}")
        return

    mermaid["info"]["total"] += 1
    if mermaid["categories"].get(cat) is None:
        mermaid["categories"][cat] = []
    mermaid["categories"][cat].append(mermaid_target)
    mermaid["icons"][mermaid_target] = {"body": body, "width": width, "height": height}


def worker(icon):
    """multiprocess resource intensive operations (java subprocess)"""
    print(f"generating PUML for {icon.source_name}", flush=True)
    icon.generate_image(
        Path(f"../dist/{icon.category}"),
        color=True,
        max_target_size=128,
        transparency=False,
    )
    icon.generate_puml(Path(f"../dist/{icon.category}"))
    icon.generate_image(
        Path(f"../dist/{icon.category}"),
        color=True,
        max_target_size=128,
        transparency=True,
    )
    return


def main():
    verify_environment()
    clean_dist()
    copy_puml()

    source_files = build_file_list()
    icons = [Icon(filename, config) for filename in source_files]

    categories = sorted(set([icon.category for icon in icons]))
    for i in categories:
        Path(f"../dist/{i}").mkdir(exist_ok=True)

    pool = Pool(processes=multiprocessing.cpu_count())
    for i in icons:
        pool.apply_async(worker, args=(i,))
    pool.close()
    pool.join()

    sorted_icons = sorted(icons, key=lambda x: (x.category, x.target))
    markdown = ["# GCP Symbols\n\n"]
    structerizr = {"name": "GCP Icons Structurizr theme", "elements": []}
    mermaid = {
        "prefix": "gcp",
        "info": {"name": "GCP Icons", "total": 0, "version": release_version},
        "lastModified": release_utc_seconds,
        "width": 64,
        "height": 64,
        "icons": {},
        "categories": {}
    }

    for j in sorted_icons:
        cat, tgt = j.category, j.target
        markdown.append(f"{cat} | {tgt} | ![{tgt}](dist/{cat}/{tgt}.png?raw=true) | {cat}/{tgt}.puml\n")
        structerizr["elements"].append({"tag": tgt, "stroke": "#4284F3", "icon": f"{cat}/{tgt}.png"})
        try:
            svg_filename = re.sub(r'\.png$', '.svg', str(j.filename))
            if Path(svg_filename).exists():
                build_mermaid_icon(mermaid, svg_filename, cat, tgt)
            else:
                build_mermaid_icon(mermaid, str(j.filename), cat, tgt)
        except Exception as e:
            print(f"Error: {e} adding {tgt} to gcp-icons-mermaid.json")

    with open(Path("../GCPSymbols.md"), "w") as f:
        f.write(''.join(markdown))
    with open(Path("../dist/gcp-icons-structurizr-theme.json"), "w") as f:
        f.write(json.dumps(structerizr, indent=2))
    with open(Path("../dist/gcp-icons-mermaid.json"), "w") as f:
        f.write(json.dumps(mermaid, indent=2))

    print("✅ Semua ikon & JSON berhasil diproses.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates GCP icons for PlantUML")
    parser.add_argument("--check-env", action="store_true", default=False)
    args = vars(parser.parse_args())
    main()
