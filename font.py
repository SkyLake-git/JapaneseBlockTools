import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


class FontWriter:
	font: PIL.ImageFont.FreeTypeFont

	def __init__(self, font_path: str, font_size: int):
		self.font_path = font_path

		self.font = PIL.ImageFont.truetype(font_path, font_size)

	def draw(self, image: PIL.Image, x: int, y: int, text: str):
		drawing = PIL.ImageDraw.Draw(image)

		width, height = drawing.textsize(text, font=self.font)
		position = (x - width / 2, y - height / 2 - 5)

		drawing.text(position, text, fill=(0, 0, 0), align="center", font=self.font)
