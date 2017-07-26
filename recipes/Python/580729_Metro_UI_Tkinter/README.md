## Metro UI TkinterOriginally published: 2016-12-10 02:40:05 
Last updated: 2017-04-13 23:48:27 
Author: Miguel Martínez López 
 
I provide here some widgets with windows metro style: QuoteFrame, Metro_LabelFrame. Metro_Button, Container, Label_Container, Pagination.\n\nIt's possible to provide an ID to the widgets, and then find the widget using the function *get_widget_by_ID*. \n\nMany widgets inherits the background from its container if this value is not provided.\n\nTo inherit the background makes easy to create colored areas, instead of setting the same background color to every widget of the area.