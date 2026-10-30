"""Build the versioned SLAB brief from Markdown, with PDF content/layout checks."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
FONT_CANDIDATES = [Path('C:/Windows/Fonts/arial.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
font = next((p for p in FONT_CANDIDATES if p.exists()), None)
if font is None:
    raise RuntimeError('A Unicode font is required: Arial on Windows or DejaVu Sans on Linux.')
pdfmetrics.registerFont(TTFont('Brief', str(font)))
bold = font.with_name('arialbd.ttf' if font.name=='arial.ttf' else 'DejaVuSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('BriefBold', str(bold)))
pdfmetrics.registerFontFamily('Brief', normal='Brief', bold='BriefBold', italic='Brief', boldItalic='BriefBold')
styles=getSampleStyleSheet()
for name in ['Normal','BodyText','Heading1','Heading2','Heading3','Title']:
    styles[name].fontName='Brief'
styles['BodyText'].fontSize=8.7
styles['BodyText'].leading=12
styles['BodyText'].spaceAfter=6
styles['Heading1'].fontSize=24;styles['Heading1'].leading=29
styles['Heading2'].fontSize=16;styles['Heading2'].leading=20;styles['Heading2'].spaceAfter=12
styles['Heading3'].fontSize=11;styles['Heading3'].leading=15;styles['Heading3'].spaceBefore=10
styles.add(ParagraphStyle(name='Cell',fontName='Brief',fontSize=8,leading=11,spaceAfter=0))
styles.add(ParagraphStyle(name='CellHead',parent=styles['Cell'],fontName='BriefBold',textColor=colors.white))

def inline(text):
    text=escape(text)
    text=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',text)
    return text.replace('`','')

def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#dd6a36'))
    canvas.line(40,38,A4[0]-40,38)
    canvas.setFont('Brief',7)
    canvas.setFillColor(colors.HexColor('#555555'))
    canvas.drawString(40,25,'SLAB • Rev D • 18 September 2026 • Demonstration reference — not for manufacture')
    canvas.drawRightString(A4[0]-40,25,str(doc.page))

source=ROOT/'docs/SLAB_PRD_RevD.md'
output=ROOT/'docs/SLAB_PRD_RevD.pdf'
lines=source.read_text(encoding='utf-8').splitlines()
story=[];i=0
while i<len(lines):
    line=lines[i].strip()
    if not line:i+=1;continue
    if line=='---PAGE---':story.append(PageBreak());i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[v.strip() for v in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[-: ]+',v) for v in cells):rows.append(cells)
            i+=1
        n=len(rows[0]);width=A4[0]-80
        ratios={2:[.32,.68],3:[.27,.16,.57],4:[.31,.22,.23,.24]}.get(n,[1/n]*n)
        if n==3 and 'Bodies' in rows[0]:ratios=[.39,.12,.49]
        data=[[Paragraph(inline(c),styles['CellHead' if r==0 else 'Cell']) for c in row] for r,row in enumerate(rows)]
        table=Table(data,colWidths=[width*r for r in ratios],repeatRows=1,hAlign='LEFT')
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#263238')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f0f3f4'),colors.white]),('LINEBELOW',(0,-1),(-1,-1),.4,colors.HexColor('#cccccc'))]))
        story.extend([table,Spacer(1,9)]);continue
    if line.startswith('#'):
        level=len(line)-len(line.lstrip('#'))
        story.append(Paragraph(inline(line.lstrip('#').strip()),styles['Heading'+str(min(level,3))]));i+=1;continue
    para=[line];i+=1
    if not line.startswith('- '):
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','---PAGE---','- ')):
            para.append(lines[i].strip());i+=1
    text=' '.join(para)
    if text.startswith('- '):text='• '+text[2:]
    story.append(Paragraph(inline(text),styles['BodyText']))
doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=38,bottomMargin=52,title='SLAB Product Design Brief — Revision D',author='S. DeFibaugh',subject='Reconciled exterior CAD demonstration requirements and validation findings')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
pdf=pymupdf.open(output)
text='\n'.join(p.get_text() for p in pdf)
for required in ['Revision D','DEC-C7','TBD-19','161.1','40.96','Appendix A','289','27B']:
    assert required in text,required
assert all(len(p.get_text().strip())>100 for p in pdf),'Blank page'
# Raster contact sheet for visual review, plus individual full-resolution pages.
from PIL import Image,ImageOps,ImageDraw
out=ROOT/'.local/prd-review';out.mkdir(parents=True,exist_ok=True)
thumbs=[]
for i,p in enumerate(pdf):
    pix=p.get_pixmap()
    image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
    image.thumbnail((298,421));thumb=Image.new('RGB',(310,445),'#dddddd');thumb.paste(image,((310-image.width)//2,5));ImageDraw.Draw(thumb).text((8,428),f'Page {i+1}',fill='black');thumbs.append(thumb)
    p.get_pixmap(matrix=pymupdf.Matrix(1.4,1.4)).save(out/f'page-{i+1}.png')
cols=3;sheet=Image.new('RGB',(cols*310,((len(thumbs)+cols-1)//cols)*445),'#cccccc')
for i,im in enumerate(thumbs):sheet.paste(im,((i%cols)*310,(i//cols)*445))
sheet.save(out/'contact.png')
print({'pdf':str(output),'pages':len(pdf),'bytes':output.stat().st_size,'content_checks':'PASS','contact_sheet':str(out/'contact.png')})
