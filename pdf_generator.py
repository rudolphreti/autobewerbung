from fpdf import FPDF

line_height = 6
font_family = 'Helvetica'

class PDF(FPDF):
    def header(self):
        self.set_font(font_family, '', 12)
        self.cell(0, line_height, 'Mikolaj Kosmalski', 0, 1)
        self.cell(0, line_height, 'Pogrelzstraße 55/6/4', 0, 1)
        self.cell(0, line_height, '1220 Wien', 0, 1)
        self.set_text_color(0, 0, 255)
        self.set_font(font_family, 'U', 12)
        self.cell(0, line_height, 'mikolaj.jakub.kosmalski@gmail.com', link='mailto:mikolaj.jakub.kosmalski@gmail.com', ln=1)
        self.cell(0, line_height, 'linkedin.com/in/mikolajkosmalski', link='https://www.linkedin.com/in/mikolajkosmalski', ln=1)
        self.set_text_color(0, 0, 0)
        self.set_font(font_family, '', 12)
        self.cell(0, line_height, '0660 20 57 157', 0, 1)
