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
FORMATTER_ASSETS = ROOT / "site-assets" / "formatter"


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
    lang_attr: str
    source_root: Path
    source_path: Path
    section_key: str
    section_title: str
    title: str
    excerpt: str
    output_rel: Path
    body_html: str
    toc_html: str
    page_kind: str
    page_label: str
    nav_title: str
    nav_group: str
    logical_id: str


BOOK_SPECS = {
    "ja": {
        "label": "日本語版",
        "lang_attr": "ja",
        "root": ROOT / "manuscript",
        "sidebar_subtitle": "AIエージェントに仕事を完了させるための Prompt / Context / Harness Engineering を扱う。",
        "home_link_label": "はじめに",
        "switch_label": "English",
        "home_summary": "曖昧な要求を仕様へ変換し、repo を読み、変更し、verify して仕事を完了させるための設計を扱う。",
        "home_actions": [
            {"kind": "first_chapter", "label": "CH01 から読む"},
            {"kind": "switch", "label": "英語版"},
        ],
        "section_sequence": [
            SectionSpec("front-matter", "導入", "front-matter"),
            SectionSpec("part-00", "Part 0", "part-00"),
            SectionSpec("part-01", "Part I Prompt Engineering", "part-01-prompt", part=True),
            SectionSpec("part-02", "Part II Context Engineering", "part-02-context", part=True),
            SectionSpec("part-03", "Part III Harness Engineering", "part-03-harness", part=True),
            SectionSpec("appendices", "付録", "appendices"),
            SectionSpec("backmatter", "後付け", "backmatter"),
        ],
        "prev_label": "前へ",
        "next_label": "次へ",
        "home_label": "目次へ",
        "toc_title": "目次",
        "search_placeholder": "Search...",
        "home_kicker": "IT Engineer Knowledge Architecture Series",
    },
    "en": {
        "label": "English Edition",
        "lang_attr": "en",
        "root": ROOT / "manuscript-en",
        "sidebar_subtitle": "Prompt, Context, and Harness Engineering for getting AI agents to complete real work.",
        "home_link_label": "Introduction",
        "switch_label": "日本語",
        "home_summary": "This web edition follows the manuscript from the introduction through the three parts, appendices, and backmatter.",
        "home_actions": [
            {"kind": "first_chapter", "label": "Start with CH01"},
            {"kind": "switch", "label": "日本語版"},
        ],
        "section_sequence": [
            SectionSpec("front-matter", "Introduction", "front-matter"),
            SectionSpec("part-00", "Part 0", "part-00"),
            SectionSpec("part-01", "Part I Prompt Engineering", "part-01-prompt", part=True),
            SectionSpec("part-02", "Part II Context Engineering", "part-02-context", part=True),
            SectionSpec("part-03", "Part III Harness Engineering", "part-03-harness", part=True),
            SectionSpec("appendices", "Appendices", "appendices"),
            SectionSpec("backmatter", "Backmatter", "backmatter"),
        ],
        "prev_label": "Previous",
        "next_label": "Next",
        "home_label": "Contents",
        "toc_title": "Contents",
        "search_placeholder": "Search...",
        "home_kicker": "IT Engineer Knowledge Architecture Series",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a book-style GitHub Pages site from the manuscript.")
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
        return candidate[:220]
    return ""


def strip_leading_h1_html(body_html: str) -> str:
    return re.sub(r"^\s*<h1\b[^>]*>.*?</h1>\s*", "", body_html, count=1, flags=re.S)


def page_token(path: Path) -> str:
    stem = path.stem
    if stem == "part-opener":
        return "part-opener"
    match = re.match(r"^(app-[a-z]+|ch\d+|\d+)", stem)
    if match:
        return match.group(1)
    return stem


def page_prefix(language: str) -> Path:
    return Path() if language == "ja" else Path("en")


def output_rel(language: str, section: SectionSpec, source_path: Path) -> Path:
    prefix = page_prefix(language)
    token = page_token(source_path)

    if section.key == "front-matter":
        if token == "00":
            return prefix / "index.html"
        return prefix / "introduction" / token / "index.html"
    if token == "part-opener":
        return prefix / "parts" / section.key / "index.html"
    if token.startswith("ch"):
        return prefix / "chapters" / token / "index.html"
    if section.key == "appendices":
        return prefix / "appendices" / token / "index.html"
    if section.key == "backmatter":
        return prefix / "backmatter" / token / "index.html"
    return prefix / token / "index.html"


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


def classify_page(language: str, section: SectionSpec, source_path: Path, title: str) -> tuple[str, str]:
    token = page_token(source_path)
    if section.key == "front-matter" and token == "00":
        return "home", BOOK_SPECS[language]["home_link_label"]
    if token == "part-opener":
        return "part-opener", section.title
    chapter_match = re.match(r"^ch(\d+)$", token)
    if chapter_match:
        chapter_no = int(chapter_match.group(1))
        if language == "ja":
            return "chapter", f"第{chapter_no}章"
        return "chapter", f"Chapter {chapter_no}"
    appendix_match = re.match(r"^app-([a-z]+)$", token)
    if appendix_match:
        letter = appendix_match.group(1).upper()
        if language == "ja":
            return "appendix", f"付録{letter}"
        return "appendix", f"Appendix {letter}"
    if section.key == "backmatter":
        return "backmatter", section.title
    return "page", section.title


def nav_title_for(language: str, page_kind: str, page_label: str, title: str) -> str:
    if page_kind in {"chapter", "appendix"}:
        joiner = "：" if language == "ja" else ": "
        return f"{page_label}{joiner}{title}"
    return title


def load_page(language: str, section: SectionSpec, source_path: Path) -> Page:
    spec = BOOK_SPECS[language]
    raw = source_path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw).strip()
    title = extract_title(body, source_path.stem)
    md = markdown.Markdown(extensions=["extra", "toc", "sane_lists"])
    body_html = strip_leading_h1_html(md.convert(body))
    excerpt = extract_excerpt(body)
    page_kind, page_label = classify_page(language, section, source_path, title)
    return Page(
        language=language,
        language_label=spec["label"],
        lang_attr=spec["lang_attr"],
        source_root=spec["root"],
        source_path=source_path,
        section_key=section.key,
        section_title=section.title,
        title=title,
        excerpt=excerpt,
        output_rel=output_rel(language, section, source_path),
        body_html=body_html,
        toc_html=md.toc if md.toc else "",
        page_kind=page_kind,
        page_label=page_label,
        nav_title=nav_title_for(language, page_kind, page_label, title),
        nav_group=section.title,
        logical_id=f"{section.key}:{page_token(source_path)}",
    )


def rel_link(from_rel: Path, to_rel: Path) -> str:
    return os.path.relpath(to_rel, start=from_rel.parent).replace(os.sep, "/")


def page_title(page: Page) -> str:
    if page.page_kind == "home" and page.language == "ja":
        return SITE_TITLE
    return f"{page.title} - {SITE_TITLE}"


def page_description(page: Page) -> str:
    if page.excerpt:
        return page.excerpt
    return BOOK_SPECS[page.language]["home_summary"]


def render_nav(pages: list[Page], current: Page, counterpart: Page | None) -> str:
    spec = BOOK_SPECS[current.language]
    home_page = next(page for page in pages if page.page_kind == "home")
    grouped: dict[str, list[Page]] = {}
    for page in pages:
        if page.page_kind == "home":
            continue
        grouped.setdefault(page.nav_group, []).append(page)

    sections = [
        "<div class=\"toc-section\">"
        "<ul class=\"toc-list\">"
        f"<li class=\"toc-item\"><a href=\"{html.escape(rel_link(current.output_rel, home_page.output_rel))}\" class=\"toc-link {'active' if current.output_rel == home_page.output_rel else ''}\">{html.escape(spec['home_link_label'])}</a></li>"
        "</ul>"
        "</div>"
    ]
    for group_title, group_pages in grouped.items():
        items = []
        for page in group_pages:
            active = " active" if page.output_rel == current.output_rel else ""
            items.append(
                f"<li class=\"toc-item{' toc-chapter' if page.page_kind == 'chapter' else ''}\">"
                f"<a href=\"{html.escape(rel_link(current.output_rel, page.output_rel))}\" class=\"toc-link{active}\">{html.escape(page.nav_title)}</a>"
                "</li>"
            )
        sections.append(
            "<div class=\"toc-section\">"
            f"<h4 class=\"toc-section-title\">{html.escape(group_title)}</h4>"
            f"<ul class=\"toc-list\">{''.join(items)}</ul>"
            "</div>"
        )

    switch_href = rel_link(current.output_rel, counterpart.output_rel if counterpart else (Path("index.html") if current.language == "en" else Path("en") / "index.html"))
    return (
        "<div class=\"sidebar-content\">"
        "<div class=\"book-info\">"
        f"<h2 class=\"book-title\">{html.escape(SITE_TITLE)}</h2>"
        f"<p class=\"book-subtitle\">{html.escape(spec['sidebar_subtitle'])}</p>"
        "</div>"
        "<div class=\"toc\">"
        f"<h3 class=\"toc-title\">{html.escape(spec['toc_title'])}</h3>"
        f"{''.join(sections)}"
        "</div>"
        "<div class=\"sidebar-footer\">"
        "<div class=\"external-links\">"
        f"<a href=\"{html.escape(switch_href)}\" class=\"external-link\">{html.escape(spec['switch_label'])}</a>"
        f"<a href=\"{html.escape(REPO_URL)}\" target=\"_blank\" rel=\"noopener\" class=\"external-link\">GitHub</a>"
        "</div>"
        "</div>"
        "</div>"
    )


def render_lead(page: Page, counterpart: Page | None, first_chapter: Page) -> str:
    spec = BOOK_SPECS[page.language]
    switch_target = counterpart.output_rel if counterpart else (Path("index.html") if page.language == "en" else Path("en") / "index.html")
    switch_href = rel_link(page.output_rel, switch_target)
    first_chapter_href = rel_link(page.output_rel, first_chapter.output_rel)

    if page.page_kind == "home":
        actions = []
        for action in spec["home_actions"]:
            if action["kind"] == "first_chapter":
                actions.append(f"<a href=\"{html.escape(first_chapter_href)}\" class=\"button primary\">{html.escape(action['label'])}</a>")
            elif action["kind"] == "switch":
                actions.append(f"<a href=\"{html.escape(switch_href)}\" class=\"button secondary\">{html.escape(action['label'])}</a>")
        return (
            "<section class=\"book-home-lead\">"
            f"<p class=\"page-kicker\">{html.escape(spec['home_kicker'])}</p>"
            f"<h1>{html.escape(SITE_TITLE)}</h1>"
            f"<p class=\"page-deck\">{html.escape(spec['home_summary'])}</p>"
            f"<div class=\"lead-actions\">{''.join(actions)}</div>"
            "</section>"
        )

    deck = html.escape(page.excerpt) if page.excerpt else ""
    return "".join(
        [
            "<section class=\"page-lead\">",
            f"<p class=\"page-kicker\">{html.escape(page.section_title)}</p>",
            f"<p class=\"page-section-label\">{html.escape(page.page_label)}</p>",
            f"<h1>{html.escape(page.title)}</h1>",
            f"<p class=\"page-deck\">{deck}</p>" if deck else "",
            "</section>",
        ]
    )


def render_pager(page: Page, previous_page: Page | None, next_page: Page | None) -> str:
    if page.page_kind == "home":
        return ""
    spec = BOOK_SPECS[page.language]
    home_target = Path("index.html") if page.language == "ja" else Path("en") / "index.html"
    prev_html = (
        f"<a href=\"{html.escape(rel_link(page.output_rel, previous_page.output_rel))}\" class=\"nav-prev\" rel=\"prev\">"
        f"<span class=\"label\">{html.escape(spec['prev_label'])}</span>"
        f"<span class=\"title\">{html.escape(previous_page.nav_title)}</span>"
        "</a>"
        if previous_page
        else f"<span class=\"nav-disabled nav-prev\"><span class=\"label\">{html.escape(spec['prev_label'])}</span></span>"
    )
    next_html = (
        f"<a href=\"{html.escape(rel_link(page.output_rel, next_page.output_rel))}\" class=\"nav-next\" rel=\"next\">"
        f"<span class=\"label\">{html.escape(spec['next_label'])}</span>"
        f"<span class=\"title\">{html.escape(next_page.nav_title)}</span>"
        "</a>"
        if next_page
        else f"<span class=\"nav-disabled nav-next\"><span class=\"label\">{html.escape(spec['next_label'])}</span></span>"
    )
    home_html = f"<a href=\"{html.escape(rel_link(page.output_rel, home_target))}\" class=\"nav-home\"><span class=\"label\">{html.escape(spec['home_label'])}</span></a>"
    return (
        "<nav class=\"book-navigation\" aria-label=\"Page navigation\">"
        "<div class=\"chapter-nav\">"
        f"{prev_html}{home_html}{next_html}"
        "</div>"
        "</nav>"
    )


def page_chrome(page: Page, body: str, current_search_placeholder: str) -> str:
    css_main = rel_link(page.output_rel, Path("assets") / "css" / "main.css")
    css_syntax = rel_link(page.output_rel, Path("assets") / "css" / "syntax-highlighting.css")
    css_custom = rel_link(page.output_rel, Path("assets") / "css" / "book-custom.css")
    js_copy = rel_link(page.output_rel, Path("assets") / "js" / "code-copy-lightweight.js")
    js_theme = rel_link(page.output_rel, Path("assets") / "js" / "theme.js")
    js_search = rel_link(page.output_rel, Path("assets") / "js" / "search.js")

    return (
        "<!DOCTYPE html>"
        f"<html lang=\"{html.escape(page.lang_attr)}\" data-theme=\"light\">"
        "<head>"
        "<meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<meta name=\"description\" content=\"{html.escape(page_description(page))}\">"
        f"<title>{html.escape(page_title(page))}</title>"
        f"<link rel=\"stylesheet\" href=\"{html.escape(css_main)}\">"
        f"<link rel=\"stylesheet\" href=\"{html.escape(css_syntax)}\">"
        f"<link rel=\"stylesheet\" href=\"{html.escape(css_custom)}\">"
        "<script>"
        "(function(){try{const k='book-theme';const t=localStorage.getItem(k)||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t);}catch(_){}})();"
        "</script>"
        "</head>"
        "<body>"
        "<input type=\"checkbox\" id=\"sidebar-toggle-checkbox\" class=\"sidebar-toggle-checkbox\" aria-hidden=\"true\" tabindex=\"-1\">"
        "<div class=\"book-layout\">"
        "<header class=\"book-header\">"
        "<div class=\"header-left\">"
        "<label for=\"sidebar-toggle-checkbox\" class=\"sidebar-toggle\" aria-label=\"Toggle sidebar\" role=\"button\" tabindex=\"0\">"
        "<svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\">"
        "<line x1=\"3\" y1=\"6\" x2=\"21\" y2=\"6\"></line>"
        "<line x1=\"3\" y1=\"12\" x2=\"21\" y2=\"12\"></line>"
        "<line x1=\"3\" y1=\"18\" x2=\"21\" y2=\"18\"></line>"
        "</svg>"
        "</label>"
        f"<a href=\"{html.escape(rel_link(page.output_rel, Path('index.html') if page.language == 'ja' else Path('en') / 'index.html'))}\" class=\"header-title\"><h1>{html.escape(SITE_TITLE)}</h1></a>"
        "</div>"
        "<div class=\"header-center\">"
        "<div class=\"search-container\">"
        f"<input type=\"search\" placeholder=\"{html.escape(current_search_placeholder)}\" class=\"search-input\" id=\"search-input\" autocomplete=\"off\">"
        "<div class=\"search-results\" id=\"search-results\"></div>"
        "</div>"
        "</div>"
        "<div class=\"header-right\">"
        "<button class=\"theme-toggle\" aria-label=\"Toggle theme\">"
        "<svg class=\"theme-icon theme-icon-light\" width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\">"
        "<circle cx=\"12\" cy=\"12\" r=\"5\"></circle>"
        "<line x1=\"12\" y1=\"1\" x2=\"12\" y2=\"3\"></line>"
        "<line x1=\"12\" y1=\"21\" x2=\"12\" y2=\"23\"></line>"
        "<line x1=\"4.22\" y1=\"4.22\" x2=\"5.64\" y2=\"5.64\"></line>"
        "<line x1=\"18.36\" y1=\"18.36\" x2=\"19.78\" y2=\"19.78\"></line>"
        "<line x1=\"1\" y1=\"12\" x2=\"3\" y2=\"12\"></line>"
        "<line x1=\"21\" y1=\"12\" x2=\"23\" y2=\"12\"></line>"
        "<line x1=\"4.22\" y1=\"19.78\" x2=\"5.64\" y2=\"18.36\"></line>"
        "<line x1=\"18.36\" y1=\"5.64\" x2=\"19.78\" y2=\"4.22\"></line>"
        "</svg>"
        "<svg class=\"theme-icon theme-icon-dark\" width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\">"
        "<path d=\"M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z\"></path>"
        "</svg>"
        "</button>"
        f"<a href=\"{html.escape(REPO_URL)}\" class=\"github-link\" target=\"_blank\" rel=\"noopener\" aria-label=\"View on GitHub\">"
        "<svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"currentColor\">"
        "<path d=\"M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z\"></path>"
        "</svg>"
        "</a>"
        "</div>"
        "</header>"
        f"{body}"
        "</div>"
        "<label for=\"sidebar-toggle-checkbox\" class=\"book-sidebar-overlay\" id=\"sidebar-overlay\" aria-label=\"Close sidebar\"></label>"
        f"<script async src=\"{html.escape(js_copy)}\"></script>"
        f"<script defer src=\"{html.escape(js_theme)}\"></script>"
        f"<script defer src=\"{html.escape(js_search)}\"></script>"
        "<script>"
        "document.addEventListener('DOMContentLoaded',function(){"
        "var cb=document.getElementById('sidebar-toggle-checkbox');"
        "if(!cb)return;"
        "cb.checked=false;"
        "document.addEventListener('click',function(e){"
        "if(!cb.checked)return;"
        "if(e.target.closest('.book-sidebar')||e.target.closest('.sidebar-toggle'))return;"
        "cb.checked=false;"
        "});"
        "});"
        "</script>"
        "</body>"
        "</html>"
    )


def render_page(
    output_dir: Path,
    pages: list[Page],
    page: Page,
    previous_page: Page | None,
    next_page: Page | None,
    counterpart: Page | None,
) -> None:
    spec = BOOK_SPECS[page.language]
    first_chapter = next(candidate for candidate in pages if candidate.page_kind == "chapter")
    sidebar_html = render_nav(pages, page, counterpart)
    toc_panel = (
        "<aside class=\"book-toc-panel\">"
        f"<h3>{html.escape(spec['toc_title'])}</h3>"
        f"{page.toc_html}"
        "</aside>"
        if page.toc_html
        else ""
    )
    footer = (
        "<footer class=\"book-footer\" role=\"contentinfo\">"
        "<div class=\"book-footer-inner\">"
        "<div class=\"book-footer-license\">"
        "GitHub Pages public edition of the manuscript repository."
        "</div>"
        "<div class=\"book-footer-links\">"
        f"<a href=\"{html.escape(REPO_URL)}\" target=\"_blank\" rel=\"noopener\">GitHub</a>"
        f"<a href=\"{html.escape(REPO_URL)}/blob/main/{html.escape(page.source_path.relative_to(ROOT).as_posix())}\" target=\"_blank\" rel=\"noopener\">Source Markdown</a>"
        "</div>"
        "</div>"
        "</footer>"
    )
    body = (
        f"<aside class=\"book-sidebar\" id=\"sidebar\"><nav class=\"sidebar-nav\" role=\"navigation\" aria-label=\"Main navigation\">{sidebar_html}</nav></aside>"
        "<main class=\"book-main\" id=\"main\">"
        "<div class=\"book-content\">"
        "<article class=\"page-content\">"
        f"{render_lead(page, counterpart, first_chapter)}"
        f"{page.body_html}"
        "</article>"
        f"{toc_panel}"
        f"{render_pager(page, previous_page, next_page)}"
        f"{footer}"
        "</div>"
        "</main>"
    )
    target = output_dir / page.output_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page_chrome(page, body, spec["search_placeholder"]), encoding="utf-8")


