from os import path
from pandas import ExcelWriter
from reportlab.platypus import Frame
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import PageTemplate
from io import BytesIO
from reportlab.platypus import Image
from reportlab.lib.units import inch
from reportlab.platypus import Table, Paragraph
from reportlab.lib import colors


def convert_to_excel(data,dataset_location,file_name):
    df_file = path.join(dataset_location,f"{file_name}.xlsx")
    writer = ExcelWriter(df_file,engine="xlsxwriter")
    data.to_excel(writer,index=False)
    writer.save()
    writer.close()
   
      
padding = dict(
  leftPadding=10, 
  rightPadding=10,
  topPadding=10,
  bottomPadding=10)

landscape_frame = Frame(0, 0, *landscape(A4), **padding)

def on_page(canvas, doc, pagesize=A4):
    # canvas.setFont('Times-Roman',14)
    page_num = canvas.getPageNumber()
    canvas.drawCentredString(pagesize[0]/2, 50, str(page_num))

def on_page_landscape(canvas, doc):
  return on_page(canvas, doc, pagesize=landscape(A4))


landscape_template = PageTemplate(
  id='landscape', 
  frames=landscape_frame, 
  onPage=on_page_landscape, 
  pagesize=landscape(A4))



def fig2image(f):
    buf = BytesIO()
    f.savefig(buf, format='png', dpi=300)
    
    buf.seek(0)
    x, y = f.get_size_inches()
    return Image(buf, x * inch, y * inch)
 
from reportlab.lib.styles import getSampleStyleSheet 
styles = getSampleStyleSheet()
p_style2 = styles["Normal"]
p_style2.fontSize = 11
p_style2.alignment = 1

def df2table(df,p_style=p_style2):
    length = 9
    df = df.astype("str")
    row_len,col_len = df.shape
    colwidths=[1.2 * inch] * length
     
    
    if col_len > length:
          df = df.iloc[:,0:9]
          df['...'] = ["..."] * row_len
          colwidths.append(0.5 * inch)
    
    head = [[Paragraph(col,p_style) for col in df.columns]]
    body =  df.values.tolist()
    body_arr = []
    for arr in body:
          arr_data = [Paragraph(cell,p_style) for cell in arr]
          body_arr.append(arr_data)
    
    data = head + body_arr
   
    return Table(data,
      style=[
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('LINEBELOW',(0,0), (-1,0), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.lightgrey, colors.white])],
      hAlign = 'LEFT',colWidths=colwidths,spaceBefore=10,)
    
def list_to_string(arr):
  is_plural = True
  string = None
  length = len(arr)
  if length < 2:
    is_plural = False
    string = arr[0]
  elif length > 1:
        arr.insert(length-1,"and,")
        string = ', '.join(arr)
        string = string.replace(",,",'')
  return string,is_plural
    