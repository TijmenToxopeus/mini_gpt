# import re

# def extract_dialogue_by_indent(input_path="lotr_raw.txt", output_path="lotr_indent_dialogue.txt"):
#     """
#     Extracts dialogue from a screenplay-like text using indentation.
#     Keeps lines with indentation levels typical for character names and dialogue,
#     and removes stage directions (low indentation).
#     """

#     with open(input_path, "r", encoding="utf-8") as f:
#         lines = f.readlines()

#     dialogue_lines = []
#     current_speaker = None
#     buffer = []

#     for line in lines:
#         # Count leading spaces
#         indent = len(line) - len(line.lstrip(" "))
#         text = line.strip()

#         # Skip empty lines
#         if not text:
#             continue

#         # Detect character name (mostly uppercase, centered, around 20+ spaces)
#         if indent >= 18 and re.fullmatch(r"[A-Z][A-Z\s'\-\.0-9\(\)]+", text):
#             # Flush previous dialogue
#             if current_speaker and buffer:
#                 dialogue_lines.append(f"{current_speaker}: {' '.join(buffer)}")
#                 buffer = []

#             current_speaker = re.sub(r"\(.*?\)", "", text).strip()
#             continue

#         # Detect dialogue line (indented but not fully left-aligned)
#         if 8 <= indent < 18 and current_speaker:
#             buffer.append(text)
#             continue

#         # Detect parentheticals, slightly deeper indent than dialogue
#         if 14 <= indent < 24 and text.startswith("(") and current_speaker:
#             # Optional: keep tone indicators if you want
#             continue

#         # Low indentation (stage direction / narration) resets speaker
#         if indent < 8:
#             if current_speaker and buffer:
#                 dialogue_lines.append(f"{current_speaker}: {' '.join(buffer)}")
#                 buffer = []
#             current_speaker = None

#     # Flush last speaker
#     if current_speaker and buffer:
#         dialogue_lines.append(f"{current_speaker}: {' '.join(buffer)}")

#     # Clean spacing
#     output_text = re.sub(r"\s{2,}", " ", "\n".join(dialogue_lines)).strip()

#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(output_text)

#     print(f"✅ Extracted dialogue saved to {output_path}")


# if __name__ == "__main__":
#     extract_dialogue_by_indent()


import re

def extract_dialogue_by_indent(input_path="lotr_raw.txt", output_path="lotr_indent_dialogue.txt"):
    """
    Extracts dialogue from a screenplay-like text using indentation.
    Keeps lines with indentation levels typical for character names and dialogue,
    removes stage directions, and cleans tone notes in parentheses.
    """

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    dialogue_lines = []
    current_speaker = None
    buffer = []

    for line in lines:
        indent = len(line) - len(line.lstrip(" "))
        text = line.strip()

        if not text:
            continue

        # Character names (usually centered)
        if indent >= 18 and re.fullmatch(r"[A-Z][A-Z\s'\-\.0-9\(\)]+", text):
            if current_speaker and buffer:
                dialogue_lines.append(f"{current_speaker}: {' '.join(buffer)}")
                buffer = []
            current_speaker = re.sub(r"\(.*?\)", "", text).strip()
            continue

        # Dialogue lines (indented moderately)
        if 8 <= indent < 18 and current_speaker:
            buffer.append(text)
            continue

        # Low indentation = narration, flush
        if indent < 8:
            if current_speaker and buffer:
                dialogue_lines.append(f"{current_speaker}: {' '.join(buffer)}")
                buffer = []
            current_speaker = None

    # Flush last one
    if current_speaker and buffer:
        dialogue_lines.append(f"{current_speaker}: {' '.join(buffer)}")

    # --- 🧹 Final cleaning ---
    output_text = "\n".join(dialogue_lines)
    output_text = re.sub(r"\s{2,}", " ", output_text)
    # Remove any parenthetical text, e.g. (whisper), (V.O.), (calling)
    output_text = re.sub(r"\s*\(.*?\)\s*", " ", output_text)
    output_text = re.sub(r"\s{2,}", " ", output_text).strip()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"✅ Extracted and cleaned dialogue saved to {output_path}")


if __name__ == "__main__":
    extract_dialogue_by_indent()
