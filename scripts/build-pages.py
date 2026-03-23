#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/itdojp/ai-agent-engineering-book"
SITE_TITLE = "AIエージェント実践: Prompt / Context / Harness Engineering"


@dataclass(frozen=True)
class SectionSpec:
    key: str
    title: str
    rel_dir: str
    part: bool = False


@dataclass
class Page:
    language: str
    language_label: str
    source_root: Path
    source_path: Path
    section_title: str
    title: str
    excerpt: str
    output_rel: Path
    body_html: str
    toc_html: str


BOOK_SPECS = {
    "ja": {
        "label": "日本語版",
        "lang_attr": "ja",
        "root": ROOT / "manuscript",
        "index_intro": "日本語原稿の front matter、各 Part、appendices、backmatter を web から順に読める reader-facing 版です。",
        "sections": [
            SectionSpec("front-matter", "前付け", "front-matter"),
            SectionSpec("part-00", "Part 0", "part-00"),
            SectionSpec("part-01", "Part 1: Prompt Engineering", "part-01-prompt", part=True),
            SectionSpec("part-02", "Part 2: Context Engineering", "part-02-context", part=True),
            SectionSpec("part-03", "Part 3: Harness Engineering", "part-03-harness", part=True),
            SectionSpec("appendices", "付録", "appendices"),
            SectionSpec("backmatter", "後付け", "backmatter"),
        ],
    },
    "en": {
        "label": "English Edition",
        "lang_attr": "en",
        "root": ROOT / "manuscript-en",
        "index_intro": "A web-facing edition of the English manuscript, organized from front matter through the three parts, appendices, and backmatter.",
        "sections": [
            SectionSpec("front-matter", "Front Matter", "front-matter"),
            SectionSpec("part-00", "Part 0", "part-00"),
            SectionSpec("part-01", "Part 1: Prompt Engineering", "part-01-prompt", part=True),
            SectionSpec("part-02", "Part 2: Context Engineering", "part-02-context", part=True),
            SectionSpec("part-03", "Part 3: Harness Engineering", "part-03-harness", part=True),
            SectionSpec("appendices", "Appendices", "appendices"),
            SectionSpec("backmatter", "Backmatter", "backmatter"),
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a static book site for GitHub Pages.")
    parser.add_argument(
        "--output",
        default=str(ROOT / "dist" / "pages"),
        help="Output directory for the built site.",
    )
    return parser.parse_args()


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + 5 :]


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return fallback


def extract_excerpt(body: str) -> str:
    for block in body.split("\n\n"):
        candidate = " ".join(line.strip() for line in block.splitlines()).strip()
        if not candidate:
            continue
        if candidate.startswith(("#", "```", "|", "-", "1.", "2.", "3.")):
            continue
        return candidate[:180]
    return ""


def page_slug(rel_path: Path) -> str:
    stem = rel_path.stem
    if stem == "part-opener":
        return "part-opener"
    match = re.match(r"^(app-[a-z]+|ch\d+|\d+)", stem)
    if match:
        return match.group(1)
    slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    return slug or "page"


def output_rel(language: str, source_root: Path, source_path: Path) -> Path:
    rel = source_path.relative_to(source_root)
    return Path(language) / rel.parent / f"{page_slug(rel)}.html"


def ordered_section_paths(source_root: Path, section: SectionSpec) -> list[Path]:
    base = source_root / section.rel_dir
    if not base.exists():
        return []
    if section.part:
        paths: list[Path] = []
        opener = base / "part-opener.md"
        if opener.exists():
            paths.append(opener)
        paths.extend(sorted(base.glob("ch*.md")))
        return paths
    return sorted(base.glob("*.md"))


def load_page(language: str, source_root: Path, language_label: str, section: SectionSpec, path: Path) -> Page:
    raw = path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw).strip()
    title = extract_title(body, path.stem)
    md = markdown.Markdown(extensions=["extra", "toc", "sane_lists"])
    body_html = md.convert(body)
    excerpt = extract_excerpt(body)
    return Page(
        language=language,
        language_label=language_label,
        source_root=source_root,
        source_path=path,
        section_title=section.title,
        title=title,
        excerpt=excerpt,
        output_rel=output_rel(language, source_root, path),
        body_html=body_html,
        toc_html=md.toc if md.toc else "",
    )


def rel_link(from_rel: Path, to_rel: Path) -> str:
    return os.path.relpath(to_rel, start=from_rel.parent).replace(os.sep, "/")


def code_literal(text: str) -> str:
    return f"<code>{html.escape(text)}</code>"


def render_nav(pages: list[Page], current: Page) -> str:
    groups: dict[str, list[Page]] = {}
    for page in pages:
        groups.setdefault(page.section_title, []).append(page)
    chunks: list[str] = []
    for section_title, section_pages in groups.items():
        items = []
        for page in section_pages:
            classes = ' class="is-current"' if page.output_rel == current.output_rel else ""
            items.append(
                f'<li><a{classes} href="{html.escape(rel_link(current.output_rel, page.output_rel))}">{html.escape(page.title)}</a></li>'
            )
        chunks.append(
            "<div class=\"nav-group\">"
            f"<div class=\"nav-group-title\">{html.escape(section_title)}</div>"
            f"<ul>{''.join(items)}</ul>"
            "</div>"
        )
    return "".join(chunks)


def page_chrome(title: str, body: str, css_href: str, lang_attr: str) -> str:
    return (
        "<!doctype html>"
        f"<html lang=\"{html.escape(lang_attr)}\">"
        "<head>"
        "<meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{html.escape(title)}</title>"
        f"<link rel=\"stylesheet\" href=\"{html.escape(css_href)}\">"
        "</head>"
        "<body>"
        "<div class=\"site-shell\">"
        f"{body}"
        "</div>"
        "</body>"
        "</html>"
    )


def render_page(output_dir: Path, pages: list[Page], page: Page, previous_page: Page | None, next_page: Page | None) -> None:
    css_href = rel_link(page.output_rel, Path("assets") / "book.css")
    home_href = rel_link(page.output_rel, Path("index.html"))
    lang_home_href = rel_link(page.output_rel, Path(page.language) / "index.html")
    repo_href = f"{REPO_URL}/blob/main/{page.source_path.relative_to(ROOT).as_posix()}"
    toc_panel = (
        "<section class=\"toc-panel\">"
        "<h2>On This Page</h2>"
        f"{page.toc_html}"
        "</section>"
        if page.toc_html
        else ""
    )
    prev_html = (
        f'<a href="{html.escape(rel_link(page.output_rel, previous_page.output_rel))}"><span class="meta-label">Previous</span><br>{html.escape(previous_page.title)}</a>'
        if previous_page
        else "<span></span>"
    )
    next_html = (
        f'<a href="{html.escape(rel_link(page.output_rel, next_page.output_rel))}" style="text-align:right;"><span class="meta-label">Next</span><br>{html.escape(next_page.title)}</a>'
        if next_page
        else "<span></span>"
    )
    body = (
        "<header class=\"site-header\">"
        "<div class=\"site-header-inner\">"
        "<div class=\"brand\">"
        f"<a class=\"brand-title\" href=\"{html.escape(home_href)}\">{html.escape(SITE_TITLE)}</a>"
        f"<div class=\"brand-subtitle\">{html.escape(page.language_label)} / {html.escape(page.section_title)}</div>"
        "</div>"
        "<nav class=\"header-links\">"
        f"<a href=\"{html.escape(home_href)}\">Home</a>"
        f"<a href=\"{html.escape(lang_home_href)}\">Language Home</a>"
        f"<a href=\"{html.escape(repo_href)}\">Source</a>"
        "</nav>"
        "</div>"
        "</header>"
        "<main class=\"site-main\">"
        "<div class=\"content-shell\">"
        f"<aside class=\"sidebar-panel\"><h2>Book Map</h2>{render_nav(pages, page)}</aside>"
        "<div class=\"content-column\">"
        "<article class=\"content-panel\">"
        f"<div class=\"content-meta\"><span class=\"meta-label\">{html.escape(page.section_title)}</span></div>"
        f"{page.body_html}"
        f"<nav class=\"pager\">{prev_html}{next_html}</nav>"
        "</article>"
        f"{toc_panel}"
        "</div>"
        "</div>"
        "</main>"
        "<footer class=\"site-footer\">"
        "<div class=\"site-footer-inner\">"
        "Published from the canonical manuscript sources in this repository."
        "</div>"
        "</footer>"
    )
    target = output_dir / page.output_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page_chrome(page.title, body, css_href, BOOK_SPECS[page.language]["lang_attr"]), encoding="utf-8")


