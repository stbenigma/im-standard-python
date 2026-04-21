#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MiroSync  –  UI-JSON ↔ Miro Board Synchronisation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Verwendung als Klasse:
    from miro_sync import MiroSync
    miro = MiroSync(token="eyJ...", board_id="uXjVI...")
    miro.push("diagram.json")
    miro.pull("3458764598765432", out_file="export.json")

Verwendung als CLI:
    python miro_sync.py boards
    python miro_sync.py frames [board-id]
    python miro_sync.py push diagram.json [board-id]
    python miro_sync.py pull <frame-id> [board-id] [output.json]

Konfiguration via Umgebungsvariablen:
    export MIRO_TOKEN="eyJ..."
    export BOARD_ID="uXjVI..."        # optional
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import datetime
from typing import Any

# requests ist deutlich komfortabler als urllib – Fallback mit Hinweis
try:
    import requests
except ImportError:
    sys.exit(
        "❌  'requests' fehlt.\n"
        "    Installation: pip install requests"
    )


# ── Farben ────────────────────────────────────────────────
class _C:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def _info(msg: str) -> None: print(f"{_C.BLUE}ℹ{_C.RESET}  {msg}")


def _ok(msg: str) -> None: print(f"{_C.GREEN}✓{_C.RESET}  {msg}")


def _warn(msg: str) -> None: print(f"{_C.YELLOW}⚠{_C.RESET}  {msg}")


def _err(msg: str) -> None: print(f"{_C.RED}✗{_C.RESET}  {msg}", file=sys.stderr)


def _bold(s: str) -> str:  return f"{_C.BOLD}{s}{_C.RESET}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class MiroSyncError(Exception):
    """Wird bei API-Fehlern oder Konfigurationsproblemen geworfen."""


