import time
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State,MATCH,ALL
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask
from dash_extensions.snippets import send_data_frame
from dash_extensions import Download
from dash.exceptions import PreventUpdate
from collections import OrderedDict
import dash_daq as daq

server = Flask(__name__)

app = dash.Dash(
    __name__,server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0, shrink-to-fit=no'
        }
    ] ,
)

app.config.suppress_callback_exceptions = True

text_font_size='1.6vh'
navbar_font_size='2vh'
header_font_size='2.2vh'
indicator_size=40

idle_state='idle'
washing_state='washing'
finished_washing_state='finished_washing'
system_state=idle_state
start_time=0
seconds=0
on='#39FF14'
off='red'

encoded = base64.b64encode(open('demo.jpg', 'rb').read())

logo_img=html.Img(src='data:image/jpg;base64,{}'.format(encoded.decode()), id='logo_img', height='150vh',width='200vh',
                  style=dict(marginLeft='1vh'))
logo_img_div=html.Div(logo_img,style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))
# setting the size and spacing of logo_img using dash bootstrap
# more info on dash bootstrap layout : https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
db_logo_img=dbc.Col([ logo_img] ,
        xs=dict(size=2,offset=0), sm=dict(size=2,offset=0),
        md=dict(size=2,offset=0), lg=dict(size=3,offset=0), xl=dict(size=3,offset=0))

header_text=html.Div('Truck Pressure Washer System',style=dict(color='white',
                     fontWeight='bold',fontSize='2.8vh',marginTop='1vh',marginLeft='',width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))




# setting the size and spacing of header_text using dash bootstrap
db_header_text=  dbc.Col([ header_text] ,
        xs=dict(size=10,offset=1), sm=dict(size=10,offset=1),
        md=dict(size=8,offset=2), lg=dict(size=6,offset=3), xl=dict(size=6,offset=3))

presoaking_text = html.Div(html.H1('Presoaking',className='card-header',
                                style=dict(fontWeight='bold', color='white',
                                           marginTop='')),
                        style=dict(display='inline-block', marginLeft='', textAlign="center"))

#        label=dict(label='PreSoaking',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),

