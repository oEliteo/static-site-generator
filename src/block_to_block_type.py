from textnode import BlockType


def block_to_block_type(markdown):
    if markdown.startswith("#"):
        hash_count = 0
        for c in markdown:
            if c == "#":
                hash_count += 1
            elif c == " ":
                break
            if hash_count > 6:
                break

        if (
            1 <= hash_count <= 6
            and len(markdown) > hash_count
            and markdown[hash_count] == " "
        ):
            return BlockType.HEADING

    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE

    if markdown.startswith(">"):
        flag = True
        lines = markdown.split("\n")
        for line in lines:
            if line.startswith(">") or line.startswith("> "):
                flag = True
            else:
                flag = False
                break

        if flag == True:
            return BlockType.QUOTE

    if markdown.startswith("-"):
        flag = True
        lines = markdown.split("\n")
        for line in lines:
            if line.startswith("- "):
                flag = True
            else:
                flag = False
                break

        if flag == True:
            return BlockType.UNORDERED

    if markdown.startswith("1."):
        flag = True
        lines = markdown.split("\n")
        for i in range(len(lines)):
            if lines[i].startswith(f"{i + 1}. "):
                flag = True
            else:
                flag = False
                break

        if flag:
            return BlockType.ORDERED

    return BlockType.PARAGRAPH