class MiroSync:
    """
    Synchronisiert UI-JSON-Diagramme mit Miro Boards.

    Args:
        token:    Miro API-Token (oder via Env-Variable MIRO_TOKEN)
        board_id: Standard-Board-ID (oder via Env-Variable BOARD_ID)
    """

    API = "https://api.miro.com/v2"
    SHAPES = {"Entity": "round_rectangle"}

    def _unshape(self, shape):
        return {val: key for key, val in self.SHAPES.items()}.get(shape, "Entity")

    def __init__(self, token: str = "", board_id=None) -> None:
        self.token = token or os.environ.get("MIRO_TOKEN", "")
        self.board_id = board_id or os.environ.get("BOARD_ID", "")

        if not self.token:
            raise MiroSyncError(
                "Kein API-Token gesetzt.\n"
                "  Option 1: MiroSync(token='eyJ...')\n"
                "  Option 2: export MIRO_TOKEN='eyJ...'\n\n"
                "Token erstellen:\n"
                "  1. https://miro.com/settings/profile → Your apps → Create new app\n"
                "  2. OAuth scopes: boards:read  boards:write\n"
                "  3. Install to team → Access token kopieren"
            )

        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    # ── Interne API-Hilfsmethoden ──────────────────────────

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        url = self.API + endpoint
        resp = self._session.get(url, params=params)
        self._raise_for_status(resp)
        return resp.json()

    def _post(self, endpoint: str, payload: dict) -> dict:
        url = self.API + endpoint
        resp = self._session.post(url, json=payload)
        self._raise_for_status(resp)
        return resp.json()

    @staticmethod
    def _raise_for_status(resp: requests.Response) -> None:
        if resp.status_code >= 400:
            try:
                body = resp.json()
                msg = body.get("message") or body.get("error") or str(body)
                for v in body.get("context", {}).values():
                    msg += "\n" + str(v)
            except Exception as e:
                msg = resp.text or f"HTTP {resp.status_code}"
            raise MiroSyncError(f"Miro API Fehler ({resp.status_code}): {msg}")

    def _get_paginated(self, endpoint: str, params: dict | None = None) -> list[dict]:
        """Lädt alle Seiten eines paginierten Endpoints."""
        items: list[dict] = []
        offset: str = None
        cursor: str = None
        while True:
            p = dict(params or {})
            p["limit"] = 50
            if offset:
                p["offset"] = offset
            if cursor:
                p["cursor"] = cursor
            page = self._get(endpoint, params=p)
            items += page.get("data", [])
            try:
                nextlink = page.get("links", dict()).get("next")
                if nextlink.find("offset=") > -1:
                    offset = str(nextlink.split("offset=")[1])
                elif nextlink.find("cursor=") > -1:
                    cursor = self._unescape(str(nextlink.split("cursor=")[1]))
                else:
                    break
            except:
                break
        return items

    # def get_flowchart_shapes(self, board_id: str = "", frame_id: str = "") -> list[dict]:
    #     """Liest Flowchart-Shapes über den experimentellen Endpoint."""
    #     bid = self._resolve_board(board_id)
    #     # Experimenteller Header erforderlich
    #     resp = self._session.get(
    #         f"{self.API}/boards/{bid}/items",
    #         params={"type": "shape", "parent_item_id": frame_id, "limit": 50},
    #         headers={"X-Miro-Experimental": "true"}
    #     )
    #     self._raise_for_status(resp)
    #     all_shapes = resp.json().get("data", [])
    #     # Nur echte Flowchart-Shapes zurückgeben
    #     return [s for s in all_shapes if s.get("data", {}).get("shape", "").startswith("flow_chart_")]
    #
    def _resolve_board(self, board_id=None) -> str:
        bid = board_id or self.board_id
        if not bid:
            raise MiroSyncError(
                "Keine Board-ID angegeben.\n"
                "  Option 1: MiroSync(board_id='uXjVI...')\n"
                "  Option 2: export BOARD_ID='uXjVI...'\n"
                "  Option 3: Als Argument übergeben.\n"
                "  Boards auflisten: miro.boards()"
            )
        return bid

    # ── Statische Hilfsmethoden ────────────────────────────

    @staticmethod
    def _unescape(text: str) -> str:
        """Entfernt HTML-Tags und dekodiert Entities."""
        text = re.sub(r"%3D", "=", text or "")
        text = re.sub(r"%20", " ", text or "")
        text = html.unescape(text)
        return text.strip()

    @staticmethod
    def _strip_html(text: str, psep=" ") -> str:
        """Entfernt HTML-Tags und dekodiert Entities."""
        # replace </p><p> (Zeilenumbruch durch ein blank)
        text = re.sub(r"</p><p>", psep, text or "")
        text = re.sub(r"<[^>]+>", "", text or "")
        return MiroSync._unescape(text)

    @staticmethod
    def _makepercent(pos: Any):
        if type(pos) == dict:
            return {key: MiroSync._makepercent(val) for key, val in pos.items()}
        else:
            """fügt '%' hinzu  '100' → '100%'."""
            val = str(pos)
            return val + ("" if val.endswith("%") else "%")

    @staticmethod
    def _clean_position(pos: Any):
        if type(pos) == dict:
            return {key: MiroSync._clean_position(val) for key, val in pos.items()}
        else:
            """Entfernt '%' aus Caption-Positionswerten: '100%' → '100'. und rundet auf 1 Stelle"""
            return round(float(re.sub(r"%", "", str(pos or "50"))), 1)

    @staticmethod
    def _hex(color: str) -> str:
        """Stellt sicher, dass die Farbe mit '#' beginnt."""
        c = (color or "4c84ff").lstrip("#")
        return f"#{c}"

    @staticmethod
    def _hex_bare(color: str) -> str:
        """Gibt die Farbe ohne '#' zurück (für JSON-Speicherung)."""
        return (color or "#4c84ff").lstrip("#")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ÖFFENTLICHE METHODEN
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def get_shapes(self, board_id, frame_id):
        all_items = self._get_paginated(
            f"/boards/{board_id}/items",
            params={"parent_item_id": frame_id},
        )
        shapes = [it for it in all_items if it.get("type") == "shape"]
        return shapes

    def get_texts(self, board_id=None, frame_id: str = "") -> list[dict]:
        """Liest alle Textfelder eines Frames."""
        bid = self._resolve_board(board_id)
        params = {"type": "text"}
        if frame_id:
            params["parent_item_id"] = frame_id
        items = self._get_paginated(f"/boards/{bid}/items", params=params)
        return [
            {
                "id": t["id"],
                "text": self._strip_html(t.get("data", {}).get("content", ""), psep=","),
                "displtext": self._unescape(t.get("data", {}).get("content", "")),
                "x": t.get("position", {}).get("x", 0),
                "y": t.get("position", {}).get("y", 0),
                "width": t.get("geometry", {}).get("width", 0),
                "height": t.get("geometry", {}).get("height", 0),
                "style": t.get("style", {}),
            }
            for t in items
        ]

    def get_item_text(self, item_id, groups: list[dict], texts: list[dict]):
        mygroups = [g.get("data", {}).get("items") for g in groups if item_id in g.get("data", {}).get("items")]
        textids = set([t.get("id") for t in texts])
        for mg in mygroups:
            mytextid = textids & set(mg)
            if len(mytextid) == 1:
                return [t for t in texts if t.get("id") == list(mytextid)[0]]
        return None

    def get_groups(self, itemlist: list = []) -> list[dict]:
        """Liest alle Gruppen eines Boards/Frames mit ihren Item-IDs."""
        bid = self._resolve_board(self.board_id)

        # Alle Gruppen des Boards
        all_groups = self._get_paginated(f"/boards/{bid}/groups")

        # Auf Frame einschränken: nur Gruppen behalten,
        # deren Items im Frame liegen
        return [
            g for g in all_groups
            if all(item_id in itemlist
                   for item_id in g.get("data", {}).get("items", []))
        ]

    def post_text(self, content:str,
                  x: float,
                  y: float,
                  fontSize: int = 10,
                  textAlign: str = "left"
                  ):
        payload = {
            "data": {
                "content": content
            },
            "style": {
                "color": "#1a1a1a",
                "fillColor": "#e7e7e7", #lightGray
                "fontSize": fontSize,
                "textAlign": textAlign
            },
            "position": {
                "x": x,
                "y": y,
                "origin": "center"
            }
            #"geometry": {
            #    "width": 200
            #}
        }
        try:
            resp = self._post(f"/boards/{self.board_id}/texts", payload)
            text_id = resp.get("id", "")
        except MiroSyncError as e:
            text_id = None
            _warn(f"  [group creation failed: {e}")
        return text_id

    def post_group(self, idlist: list):
        payload = {
            "data": {
                "items": idlist
            }
        }
        try:
            resp = self._post(f"/boards/{self.board_id}/groups", payload)
            conn_id = resp.get("id", "")
        except MiroSyncError as e:
            conn_id = None
            _warn(f"  [group creation failed: {e}")
        return conn_id

    def boards(self, filter: str) -> list[dict]:
        """
        Gibt alle verfügbaren Miro-Boards zurück.

        param: filter:str regexp to be matched
        Returns:
            Liste von Dicts mit 'id' und 'name'.
        """
        _info("Lade Boards …")
        result = self._get_paginated("/boards")
        foundboards = [b for b in result if re.match(filter, b.get("name"))]
        _info(f"{len(foundboards)} Board(s) gefunden")
        return foundboards

    def frames(self, board_id=None, filter: str = "") -> list[dict]:
        """
        Gibt alle Frames eines Boards zurück.

        Args:
            board_id: Board-ID (überschreibt self.board_id)

        Returns:
            Liste von Dicts mit 'id', 'name', 'width', 'height'.
        """
        bid = self._resolve_board(board_id)
        _info(f"Lade Frames für Board {_bold(bid)} …")
        result = self._get_paginated(f"/boards/{bid}/frames")
        frames = [
            {
                "id": f["id"],
                "name": f.get("data", {}).get("title", ""),
                "width": f.get("geometry", {}).get("width", 0),
                "height": f.get("geometry", {}).get("height", 0),
            }
            for f in result if re.match(filter, f.get("data", {}).get("title", ""))
        ]
        _info(f"{len(frames)} Frame(s) gefunden")
        return frames

    def push(self, json_file: str, board_id=None,withexamples=False) -> str:
        """
        Lädt ein UI-JSON als Miro-Frame hoch.

        Args:
            json_file: Pfad zur JSON-Datei
            board_id:  Ziel-Board-ID (überschreibt self.board_id)

        Returns:
            Frame-ID des neu erstellten Frames.
        """
        if board_id is not None:
            self.board_id = board_id
        bid = self._resolve_board(board_id)

        if not os.path.isfile(json_file):
            raise MiroSyncError(f"File not found: {json_file}")

        _info(f"Lese {_bold(json_file)} …")
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)

        name = data.get("name", "Diagram")
        elements = data.get("elements", {}).get("elements", [])
        rels = data.get("elements", {}).get("relationships", [])
        total_w = data.get("width", 700)
        total_h = data.get("height", 900)
        frame_x = data.get("x", 0)
        frame_y = data.get("y", 0)

        _info(f"Diagram: {_bold(name)}  |  {len(elements)} elements, {len(rels)} relations")
        print()

        # 1. Frame anlegen ─────────────────────────────────
        _info("Erstelle Frame …")
        frame = self._post(f"/boards/{bid}/frames", {
            "data": {"title": name, "format": "custom",
                     "type": "freeform", "showContent": True},
            "geometry": {"width": total_w, "height": total_h},
            "position": {"x": frame_x, "y": frame_y, "origin": "center"},
        })
        frame_id = frame["id"]
        _ok(f"Frame erstellt: {_bold(frame_id)}")
        print()

        # 2. Shapes (Systeme) anlegen ──────────────────────
        # Mapping: elementid → neue Miro-Shape-ID
        id_map: dict[str, str] = {}

        for i, elem in enumerate(elements, 1):
            eid = elem.get("elementid", f"sys_{i}")
            sname = elem.get("name", eid)
            dname = elem.get("displname")
            examples = elem.get("examples")
            shape = self.SHAPES.get(elem.get("type", "Entity"))
            x = float(elem.get("pos_x", 0))
            y = float(elem.get("pos_y", 0))
            ui = elem.get("ui", {})
            w = float(ui.get("width", 140))
            h = float(ui.get("height", 60))
            color = self._hex(ui.get("color", "4c84ff"))
            fsize = str(ui.get("fontsize", 14))

            # JSON pos = top-left → Miro pos = center (relativ zu Frame-Top-Left)
            mx = round(x + w / 2, 1)
            my = round(y + h / 2, 1)

            try:
                resp = self._post(f"/boards/{bid}/shapes", {
                    "data": {
                        "shape": shape,
                        "content": dname or f"<p>{sname}</p>",
                    },
                    "style": {
                        "fillColor": color,
                        "borderColor": "#aaaaaa",
                        "textAlign": "center",
                        "textAlignVertical": "middle",
                        "fontSize": fsize,
                        "color": "#000000",
                    },
                    "position": {"x": mx, "y": my, "origin": "center"},
                    "geometry": {"width": w, "height": h},
                    "parent": {"id": frame_id},
                })
                shape_id = resp["id"]
                id_map[eid] = shape_id
                _info(f"  [{i}/{len(elements)}] {_bold(sname)}")
            except MiroSyncError as e:
                shape_id = None
                _warn(f"  [{i}/{len(elements)}] Fehlgeschlagen: {sname} – {e}")

            # TODO self.write_text() position lower level corner of item
            if withexamples and examples:
                text_id = self.post_text(content="".join([f"<p>{ex}</p>" for ex in examples]),
                                         x=round(x + w * 0.95)+frame_x,
                                         y=round(y + h/2 * 0.95 +frame_y)
                                         )
                if shape_id and text_id:  # if i have item and Text
                    self.post_group([shape_id, text_id])

        print()

        # 3. Connectors anlegen ────────────────────────────
        if rels:
            _info("Erstelle Verbindungen …")
            for j, rel in enumerate(rels, 1):
                from_eid = rel.get("fromElement", "")
                to_eid = rel.get("toElement", "")
                from_mid = id_map.get(from_eid)
                to_mid = id_map.get(to_eid)

                if not from_mid or not to_mid:
                    _warn(f"  [{j}/{len(rels)}] IDs nicht gefunden: {from_eid} → {to_eid}")
                    continue

                # Captions: neues Format bevorzugen, legacy 'label' als Fallback
                captions_raw = rel.get("captions", [])
                if captions_raw:
                    captions = [
                        {
                            "content": c.get("content", ""),
                            "position": self._makepercent(c.get("position", "50")),
                        }
                        for c in captions_raw
                    ]
                elif rel.get("label"):
                    captions = [{"content": rel["label"], "position": "50%"}]
                else:
                    captions = []

                # Andockpunkte: startSnap / endSnap übernehmen
                start_item: dict = {"id": from_mid}
                end_item: dict = {"id": to_mid}
                for snap_key, item in [("startposition", start_item), ("endposition", end_item)]:
                    item["position"] = self._makepercent(rel.get(snap_key, {"x": "50.0", "y": "50.0"}))

                payload: dict = {
                    "startItem": start_item,
                    "endItem": end_item,
                    "shape": rel.get("shape", "elbowed")
                }
                if rel.get("style"):
                    payload["style"] = rel.get("style")

                if captions:
                    payload["captions"] = captions

                try:
                    resp = self._post(f"/boards/{bid}/connectors", payload)
                    conn_id = resp.get("id", "")
                    if conn_id:
                        _info(f"  [{j}/{len(rels)}] {from_eid} → {to_eid}")
                    else:
                        _warn(f"  [{j}/{len(rels)}] Keine ID zurückgegeben")
                except MiroSyncError as e:
                    _warn(f"  [{j}/{len(rels)}] Fehlgeschlagen: {e}")

            print()

        _ok("Fertig!")
        print()
        print(f"  Frame-ID:  {_bold(frame_id)}")
        print(f"  Board-URL: {_C.BLUE}https://miro.com/app/board/{bid}/{_C.RESET}")
        print()
        print(f"  Pull-Befehl:")
        print(f"  {_C.YELLOW}python miro_sync.py pull {frame_id} {bid} export.json{_C.RESET}")
        print()
        return frame_id

    def _relaname(self,fromid:str,toid:str,captions:list,elements:list):
        names={e.get("elementid"):e.get("name") for e in elements}
        verb = self._strip_html(captions[0].get("content"))
        if verb.startswith("/") and verb.endswith("/"):
            verb=self._strip_html(captions[1].get("content"))
        return f'{names.get(fromid, "??")}->{verb}->{names.get(toid, "??")}'

    def pull(
            self,
            frame_id: str,
            board_id=None,
            out_file: str = "output.json",
            contenttype: str = "Entity"
    ) -> dict:
        """
        Exportiert einen Miro-Frame als UI-JSON.

        Args:
            frame_id: ID des Miro-Frames
            board_id: Board-ID (überschreibt self.board_id)
            out_file: Pfad der Ausgabedatei (Standard: output.json)

        Returns:
            Das erzeugte UI-JSON als Dict.
        """
        if board_id is not None:
            self.board_id = board_id
        bid = self._resolve_board(board_id)

        # Frame-Metadaten
        _info(f"Lade Frame {_bold(frame_id)} …")
        frame_data = self._get(f"/boards/{bid}/frames/{frame_id}")
        frame_title = frame_data.get("data", {}).get("title", "Diagram")
        frame_w = round(frame_data.get("geometry", {}).get("width", 700), 1)
        frame_h = round(frame_data.get("geometry", {}).get("height", 900), 1)
        frame_x = round(frame_data.get("position", {}).get("x", 0), 1)
        frame_y = round(frame_data.get("position", {}).get("y", 0), 1)
        _info(f"Frame: {_bold(frame_title)}  ({frame_w} × {frame_h})")

        # Shapes laden
        _info("Lade Shapes …")
        shapes = self.get_shapes(board_id=bid, frame_id=frame_id)
        shape_ids = {s["id"] for s in shapes}
        _info(f"{len(shapes)} Shapes gefunden")

        # TODO flowshapes= self.get_flowchart_shapes(board_id=board_id,frame_id=frame_id)

        # Connectors laden (eigener Endpoint – nicht Teil von /items)
        _info("Lade Connectors …")
        all_connectors = self._get_paginated(f"/boards/{bid}/connectors")

        # Nur Connectors behalten, bei denen beide Enden im Frame liegen
        frame_connectors = [
            c for c in all_connectors
            if c.get("startItem", {}).get("id") in shape_ids
               and c.get("endItem", {}).get("id") in shape_ids
        ]
        _info(f"{len(frame_connectors)} Connectors im Frame")
        print()

        # lade alle texte und gruppen
        texts = self.get_texts(frame_id=frame_id)
        groups = self.get_groups(itemlist=list(shape_ids) + [t.get("id") for t in texts])
        # Shapes → Elements
        elements: list[dict] = []
        for shape in shapes:
            # lade text zu shape
            examples = self.get_item_text(item_id=shape.get("id"),
                                          groups=groups, texts=texts)
            example = None if examples is None else examples[0].get("text").split(",")
            pos = shape.get("position", {})
            geo = shape.get("geometry", {})
            sty = shape.get("style", {})
            w = float(geo.get("width", 140))
            h = float(geo.get("height", 60))
            # Miro center → top-left
            px = float(pos.get("x", 0)) - w / 2
            py = float(pos.get("y", 0)) - h / 2

            raw_color = sty.get("fillColor", "#4c84ff")
            raw_fcolor = sty.get("color", "#000000")
            raw_fsize = sty.get("fontSize", "14")
            fsize_num = int(re.sub(r"[^0-9]", "", str(raw_fsize)) or "14")

            elements.append({
                "elementid": shape["id"],
                "name": self._strip_html(shape.get("data", {}).get("content", "")),
                "displname": self._unescape(shape.get("data", {}).get("content", "")),
                "examples": example,
                "type": self._unshape(shape.get("data", {}).get("shape")),
                "index": 0,
                "pos_x": round(px, 1),
                "pos_y": round(py, 1),
                "srclink": None,
                "ui": {
                    "width": w,
                    "height": h,
                    "opacity": "1.0",
                    "color": self._hex_bare(raw_color),
                    "marginwidth": 2,
                    "marginopacity": 0,
                    "margincolor": "000000",
                    "fontsize": fsize_num,
                    "fontcolor": self._hex_bare(raw_fcolor),
                },
            })

        # Connectors → relationships
        relationships: list[dict] = []
        for conn in frame_connectors:
            start = conn.get("startItem", {})
            end = conn.get("endItem", {})

            captions = [
                {
                    "content": c.get("content", ""),
                    "position": self._clean_position(c.get("position", "50")),
                }
                for c in conn.get("captions", [])
            ]

            relationships.append({
                "elementid": conn["id"],
                "name":self._relaname(fromid=start.get("id", ""),
                                      toid=end.get("id", ""),
                                      captions=captions,elements=elements),
                "fromElement": start.get("id", ""),
                "toElement": end.get("id", ""),
                "captions": captions,
                "shape": conn.get("shape"),
                "startposition": self._clean_position(start.get("position")),
                "endposition": self._clean_position(end.get("position")),
                "style": conn.get("style", {})
            })

        # UI-JSON zusammenbauen
        result = {
            "elementid": frame_id,
            "name": frame_title,
            "type": contenttype,
            "width": frame_w,
            "height": frame_h,
            "x": frame_x,
            "y": frame_y,
            "dc": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23],
            "srclink": None,
            "elements": {
                "categories": [],
                "elements": elements,
                "relationships": relationships
            },
        }

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        _ok(f"{len(elements)} Elements, {len(relationships)} Relations")
        _ok(f"Gespeichert: {_bold(out_file)}")
        print()
        return result


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _print_boards(boards: list[dict]) -> None:
    print()
    print(f"{_C.BOLD}Miro-Boards:{_C.RESET}")
    print("─" * 52)
    for b in boards:
        print(f"  {b['id']}  {b['name']}")
    print("─" * 52)
    print(f"  {len(boards)} Board(s)")
    print()
    print(f"  Tipp: {_C.YELLOW}export BOARD_ID='<board-id>'{_C.RESET}")
    print()


