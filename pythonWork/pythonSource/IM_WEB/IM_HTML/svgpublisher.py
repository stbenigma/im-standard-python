from IM_WEB.IM_HTML import getsvgtext, HTMLExport
from pathlib import Path


def publish_svg_diagrams(config: HTMLExport, language: str) -> dict:
    assert config is not None
    assert config.model is not None
    assert config.model.jsmodel is not None
    model_json = config.model.jsmodel

    # ensure destination folder exists
    destination_folder = Path(config.webDirec) / f'svg-diagrams-{language}'
    destination_folder.mkdir(parents=True, exist_ok=True)
    assert destination_folder.is_dir(), f"Destination path {destination_folder.resolve()} is not a directory"

    results = {}
    for diagram_key, diagram in model_json['diagrams'].items():
        svg_content = getsvgtext(export=config, plang=language,
                                 pdiaganker=diagram_key, pdiagelem=diagram, ptitle=diagram['name'])
        outfile = destination_folder / f"{diagram['name']}-{diagram_key}.svg"
        with open(outfile, "w") as dest:
            dest.write(svg_content)
        results[diagram_key] = outfile
        print(f"Wrote diagram {diagram_key} to {outfile}")

    return results
