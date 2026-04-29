from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("Knowledge Base Server")

NOTES_DIR = (
    Path(__file__).parent / "notes"
)  # this makes the notes dir relative to the current executed file regardless from where it was executed


def _build_note_title(title: str) -> Path:
    slug = "-".join(title.lower().split(" "))
    return NOTES_DIR / f"{slug}.md"


@mcp.tool
def create_note(title: str, content: str, tags: list = []):
    with open(_build_note_title(title=title), mode="w") as f:
        f.write(content)


if __name__ == "__main__":
    mcp.run()
