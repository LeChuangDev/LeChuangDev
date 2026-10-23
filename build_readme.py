"""把编码时长与最新文章写入 README 的占位区块。

设计原则：任何一个数据源不可用时，只跳过对应区块，绝不把错误内容写进 README。
"""

from __future__ import annotations

import html
import os
import pathlib
import re
import sys
import time

import feedparser
import httpx

ROOT = pathlib.Path(__file__).parent.resolve()
README = ROOT / "README.md"

# 通过环境变量注入，避免把私人地址写死在代码里
BLOG_FEED_URL = os.getenv("BLOG_FEED_URL", "").strip()
WAKATIME_RAW_URL = os.getenv("WAKATIME_RAW_URL", "").strip()

TIMEOUT = 20.0
UA = "Mozilla/5.0 (compatible; readme-bot/1.0)"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def replace_chunk(content: str, marker: str, chunk: str) -> str:
    """替换 <!-- marker starts --> ... <!-- marker ends --> 之间的内容。"""
    pattern = re.compile(
        r"(<!--\s*{}\s*starts\s*-->).*?(<!--\s*{}\s*ends\s*-->)".format(
            re.escape(marker), re.escape(marker)
        ),
        re.DOTALL,
    )
    if not pattern.search(content):
        print(f"[warn] 未找到标记 {marker}，跳过替换", file=sys.stderr)
        return content

    # 用函数作为替换值，避免 chunk 里的 \1、\g<name> 被当成反向引用
    return pattern.sub(
        lambda m: f"{m.group(1)}\n{chunk}\n{m.group(2)}", content, count=1
    )


def fetch_code_time() -> str | None:
    """拉取 WakaTime 纯文本统计，返回 markdown 代码块。"""
    if not WAKATIME_RAW_URL:
        print("[info] 未配置 WAKATIME_RAW_URL，跳过 code_time")
        return None

    try:
        resp = httpx.get(
            WAKATIME_RAW_URL, timeout=TIMEOUT, follow_redirects=True, headers={"User-Agent": UA}
        )
        resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001 - 任何网络异常都只降级
        print(f"[warn] 获取编码时长失败：{exc}", file=sys.stderr)
        return None

    text = ANSI_RE.sub("", resp.text).strip()
    # 防止 Gist 挂了返回一段 HTML 错误页
    if not text or text.startswith("<"):
        print("[warn] 编码时长内容不可用，跳过", file=sys.stderr)
        return None

    return "```text\n" + text + "\n```"


def fetch_blog_entries(limit: int = 5) -> str | None:
    """拉取博客 feed，返回 markdown 列表。"""
    if not BLOG_FEED_URL:
        print("[info] 未配置 BLOG_FEED_URL，跳过 blog")
        return None

    try:
        resp = httpx.get(
            BLOG_FEED_URL, timeout=TIMEOUT, follow_redirects=True, headers={"User-Agent": UA}
        )
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] 获取博客 feed 失败：{exc}", file=sys.stderr)
        return None

    if not feed.entries:
        print("[warn] feed 中没有条目，跳过", file=sys.stderr)
        return None

    lines: list[str] = []
    for entry in feed.entries[:limit]:
        title = (entry.get("title") or "").strip()
        url = (entry.get("link") or "").split("#")[0].strip()
        if not title or not url:
            continue

        published = ""
        stamp = entry.get("published_parsed") or entry.get("updated_parsed")
        if stamp:
            published = time.strftime("%Y-%m-%d", stamp)

        suffix = f" - {published}" if published else ""
        lines.append(
            '* <a href="{url}" target="_blank">{title}</a>{suffix}'.format(
                url=html.escape(url, quote=True),
                title=html.escape(title),
                suffix=suffix,
            )
        )

    return "\n".join(lines) if lines else None


def main() -> int:
    original = README.read_text(encoding="utf-8")
    updated = original

    code_time = fetch_code_time()
    if code_time:
        updated = replace_chunk(updated, "code_time", code_time)

    blog = fetch_blog_entries()
    if blog:
        updated = replace_chunk(updated, "blog", blog)

    if updated == original:
        print("[info] README 无变化")
        return 0

    README.write_text(updated, encoding="utf-8")
    print("[info] README 已更新")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())