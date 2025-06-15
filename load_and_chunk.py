import json
from langchain.schema import Document

def laod_and_chunk(filepath="./utils/data.json"):
  with open(filepath, "r") as f:
    raw_data = json.load(f)
  

  chunks = []

  for entry in raw_data:
    if "components" in entry:
      for comp in entry["components"]:
        name = comp.get("name") or comp.get("test_name")
        range_ = comp.get("normal_range")
        unit = comp.get("units")
        desc = comp.get("description", entry.get("description", ""))
        source = entry.get("source", "")

        text = f"{name}: {desc}. Normal ranges: {range_} {unit}"
        chunks.append(
          Document(page_content=text, metadata={"name": name, "source": source})
        )
    else:
      name = entry.get("test_name") or entry.get("name")
      range_ = entry.get("normal_range")
      unit = entry.get("units")
      desc = entry.get("description", "")
      source = entry.get("source", "")

      text = f"{name}: {desc}. Normal range: {range_} {unit}."
      chunks.append(
          Document(page_content=text, metadata={"name": name, "source": source})
      )

  return chunks
