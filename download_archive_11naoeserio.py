#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://archive.org/details/11naoeserio"
DEFAULT_DEST = "/home/temoteo/Músicas/charlie brown jr"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Baixa todos os arquivos de download encontrados em https://archive.org/details/11naoeserio"
    )
    parser.add_argument("--url", default=DEFAULT_URL, help="URL da página Archive.org")
    parser.add_argument("--dest", default=DEFAULT_DEST, help="Pasta de destino para os downloads")
    parser.add_argument(
        "--ext",
        default="mp3",
        help="Extensão do arquivo a baixar (padrão: mp3). Use 'all' para baixar qualquer formato.",
    )
    return parser.parse_args()


def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def extract_download_links(soup: BeautifulSoup, base_url: str, ext: str):
    links = []
    for a in soup.select("a.stealth.download-pill"):
        href = a.get("href")
        if not href:
            continue
        href = href.strip()
        if href.startswith("#"):
            continue
        if not href.startswith("http"):
            href = urljoin(base_url, href)

        if ext != "all":
            if not href.lower().endswith(f".{ext.lower()}"):
                continue

        links.append(href)

    return links


def sanitize_filename(filename: str) -> str:
    return "".join(ch for ch in filename if ch not in "<>:\\/?*|\"\n\r").strip()


def download_file(url: str, dest_folder: Path):
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename:
        raise ValueError(f"Não foi possível determinar o nome do arquivo para URL: {url}")
    filename = sanitize_filename(filename)
    dest_path = dest_folder / filename

    if dest_path.exists():
        print(f"Já existe: {dest_path}")
        return dest_path

    print(f"Baixando: {url}")
    with requests.get(url, headers=HEADERS, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        dest_folder.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"Salvo em: {dest_path}")
    return dest_path


def main():
    args = parse_args()
    dest_folder = Path(args.dest)
    soup = get_soup(args.url)
    links = extract_download_links(soup, args.url, args.ext)

    if not links:
        print("Nenhum link de download encontrado. Verifique a URL ou a estrutura da página.")
        sys.exit(1)

    print(f"Encontrados {len(links)} links. Iniciando downloads...")
    for link in links:
        try:
            download_file(link, dest_folder)
        except Exception as exc:
            print(f"Erro ao baixar {link}: {exc}")


if __name__ == "__main__":
    main()