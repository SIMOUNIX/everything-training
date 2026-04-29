from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("Knowledge Base Server")

NOTES_DIR = (
    Path(__file__).parent / "notes"
)  # this makes the notes dir relative to the current executed file regardless from where it was executed


def _parse_note(path: Path) -> dict:
    raw = path.read_text()
    parts = raw.split("---", 2)  # gives ["", frontmatter, content]
    meta = {}
    for line in parts[1].strip().splitlines():
        key, value = line.split(":", 1)  # frontmatter is defined as title: [title]\n...
        meta[key.strip()] = value.strip()
    meta["content"] = parts[2].strip()
    return meta


@mcp.tool
def create_note(title: str, content: str, tags: list[str]):
    slug = "-".join(title.lower().split(" "))
    path = NOTES_DIR / f"{slug}.md"
    tags_str = ", ".join(tags)

    frontmatter = (
        f"---\ntitle: {title}\ntags: {tags_str}\ncreated_at: {datetime.now()}\n---\n\n"
    )
    final_content = f"{frontmatter}{content}"
    _ = path.write_text(data=final_content)


@mcp.tool
def get_note(slug: str) -> dict:
    path = NOTES_DIR / f"{slug}.md"
    return _parse_note(path=path)


if __name__ == "__main__":
    mcp.run()
