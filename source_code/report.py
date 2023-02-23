from reportlab.platypus import PageBreak,BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import  Paragraph   
from os import path
from source_code.converter import  landscape_template,fig2image,list_to_string,df2table
from source_code.insights.time_series import plot_time_series,average_sales
from source_code.insights.univariats_plot_funcs import feature_uniques_percentage,plot_graph
from source_code.insights.plot_returns import average_returns,plot_average_returns
from source_code.introduction import introduction_p1, introduction_p2, introduction_p3
from source_code.sub_classes import TIME_SEERIES_VAL,PRODUCT_VAL
from source_code.insights.interpretation import time_series_insights
from matplotlib.pylab import close
# from gc import collect
       
def create_report_pdf(df,report_heading,dataset_location,
                      pngs_location,excels_location,mapper,multiple_features):
    
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
    heading3 = styles['Heading3']
    heading.alignment = 1
    heading.spaceAfter = 10
    heading2.spaceBefore = 10
    heading2.spaceAfter = 0
    heading3.spaceBefore = 5
    p_style.fontSize = 14
    p_style.spaceBefore = 5
    p_style.spaceAfter = 5
    p_style.leading = 15
    p_style.bulletFontSize = 16


    cat_features = df.select_dtypes(exclude=['int64','float64','datetime64'])
    cat_features = cat_features.loc[:,cat_features.nunique() < 16]
    story = [Paragraph(report_heading, heading)]

    story.append(Paragraph("Introduction",heading2))
    story.append(Paragraph(introduction_p1,p_style))
    story.append(Paragraph(introduction_p2,p_style))
    story.append(Paragraph(introduction_p3,p_style))

    for col in cat_features.columns: 
        data_dic,info_df = feature_uniques_percentage(cat_features,col)
        fig = plot_graph(pngs_location=pngs_location,**data_dic)
        story.append(PageBreak())
        story.append(fig2image(fig))
        content,is_plural = list_to_string(info_df)
        story.append(Paragraph(content,p_style))
        close("all")
        del data_dic,info_df,fig
        #collect()
     
    ### plot Time Series
    for period in ["d",'m']:

        label_period = "Daily"
        if period == "m":
            label_period = "Monthly"
        
        
        for item in TIME_SEERIES_VAL:
            data_list = None
            data = None
            try:
                data_list,data = average_sales(df,mapper['sales_date'],mapper[item],mapper,period)
                pass
            except KeyError:
                continue 
           
            if data_list:
                story.append(PageBreak())
                story.append(Paragraph(f'{label_period} Sales Graphs',heading2))
                story.append(Paragraph(mapper[item],heading3))
                info_df = time_series_insights(data,period,mapper[item])
                del data
                story.append(Paragraph(info_df,p_style))
                for count,data in enumerate(data_list):
                    if count>0:
                        story.append(PageBreak())
                        story.append(Paragraph(f'{mapper[item]} continues ({label_period})',heading3))
                    fig = plot_time_series(data,mapper[item],count,pngs_location,period)
                    story.append(fig2image(fig))
                    close("all")
                    del fig
                    info_df = None
                    #collect()
                data_list = None
        # multiple keys
        for item in TIME_SEERIES_VAL:
            data_list = None
            data = None
            try:
                for item2 in multiple_features[item]:
                    try:
                        data_list,data = average_sales(df,mapper['sales_date'],mapper[item2],mapper,period)
                    except KeyError:
                        continue 
            except KeyError:
                continue
   
            if data_list:
                story.append(PageBreak())
                story.append(Paragraph(mapper[item2],heading3))
                info_df = time_series_insights(data,period,mapper[item2])
                del data
                story.append(Paragraph(info_df,p_style)) 
                for count,data in enumerate(data_list):
                    if count>0:
                        story.append(PageBreak())
                        story.append(Paragraph(f'{mapper[item2]} continues ({label_period})',heading3))
                    fig = plot_time_series(data,mapper[item2],count,pngs_location,period)
                    story.append(fig2image(fig))
                    close("all")
                    del fig
                    info_df = None
                    #collect()
                data_list = None

    ### Sales Return                         
    try:
        if df["returns(%)"].mean() > 0:
            story.append(Paragraph('Average Sales Returns Graphs',heading2))
            content = "This shows the average percentage of profits to investement on products. For Example 10% averages shows that \
                the product on average has yeilded 10% of the cost price or gross cost price as profit "
            story.append(Paragraph(content,p_style))
            
            for item in PRODUCT_VAL:
                data_list = None
                info_df = None
                try:
                    data_list,info_df = average_returns(df,mapper[item])
                except KeyError:
                    continue 
                
                if data_list:
                    story.append(PageBreak())
                    story.append(Paragraph(mapper[item],heading3))
                    story.append(Paragraph(info_df,p_style)) 
                    for count,data in enumerate(data_list):
                        if count>0:
                            story.append(PageBreak())
                            story.append(Paragraph(f'{mapper[item]} continues ({label_period})',heading3))
                        fig = plot_average_returns(data,mapper[item],count,pngs_location)
                        story.append(fig2image(fig))
                        close("all")
                        del fig
                        info_df =  None
                        #collect()
                data_list = None
            # multiple keys
            for item in PRODUCT_VAL:
                data_list = None
                info_df = None
                try:
                    for item2 in multiple_features[item]:
                        try:
                            data_list,info_df = average_returns(df,mapper[item2])
                        except KeyError:
                            continue 
                except KeyError:
                    continue
                             
                if data_list:
                    story.append(PageBreak())
                    story.append(Paragraph(mapper[item2],heading3))
                    story.append(Paragraph(info_df,p_style)) 
                    for count,data in enumerate(data_list):
                        if count>0:
                            story.append(PageBreak())
                            story.append(Paragraph(f'{mapper[item2]} continues ({label_period})',heading3))
                        fig = plot_average_returns(data,mapper[item2],count,pngs_location)
                        story.append(fig2image(fig))
                        close("all")
                        del fig
                        info_df = None
                        #collect()
                data_list = None
    except KeyError:
        pass

    doc.build(story)
       