def render_language_index(output_dir: Path, language: str, spec: dict, pages: list[Page]) -> None:
    index_rel = Path(language) / "index.html"
    css_href = rel_link(index_rel, Path("assets") / "book.css")
    home_href = rel_link(index_rel, Path("index.html"))
    sections: dict[str, list[Page]] = {}
    for page in pages:
        sections.setdefault(page.section_title, []).append(page)
    cards = []
    for section_title, section_pages in sections.items():
        items = "".join(
            f'<li><a href="{html.escape(rel_link(index_rel, page.output_rel))}">{html.escape(page.title)}</a></li>'
            for page in section_pages
        )
        cards.append(
            "<section class=\"section-card\">"
            f"<h2>{html.escape(section_title)}</h2>"
            f"<ul>{items}</ul>"
            "</section>"
        )
    body = (
        "<header class=\"site-header\">"
        "<div class=\"site-header-inner\">"
        "<div class=\"brand\">"
        f"<a class=\"brand-title\" href=\"{html.escape(home_href)}\">{html.escape(SITE_TITLE)}</a>"
        f"<div class=\"brand-subtitle\">{html.escape(spec['label'])}</div>"
        "</div>"
        "<nav class=\"header-links\">"
        f"<a href=\"{html.escape(home_href)}\">Home</a>"
        f"<a href=\"{html.escape(REPO_URL)}\">Repository</a>"
        "</nav>"
        "</div>"
        "</header>"
        "<main class=\"site-main\">"
        "<div class=\"language-home\">"
        "<section class=\"hero-card\">"
        f"<div class=\"hero-kicker\">{html.escape(spec['label'])}</div>"
        f"<h1>{html.escape(spec['label'])}</h1>"
        f"<p>{html.escape(spec['index_intro'])}</p>"
        f"<p><a class=\"button secondary\" href=\"{html.escape(REPO_URL)}\">Open Repository</a></p>"
        "</section>"
        f"<div class=\"section-list\">{''.join(cards)}</div>"
        "</div>"
        "</main>"
        "<footer class=\"site-footer\"><div class=\"site-footer-inner\">Generated from the manuscript sources on GitHub.</div></footer>"
    )
    target = output_dir / index_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page_chrome(spec["label"], body, css_href, spec["lang_attr"]), encoding="utf-8")