presoaking_indicator=html.Div(daq.Indicator(className='indicator',
        id='presoaking_indicator',
label=dict(label='PreSoaking',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )  , style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center')
                              )

#style={'font-size': '12px', 'width': '140px', 'display': 'inline-block',
# 'margin-bottom': '10px', 'margin-right': '5px', 'height':'37px', 'verticalAlign': 'top'}
presoaking_on_button=html.Div([dbc.Button("On/Off",size='lg',outline=False, color="primary", className="me-1", n_clicks=0,id="presoaking_on_button"
                            ,style=dict(fontWeight='bold',border='')
                            )],style=dict(display='inline-block'))

presoaking_off_button=html.Div([dbc.Button("Turn Off",size='lg',outline=True, color="danger", className="me-1",id="presoaking_off_button"
                            ,style=dict(fontWeight='bold',border='1px solid red')
                            )],style=dict(display='inline-block',marginLeft='1.5vh'))

presoaking_buttons_div=html.Div([presoaking_on_button,presoaking_off_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))





soap_indicator=daq.Indicator(
        id='soap_indicator',
        label=dict(label='Soap',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

soap_on_button=html.Div([dbc.Button("Turn On",size='lg',outline=True, color="success", className="me-1", n_clicks=0,id="soap_on_button"
                            ,style=dict(fontWeight='bold',border='1px solid #39FF14')
                            )],style=dict(display='inline-block'))

soap_off_button=html.Div([dbc.Button("Turn Off", size='lg', outline=True, color="danger", className="me-1", n_clicks=0,id="soap_off_button"
                            ,style=dict(fontWeight='bold',border='1px solid red')
                            )],style=dict(display='inline-block',marginLeft='1.5vh'))

soap_buttons_div=html.Div([soap_on_button,soap_off_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))




degreaser_indicator=daq.Indicator(
        id='degreaser_indicator',
        label=dict(label='Degreaser',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

degreaser_on_button=html.Div([dbc.Button("Turn On",size='lg',outline=True, color="success", className="me-1", n_clicks=0,id="degreaser_on_button"
                            ,style=dict(fontWeight='bold',border='1px solid #39FF14')
                            )],style=dict(display='inline-block'))

degreaser_off_button=html.Div([dbc.Button("Turn Off",size='lg',outline=True, color="danger", className="me-1",n_clicks=0,id="degreaser_off_button"
                            ,style=dict(fontWeight='bold',border='1px solid red')
                            )],style=dict(display='inline-block',marginLeft='1.5vh'))

degreaser_buttons_div=html.Div([degreaser_on_button,degreaser_off_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

rinse_indicator=daq.Indicator(
        id='rinse_indicator',
        label=dict(label='Rinse',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

rinse_on_button=html.Div([dbc.Button("Turn On",size='lg',outline=True, color="success", className="me-1", n_clicks=0,id="rinse_on_button"
                            ,style=dict(fontWeight='bold',border='1px solid #39FF14')
                            )],style=dict(display='inline-block'))

rinse_off_button=html.Div([dbc.Button("Turn Off",size='lg',outline=True, color="danger", className="me-1",n_clicks=0,id="rinse_off_button"
                            ,style=dict(fontWeight='bold',border='1px solid red')
                            )],style=dict(display='inline-block',marginLeft='1.5vh'))

rinse_buttons_div=html.Div([rinse_on_button,rinse_off_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

pressure_washer_indicator=daq.Indicator(
        id='pressure_washer_indicator',
        label=dict(label='Pressure Washer',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

pressure_washer_on_button=html.Div([dbc.Button("Turn On",size='lg',outline=True, color="success", className="me-1", n_clicks=0,id="pressure_washer_on_button"
                            ,style=dict(fontWeight='bold',border='1px solid #39FF14')
                            )],style=dict(display='inline-block'))

pressure_washer_off_button=html.Div([dbc.Button("Turn Off",size='lg',outline=True, color="danger", className="me-1",n_clicks=0,id="pressure_washer_off_button"
                            ,style=dict(fontWeight='bold',border='1px solid red')
                            )],style=dict(display='inline-block',marginLeft='1.5vh'))

pressure_washer_buttons_div=html.Div([pressure_washer_on_button,pressure_washer_off_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

heater_indicator=daq.Indicator(
        id='heater_indicator',
        label=dict(label='Heater',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

heater_on_button=html.Div([dbc.Button("Turn On",size='lg',outline=True, color="success", className="me-1", n_clicks=0,id="heater_on_button"
                            ,style=dict(fontWeight='bold',border='1px solid #39FF14')
                            )],style=dict(display='inline-block'))

heater_off_button=html.Div([dbc.Button("Turn Off",size='lg',outline=True, color="danger", className="me-1",n_clicks=0,id="heater_off_button"
                            ,style=dict(fontWeight='bold',border='1px solid red')
                            )],style=dict(display='inline-block',marginLeft='1.5vh'))

heater_buttons_div=html.Div([heater_on_button,heater_off_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))


cycle_timer=daq.LEDDisplay(
    id='cycle_timer',
    label=dict(label="Cycle Timer",style=dict(color='white',fontWeight='bold',fontSize=header_font_size)),
    value=0 , size=60 , color='#42C4F7',backgroundColor="#0f2937"
#42C4F7"
#0f2937 #FF5E5E
)
cycle_timer_div=html.Div(cycle_timer,style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

timer_update=dcc.Interval(id="timer_update",interval=1000,n_intervals=0)

emergency_stop=dbc.Button("Emergency Stop",size='lg', color="danger",n_clicks=0,id="emergency_stop",className='stop'
                            ,style=dict(fontWeight='bold',border='1px solid red')
                            )
emergency_stop_div=html.Div(emergency_stop,style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

app.layout=html.Div([ dbc.Row([db_header_text],style=dict(backgroundColor='#20374c') ),html.Br(),
       dbc.Row([

           dbc.Col([dbc.Card(dbc.CardBody(
        [html.Div([presoaking_indicator ,html.Br(),presoaking_buttons_div,html.Br()

                   ], style=dict(height=''))])
        , style=dict(backgroundColor='#20374c')), html.Br()
    ], xl=dict(size=3,offset=0),lg=dict(size=3,offset=0),
                     md=dict(size=5,offset=1),sm=dict(size=6,offset=0),xs=dict(size=6,offset=0)),

                      dbc.Col([dbc.Card(dbc.CardBody(
                          [html.Div([soap_indicator, html.Br(),soap_buttons_div,html.Br()

                                     ], style=dict(height=''))])
                          , style=dict(backgroundColor='#20374c')), html.Br()
                      ], xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
                          md=dict(size=5, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0)),

           dbc.Col([dbc.Card(dbc.CardBody(
               [html.Div([degreaser_indicator, html.Br(), degreaser_buttons_div,html.Br()

                          ], style=dict(height=''))])
               , style=dict(backgroundColor='#20374c')), html.Br()
           ], xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=5, offset=1), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0)),

           dbc.Col([dbc.Card(dbc.CardBody(
               [html.Div([rinse_indicator, html.Br(), rinse_buttons_div,html.Br()

                          ], style=dict(height=''))])
               , style=dict(backgroundColor='#20374c')), html.Br()
           ], xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=5, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0)) ,

           dbc.Col([dbc.Card(dbc.CardBody(
               [html.Div([pressure_washer_indicator, html.Br(), pressure_washer_buttons_div,html.Br()

                          ], style=dict(height=''))])
               , style=dict(backgroundColor='#20374c')), html.Br()
           ], xl=dict(size=3, offset=2), lg=dict(size=3, offset=2),
               md=dict(size=5, offset=1), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0)) ,

           dbc.Col([dbc.Card(dbc.CardBody(
               [html.Div([heater_indicator, html.Br(), heater_buttons_div, html.Br()

                          ], style=dict())])
               , style=dict(backgroundColor='#20374c')), html.Br()
           ], xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=5, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0),style=dict(display='inline-block')
           ),

           dbc.Col([
               html.Div([html.Br(),cycle_timer_div

                          ], style=dict())
              , html.Br()
           ], xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=5, offset=1), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0),style=dict(display='inline-block',verticalAlign='middle')
           )
         ,

           dbc.Col([
               html.Div([html.Br(), emergency_stop_div

                         ], style=dict())
               , html.Br()
           ], xl=dict(size=3, offset=3), lg=dict(size=3, offset=3),
               md=dict(size=5, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0),
               style=dict(display='inline-block', verticalAlign='middle')
           ),

           dbc.Col([
               html.Div([html.Br(),html.Br(), logo_img_div

                         ], style=dict())
               , html.Br()
           ], xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=5, offset=1), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0),
               style=dict(display='inline-block', verticalAlign='middle')
           )
            ,timer_update

       ])
       ])


@app.callback([Output('presoaking_indicator','color'),Output('soap_indicator','color'),
               Output('degreaser_indicator','color'),Output('rinse_indicator','color'),
               Output('pressure_washer_indicator','color'),Output('heater_indicator','color')
               ],
              [Input('presoaking_on_button','n_clicks'),Input('presoaking_off_button','n_clicks'),
               Input('soap_on_button','n_clicks'),Input('soap_off_button','n_clicks'),
               Input('degreaser_on_button','n_clicks'),Input('degreaser_off_button','n_clicks'),
                Input('rinse_on_button','n_clicks'),Input('rinse_off_button','n_clicks'),
                Input('pressure_washer_on_button','n_clicks'),Input('pressure_washer_off_button','n_clicks'),
                Input('heater_on_button','n_clicks'),Input('heater_off_button','n_clicks'),Input('emergency_stop','n_clicks')

               ]
              ,prevent_initial_call=True)
def cycle_control(presoaking_on_button,presoaking_off_button,soap_on_button,soap_off_button,degreaser_on_button,
                  degreaser_off_button,rinse_on_button,rinse_off_button,pressure_washer_on_button,pressure_washer_off_button,
                  heater_on_button,heater_off_button,emergency_stop
                  ):
    global idle_state ,washing_state ,system_state ,start_time ,seconds
    ctx = dash.callback_context
    button_pressed = ctx.triggered[0]['prop_id'].split('.')[0]

    if system_state==idle_state:
        if button_pressed=='pressure_washer_on_button':
            system_state=washing_state
            start_time=time.time()
            # pressure_washer pin on
            return (dash.no_update,dash.no_update,dash.no_update,dash.no_update,on,dash.no_update)
        else:
            raise PreventUpdate



    elif system_state==washing_state:

        if button_pressed=='pressure_washer_off_button' or button_pressed=='emergency_stop':
            system_state=finished_washing_state
            # all pins off
            return (off,off,off,off,off,off)

        elif button_pressed=='presoaking_off_button':
            # presoaking pin off
            return (off,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update)

        elif button_pressed=='presoaking_on_button':
            # presoaking pin on and the other 3 pins on top off
            return (on,off,off,off,dash.no_update,dash.no_update)

        elif button_pressed == 'soap_off_button':
            # soap pin off
            return (dash.no_update,off,dash.no_update,dash.no_update,dash.no_update,dash.no_update)

        elif button_pressed == 'soap_on_button':
            # soap pin on and the other 3 pins on top off
            return (off,on,off,off,dash.no_update,dash.no_update)

        elif button_pressed == 'degreaser_off_button':
            # degreaser pin off
            return (dash.no_update,dash.no_update,off,dash.no_update,dash.no_update,dash.no_update)

        elif button_pressed == 'degreaser_on_button':
            # degreaser pin on and the other 3 pins on top off
            return (off,off,on,off,dash.no_update,dash.no_update)

        elif button_pressed == 'rinse_off_button':
            # rinse pin off
            return (dash.no_update,dash.no_update,dash.no_update,off,dash.no_update,dash.no_update)

        elif button_pressed == 'rinse_on_button':
            # rinse pin on and the other 3 pins on top off
            return (off,off,off,on,dash.no_update,dash.no_update)

        elif button_pressed == 'heater_off_button':
            # heater pin off
            return (dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,off)

        elif button_pressed == 'heater_on_button':
            # heater pin on
            return (dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,on)
        elif button_pressed == 'pressure_washer_on_button':
            # pressure washer pin on
            return (on,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update)


        else:
            raise PreventUpdate

    elif system_state==finished_washing_state:
        if button_pressed=='pressure_washer_on_button':
            system_state=washing_state
            start_time=time.time()
            # pressure_washer pin on
            return (dash.no_update,dash.no_update,dash.no_update,dash.no_update,on,dash.no_update)
        else:
            raise PreventUpdate


@app.callback(Output('cycle_timer','value'),
              Input('timer_update','n_intervals'))
def update_timer(time_update):
    if system_state== washing_state:
        seconds = int(time.time() - start_time)
        return seconds
    else:
        return 0
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8055,debug=False,dev_tools_silence_routes_logging=True)