def _print_frames(frames: list[dict], board_id: str) -> None:
    print()
    print(f"{_C.BOLD}Frames auf Board {board_id}:{_C.RESET}")
    print("─" * 66)
    print(f"  {'Name':<30}  {'Frame-ID':<22}  Size")
    print("─" * 66)
    for fr in frames:
        size = f"{int(fr['width'])} × {int(fr['height'])}"
        print(f"  {fr['name']:<30}  {fr['id']:<22}  {size}")
    print("─" * 66)
    print(f"  {len(frames)} Frame(s) found")
    print()
    print(f"  Pull:")
    print(f"  {_C.YELLOW}python miro_sync.py pull <frame-id> {board_id} export.json{_C.RESET}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="miro_sync.py",
        description="UI-JSON ↔ Miro Synchronisation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Konfiguration:\n"
            "  export MIRO_TOKEN='eyJ...'       # Optional\n"
            "  export BOARD_ID='uXjVI...'       # Optional\n\n"
            "Examples:\n"
            "  python miro_sync.py boards -t <token>\n"
            "  python miro_sync.py frames uXjVKabc123= -t <token>\n"
            "  python miro_sync.py push diagram.json uXjVKabc123= -t <token>\n"
            "  python miro_sync.py pull 3458764598765432 uXjVKabc123= export.json"
        ),
    )
    parser.add_argument("-t", "--token", help="Authentification token (default $MIRO_TOKEN)", type=str)
    parser.add_argument("-f", "--filter", help="regexp to filter board or frame names", type=str)
    sub = parser.add_subparsers(dest="cmd", metavar="COMMAND")

    # boards
    sub.add_parser("boards", help="List Miro-Boards")

    # frames
    p_frames = sub.add_parser("frames", help="List frames of a board")
    p_frames.add_argument("board_id", nargs="?", default="",
                          help="Board-ID (default: $BOARD_ID)")

    # push
    p_push = sub.add_parser("push", help="JSON-file to upload")
    p_push.add_argument("json_file", help="Path to UI-JSON-file")
    p_push.add_argument("board_id", nargs="?", default="",
                        help="Board-ID (default: $BOARD_ID)")

    # pull
    p_pull = sub.add_parser("pull", help="Miro-Frame als JSON exportieren")
    p_pull.add_argument("frame_id", help="Miro Frame-ID")
    p_pull.add_argument("board_id", nargs="?", default="",
                        help="Board-ID (Standard: $BOARD_ID)")
    p_pull.add_argument("out_file", nargs="?", default="output.json",
                        help="Outputfile (default: output.json)")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        sys.exit(0)

    try:
        miro = MiroSync(token=args.token)

        if args.cmd == "boards":
            _print_boards(miro.boards(filter=args.filter))

        elif args.cmd == "frames":
            bid = args.board_id or miro.board_id
            frames = miro.frames(filter=args.filter)
            _print_frames(frames, bid)

        elif args.cmd == "push":
            miro.push(args.json_file, args.board_id)

        elif args.cmd == "pull":
            miro.pull(args.frame_id, args.board_id, args.out_file)

    except MiroSyncError as e:
        _err(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAbgebrochen.")
        sys.exit(0)


def boards(token=None, filter=None):
    miro = MiroSync(token=token)
    return miro.boards(filter=filter)


def frames(boardid, token=None, filter=None):
    miro = MiroSync(token=token)
    return miro.frames(board_id=boardid, filter=filter)


if __name__ == "__main__":
    main()