def collect_pages(language: str) -> list[Page]:
    spec = BOOK_SPECS[language]
    pages: list[Page] = []
    for section in spec["section_sequence"]:
        for source_path in ordered_section_paths(spec["root"], section):
            pages.append(load_page(language, section, source_path))
    return pages


def copy_assets(output_dir: Path) -> None:
    css_dir = output_dir / "assets" / "css"
    js_dir = output_dir / "assets" / "js"
    css_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FORMATTER_ASSETS / "css" / "main.css", css_dir / "main.css")
    shutil.copy2(FORMATTER_ASSETS / "css" / "mobile-responsive.css", css_dir / "mobile-responsive.css")
    shutil.copy2(FORMATTER_ASSETS / "css" / "syntax-highlighting.css", css_dir / "syntax-highlighting.css")
    shutil.copy2(ROOT / "site-assets" / "book-custom.css", css_dir / "book-custom.css")
    shutil.copy2(FORMATTER_ASSETS / "js" / "theme.js", js_dir / "theme.js")
    shutil.copy2(FORMATTER_ASSETS / "js" / "search.js", js_dir / "search.js")
    shutil.copy2(FORMATTER_ASSETS / "js" / "code-copy-lightweight.js", js_dir / "code-copy-lightweight.js")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")


def build_counterpart_map(books: dict[str, list[Page]]) -> dict[tuple[str, str], Page]:
    lookup: dict[tuple[str, str], Page] = {}
    for language, pages in books.items():
        for page in pages:
            lookup[(language, page.logical_id)] = page
    return lookup


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output).resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    copy_assets(output_dir)

    books = {language: collect_pages(language) for language in ("ja", "en")}
    lookup = build_counterpart_map(books)

    for language, pages in books.items():
        for index, page in enumerate(pages):
            other_language = "en" if language == "ja" else "ja"
            counterpart = lookup.get((other_language, page.logical_id))
            previous_page = pages[index - 1] if index > 0 else None
            next_page = pages[index + 1] if index < len(pages) - 1 else None
            render_page(output_dir, pages, page, previous_page, next_page, counterpart)

    print(f"pages site built at {output_dir}")


if __name__ == "__main__":
    main()
