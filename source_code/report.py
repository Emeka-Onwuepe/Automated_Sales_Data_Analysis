from email import header
from reportlab.platypus import PageBreak,BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import  Paragraph   
from os import path
from source_code.converter import  df2table,landscape_template,list_to_string,fig2image
from source_code.insights.univariats_plot_funcs import feature_uniques_percentage
from source_code.sub_classes import CAT_UNIVARIATS

        
        
def create_report_pdf(df,report_heading,dataset_location,
                      pngs_location,excels_location,mapper):
    
    file_name = path.join(dataset_location,"report.pdf")

    doc = BaseDocTemplate(
            file_name,
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
    p_style.spaceBefore = 5
    p_style.spaceAfter = 5
    p_style.leading = 15
    p_style.bulletFontSize = 16
    
    cat_features = df.select_dtypes(exclude=['int64','float64','datetime64'])
    cat_features = cat_features.loc[:,cat_features.nunique() < 16]
    story = [Paragraph(report_heading, heading)]
    
    for col in cat_features.columns: 
        fig,info_df = feature_uniques_percentage(cat_features,col,pngs_location)
        story.append(fig2image(fig))
        story.append(Paragraph(" ".join(info_df),p_style))
    doc.build(story)
       