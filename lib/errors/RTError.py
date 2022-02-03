from errors.Error import Error
from string_with_arrows import string_with_arrows

class RTError(Error):
	def __init__(self, pos_start, pos_end, details, ctx):
		super().__init__(pos_start, pos_end, 'RTError', details)
		self.ctx = ctx

	def as_string(self):
		result  = self.generate_traceback()
		result += f"{self.name}: {self.details}\n\n"
		result += string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.ctx

		while ctx:
			result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result