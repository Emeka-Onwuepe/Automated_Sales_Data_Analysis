from reportlab.platypus import BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import  Paragraph   
from os import path
from source_code.converter import  landscape_template,fig2image
from source_code.insights.time_series import plot_time_series,average_sales
from source_code.insights.univariats_plot_funcs import feature_uniques_percentage,plot_graph
from source_code.insights.plot_returns import average_returns,plot_average_returns
from source_code.sub_classes import TIME_SEERIES_VAL,PRODUCT_VAL
from matplotlib.pylab import close
from gc import collect

        
        
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
        data_dic,info_df = feature_uniques_percentage(cat_features,col)
        fig = plot_graph(pngs_location=pngs_location,**data_dic)
        story.append(fig2image(fig))
        story.append(Paragraph(" ".join(info_df),p_style))
        close("all")
        del data_dic,info_df,fig
        collect()
     

    ### plot Time Series
    for period in ["d",'m']:

        label_period = "Daily"
        if period == "m":
            label_period = "Monthly"
        
        
        story.append(Paragraph(f'{label_period} Sales Graphs',heading2))
        for feature in TIME_SEERIES_VAL:
            graph_list = None
            try:
                graph_list = average_sales(df,mapper['sales_date'],mapper[feature],mapper,period)
                pass
            except KeyError:
                continue 
            
            if graph_list:
                for graph in graph_list:
                    fig,info_df = plot_time_series(pngs_location=pngs_location,**graph)
                    story.append(fig2image(fig))
                    close("all")
                    del fig,info_df
                    collect()
                graph_list = None
        # multiple keys
        for feature in TIME_SEERIES_VAL:
            graph_list = None
            try:
                for feature2 in multiple_features[feature]:
                    try:
                        graph_list = average_sales(df,mapper['sales_date'],mapper[feature2],mapper,period)
                    except KeyError:
                        continue 
            except KeyError:
                continue
                
            if graph_list:
                for graph in graph_list:
                    fig,info_df = plot_time_series(pngs_location=pngs_location,**graph)
                    story.append(fig2image(fig))
                    close("all")
                    del fig,info_df
                    collect()
                graph_list = None


    ### Sales Return                         
    try:
        if df["returns(%)"].mean() > 0:
            story.append(Paragraph('Average Sales Returns Graphs',heading2))
            content = "This shows the average percentage of profits to investement on products. For Example 10% averages shows that \
                the product on average has yeilded 10% of the cost price or gross cost price as profit "
            story.append(Paragraph(content,p_style))
            
            for feature in PRODUCT_VAL:
                graph_list = None
                try:
                    graph_list = average_returns(df,mapper[feature])
                except KeyError:
                    continue 
                
                if graph_list:
                    for graph in graph_list:
                        fig,info_df = plot_average_returns(pngs_location=pngs_location,**graph)
                        story.append(fig2image(fig))
                        close("all")
                        del fig,info_df
                        collect()
                graph_list = None
            # multiple keys
            for feature in PRODUCT_VAL:
                graph_list = None
                try:
                    for feature2 in multiple_features[feature]:
                        try:
                            graph_list = average_returns(df,mapper[feature2])
                        except KeyError:
                            continue 
                except KeyError:
                    continue
                
                    
                if graph_list:
                    for graph in graph_list:
                        fig,info_df = plot_average_returns(pngs_location=pngs_location,**graph)
                        story.append(fig2image(fig))
                        close("all")
                        del fig,info_df
                        collect()
                graph_list = None
    except KeyError:
        pass

    doc.build(story)
       