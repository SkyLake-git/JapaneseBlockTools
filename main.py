import json
import random
import hashlib
import shutil

import font
import PIL.Image
import PIL.ImageDraw
import os
from tqdm import tqdm
import base64


def generate_images(output_path: str, chars: list[str], ending_chars: list[str], starting_chars: list[str], emoji_chars: list[str]):
	writer = font.FontWriter("C:\\Windows\\Fonts\\meiryob.ttc", 100)
	emoji_writer = font.FontWriter("C:\\Windows\\Fonts\\SEGUIEMJ.TTF", 100)
	size = (128, 128)

	for char in tqdm(chars):
		print(char, get_char_identity(char))
		image = base_image_create(size, char in ending_chars, char in starting_chars)

		current_writer = writer
		if char in emoji_chars:
			print("emoji")
			current_writer = emoji_writer

		current_writer.draw(image, int(size[0] / 2), int(size[1] / 2), char)

		image.save(os.path.join(output_path, get_char_identity(char) + ".png"))


def regenerate_resource_pack(path: str, chars: list[str]):
	with open(os.path.join(path, "manifest.json"), "r", encoding="utf-8") as f:
		manifest_data = json.load(f)

		manifest_data["header"]["version"][2] += 1

	with open(os.path.join(path, "manifest.json"), "w", encoding="utf-8") as f:
		json.dump(manifest_data, f, indent=4, ensure_ascii=False)

	terrain_texture_data = generate_terrain_textures(chars)

	with open(os.path.join(path, "textures", "terrain_texture.json"), 'w', encoding="utf-8") as f:
		json.dump(terrain_texture_data, f, ensure_ascii=False)

	translation_data = generate_translations(chars)

	for lang in ["ja_JP", "en_US"]:
		with open(os.path.join(path, "texts", f"{lang}.lang"), 'w', encoding="utf-8") as f:
			f.write(translation_data)


def get_char_identity(char: str) -> str:
	return hashlib.md5(char.encode()).hexdigest()


def generate_terrain_textures(chars: list[str]) -> dict:
	number = 0

	data = {
		"num_mip_levels": 4,
		"padding": 8,
		"resource_pack_name": "japanese_block",
		"texture_data": {}
	}

	for char in chars:
		key, registry = create_terrain_registry(char, f"textures/blocks/japanese/{get_char_identity(char)}")

		data["texture_data"][key] = registry

	return data


def generate_translations(chars: list[str]):
	text = ""
	for char in chars:
		text += create_translation(char) + "\n"

	return text


def generate_entries(chars: list[str]):
	data = []
	for char in chars:
		data.append({
			"char": char,
			"identity": "japanese_" + get_char_identity(char)
		})
	return data


def create_terrain_registry(char: str, path: str):
	return f"japanese_{get_char_identity(char)}", {"textures": path}


def create_translation(char: str):
	return f"tile.japanese_block:japanese_{get_char_identity(char)}.name={char}"


def base_image_create(size: tuple[int, int], ending: bool, starting: bool) -> PIL.Image:
	image = PIL.Image.new('RGB', size, (255, 255, 255))

	drawing = PIL.ImageDraw.Draw(image)

	pad = 10
	start_offset = pad + 1
	last_offset = pad + 1

	if ending:
		last_offset = 0

	if starting:
		start_offset = 0

	drawing.rectangle((-start_offset, 0, size[0] + last_offset, size[1]), (255, 255, 255), (0, 0, 0), width=pad)

	return image


if __name__ == '__main__':
	chars = list(
		"あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポぁぃぅぇぉゅヵヶっァィゥェォッュ、。！？1234567890＃満❤ー・…/￥」「｜＝(),.;:草[]-")
	ending_chars = list("。！？❤」｜)]")
	starting_chars = list("＃「｜([")
	emoji_chars = list("ℹ�")

	resource_path = os.path.join(os.getcwd(), "resource")
	generate_images(os.path.join(resource_path, "textures", "blocks", "japanese"), chars, ending_chars, starting_chars, emoji_chars)
	regenerate_resource_pack(resource_path, chars)

	with open('./entries.json', 'w', encoding="utf-8") as f:
		json.dump(generate_entries(chars), f, indent=4, ensure_ascii=False)

	shutil.make_archive(resource_path, format="zip", root_dir=resource_path)
