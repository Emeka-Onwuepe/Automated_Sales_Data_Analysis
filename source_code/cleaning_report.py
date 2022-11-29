from email import header
from reportlab.platypus import PageBreak,BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import  Paragraph   
from os import path
from source_code.converter import  df2table,landscape_template,list_to_string

        
        
def create_cleaning_pdf(df,error_mgs,null_report,num_ranges,null_table,
                        null_table_cleaned,name_errors,dataset_location):
    
    file_name = path.join(dataset_location,"cleaning_report.pdf")
    
    doc = BaseDocTemplate(
            "cleaning_report.pdf",
            pageTemplates=[
            landscape_template
            ]
            )
    
    styles = getSampleStyleSheet()
    p_style = styles["Normal"]
    heading = styles['Heading1']
    heading2 = styles['Heading2']
    heading.alignment = 1
    heading.spaceAfter = 10
    heading2.spaceBefore = 10
    heading2.spaceAfter = 0
    p_style.fontSize = 14
    p_style.spaceAfter = 3
    p_style.leading = 15
    p_style.bulletFontSize = 16

    
    
    
    story = [Paragraph('Cleaning Report', heading)]
    
    if error_mgs['out_of_bound']:
        string,is_plural = list_to_string(error_mgs['out_of_bound'])
        # identifier = "them" if is_plural else "it"
        content = f"we were unable to convert {string} to date datatype."
        
    story.append(Paragraph(content,p_style))
    story.append(df2table(df.head()))
    story.append(Paragraph("The image format is saved as data_head.png"))
    
    if null_table.shape[0]:
        story.append(Paragraph('Null Table', heading2))
        story.append(df2table(null_table))
        story.append(Paragraph('You can see all the affected row in the null_values excel file'))
        story.append(Paragraph('Null Cleaning', heading2))

        if null_report['dropped']:
            string,is_plural = list_to_string(null_report['dropped'])
            content = f"<bullet>&bull;</bullet>All null values in {string} were dropped."
            story.append(Paragraph(content,p_style))
        if null_report['mean']:
            string,is_plural = list_to_string(null_report['mean'])
            content = f"<bullet>&bull;</bullet>Null values in {string} were filled with their mean/average values."
            story.append(Paragraph(content,p_style))
        if null_report['ffill']:
            string,is_plural = list_to_string(null_report['ffill'])
            content = f"<bullet>&bull;</bullet>Valid value that comes before null value(s) was used to fill up the \
            null value(s) in {string}."
            story.append(Paragraph(content,p_style))
        if null_report['unknown']:
            string,is_plural = list_to_string(null_report['unknown'])
            content = f"<bullet>&bull;</bullet>All null values in {string} were filled with the word 'unknown'."
            story.append(Paragraph(content,p_style))
      
    story.append(Paragraph('Quantitative Feature Ranges', heading2))
    content = "Data points that does not fall within the min and max are generally \
    regarded as outliers and are meant to be removed but they were not removed in this analysis. \
    Each feature outlier were recored in an excel file suffix with '_outlier'"
    story.append(Paragraph(content,p_style))
    story.append(df2table(num_ranges))
    
    if name_errors:
        story.append(Paragraph(f"we noticed an irregular name patterns in :",p_style))
        for key,values in name_errors.items():
            string,is_plural = list_to_string(values)
            story.append(Paragraph(f"<b>{key} :</b> {string}",p_style))
            
    story.append(Paragraph("Cleaned Dataset Datatypes and Null Values",heading2))
    story.append(df2table(null_table_cleaned))
  
    story.append(Paragraph("Statistical Summary",heading2))
    story.append(df2table(df.describe()))
    story.append(Paragraph("The cleaned dataset is saved as clean.xlsx"))
    
    doc.build(story)
       