def render_root_index(output_dir: Path, books: dict[str, list[Page]]) -> None:
    index_rel = Path("index.html")
    css_href = "assets/book.css"
    cards = []
    for language, pages in books.items():
        spec = BOOK_SPECS[language]
        source_dir = "manuscript/" if language == "ja" else "manuscript-en/"
        cards.append(
            "<section class=\"language-card\">"
            f"<div class=\"hero-kicker\">{html.escape(spec['label'])}</div>"
            f"<h2>{html.escape(spec['label'])}</h2>"
            f"<p>{html.escape(spec['index_intro'])}</p>"
            f"<p>{len(pages)} pages generated from {code_literal(source_dir)}.</p>"
            "<div class=\"button-row\">"
            f"<a class=\"button primary\" href=\"{language}/index.html\">Read</a>"
            f"<a class=\"button secondary\" href=\"{REPO_URL}/tree/main/{'manuscript' if language == 'ja' else 'manuscript-en'}\">Source Tree</a>"
            "</div>"
            "</section>"
        )
    body = (
        "<header class=\"site-header\">"
        "<div class=\"site-header-inner\">"
        "<div class=\"brand\">"
        f"<div class=\"brand-title\">{html.escape(SITE_TITLE)}</div>"
        "<div class=\"brand-subtitle\">GitHub Pages edition</div>"
        "</div>"
        "<nav class=\"header-links\">"
        f"<a href=\"{html.escape(REPO_URL)}\">Repository</a>"
        f"<a href=\"{html.escape(REPO_URL)}/blob/main/docs/pages-publishing.md\">Publishing Guide</a>"
        "</nav>"
        "</div>"
        "</header>"
        "<main class=\"site-main\">"
        "<section class=\"hero\">"
        "<div class=\"hero-card\">"
        "<div class=\"hero-kicker\">Book Site</div>"
        f"<h1>{html.escape(SITE_TITLE)}</h1>"
        "<p>この site は "
        f"{code_literal('manuscript/')} と {code_literal('manuscript-en/')}"
        " の canonical source から生成した reader-facing edition です。"
        "日本語版と英語版を切り替えながら、front matter、各 Part、appendices、backmatter を順に読めます。</p>"
        "<ul class=\"pill-list\">"
        "<li>Prompt Engineering</li>"
        "<li>Context Engineering</li>"
        "<li>Harness Engineering</li>"
        "<li>Japanese / English</li>"
        "</ul>"
        "</div>"
        f"<div class=\"language-grid\">{''.join(cards)}</div>"
        "</section>"
        "</main>"
        "<footer class=\"site-footer\"><div class=\"site-footer-inner\">Built from the canonical manuscript sources in the GitHub repository.</div></footer>"
    )
    (output_dir / index_rel).write_text(page_chrome(SITE_TITLE, body, css_href, "en"), encoding="utf-8")


def collect_pages(language: str) -> list[Page]:
    spec = BOOK_SPECS[language]
    pages: list[Page] = []
    for section in spec["sections"]:
        for path in ordered_section_paths(spec["root"], section):
            pages.append(load_page(language, spec["root"], spec["label"], section, path))
    return pages


def copy_assets(output_dir: Path) -> None:
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "site-assets" / "book.css", assets_dir / "book.css")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output).resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    copy_assets(output_dir)

    books: dict[str, list[Page]] = {}
    for language in ("ja", "en"):
        pages = collect_pages(language)
        books[language] = pages
        render_language_index(output_dir, language, BOOK_SPECS[language], pages)
        for index, page in enumerate(pages):
            previous_page = pages[index - 1] if index > 0 else None
            next_page = pages[index + 1] if index < len(pages) - 1 else None
            render_page(output_dir, pages, page, previous_page, next_page)

    render_root_index(output_dir, books)
    print(f"pages site built at {output_dir}")


if __name__ == "__main__":
    main()
