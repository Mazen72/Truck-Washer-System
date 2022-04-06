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
presoaking_button=html.Div([dbc.Button("On/Off",size='lg',outline=False, color="primary", className="me-1", n_clicks=0,id="presoaking_button"
                            ,style=dict(fontWeight='bold',border='')
                            )],style=dict(display='inline-block'))



presoaking_buttons_div=html.Div([presoaking_button,],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))



soap_indicator=daq.Indicator(
        id='soap_indicator',
        label=dict(label='Soap',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

soap_button=html.Div([dbc.Button("On/Off",size='lg',outline=False, color="primary", className="me-1", n_clicks=0,id="soap_button"
                            ,style=dict(fontWeight='bold',border='')
                            )],style=dict(display='inline-block'))



soap_buttons_div=html.Div([soap_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))




degreaser_indicator=daq.Indicator(
        id='degreaser_indicator',
        label=dict(label='Degreaser',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

degreaser_button=html.Div([dbc.Button("On/Off",size='lg',outline=False, color="primary", className="me-1", n_clicks=0,id="degreaser_button"
                            ,style=dict(fontWeight='bold',border='')
                            )],style=dict(display='inline-block'))



degreaser_buttons_div=html.Div([degreaser_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

rinse_indicator=daq.Indicator(
        id='rinse_indicator',
        label=dict(label='Rinse',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

rinse_button=html.Div([dbc.Button("On/Off",size='lg',outline=False, color="primary", className="me-1", n_clicks=0,id="rinse_button"
                            ,style=dict(fontWeight='bold',border='')
                            )],style=dict(display='inline-block'))


rinse_buttons_div=html.Div([rinse_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

wax_indicator=daq.Indicator(
        id='wax_indicator',
        label=dict(label='Wax',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

wax_button=html.Div([dbc.Button("On/Off",size='lg',outline=False, color="primary", className="me-1", n_clicks=0,id="wax_button"
                            ,style=dict(fontWeight='bold',border='')
                            )],style=dict(display='inline-block'))


wax_buttons_div=html.Div([wax_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

pressure_washer_indicator=daq.Indicator(
        id='pressure_washer_indicator',
        label=dict(label='Pressure Washer',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

pressure_washer_button=html.Div([dbc.Button("On/Off",size='lg',outline=False, color="primary", className="me-1", n_clicks=0,id="pressure_washer_button"
                            ,style=dict(fontWeight='bold',border='')
                            )],style=dict(display='inline-block'))


pressure_washer_buttons_div=html.Div([pressure_washer_button],
                                style=dict(width='100%',
                     display= 'flex', alignItems= 'center', justifyContent= 'center'))

heater_indicator=daq.Indicator(
        id='heater_indicator',
        label=dict(label='Heater',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')),
    color='red',value=True,size=indicator_size
    )

heater_button=html.Div([dbc.Button("On/Off",size='lg',outline=False, color="primary", className="me-1", n_clicks=0,id="heater_button"
                            ,style=dict(fontWeight='bold',border='')
                            )],style=dict(display='inline-block'))


heater_buttons_div=html.Div([heater_button],
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


power_button_theme = {
    'dark': True,
    'detail': 'darkgrey',
    'primary': 'darkgrey',
    'secondary': 'darkgrey'
}


power_button= daq.PowerButton(on=False,color=on,className='dark-theme-control',size=100,id='power_button',
                             label=dict(label='Pressure Washer',style=dict(color='white',fontSize=header_font_size,fontWeight='bold')))



power_button_div=html.Div(id='power_button_div', children=[
    daq.DarkThemeProvider(theme=power_button_theme, children=power_button)],
                          style=dict(width='100%',display= 'flex', alignItems= 'center', justifyContent= 'center')
                          )

app.layout=html.Div([ dbc.Row([db_header_text],style=dict(backgroundColor='#20374c') ),html.Br(),
       dbc.Row([

           dbc.Col([dbc.Card(dbc.CardBody(
        [html.Div([presoaking_indicator ,html.Br(),presoaking_buttons_div,html.Br()

                   ], style=dict(height=''))])
        , style=dict(backgroundColor='#20374c')), html.Br()
    ], xl=dict(size=2,offset=1),lg=dict(size=3,offset=0),
                     md=dict(size=4,offset=0),sm=dict(size=6,offset=0),xs=dict(size=6,offset=0)),

                      dbc.Col([dbc.Card(dbc.CardBody(
                          [html.Div([soap_indicator, html.Br(),soap_buttons_div,html.Br()

                                     ], style=dict(height=''))])
                          , style=dict(backgroundColor='#20374c')), html.Br()
                      ], xl=dict(size=2, offset=0), lg=dict(size=3, offset=0),
                          md=dict(size=4, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0)),

           dbc.Col([dbc.Card(dbc.CardBody(
               [html.Div([degreaser_indicator, html.Br(), degreaser_buttons_div,html.Br()

                          ], style=dict(height=''))])
               , style=dict(backgroundColor='#20374c')), html.Br()
           ], xl=dict(size=2, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=4, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0)),

           dbc.Col([dbc.Card(dbc.CardBody(
               [html.Div([rinse_indicator, html.Br(), rinse_buttons_div,html.Br()

                          ], style=dict(height=''))])
               , style=dict(backgroundColor='#20374c')), html.Br()
           ], xl=dict(size=2, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=4, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0)) ,

           dbc.Col([dbc.Card(dbc.CardBody(
               [html.Div([wax_indicator, html.Br(), wax_buttons_div, html.Br()

                          ], style=dict(height=''))])
               , style=dict(backgroundColor='#20374c')), html.Br()
           ], xl=dict(size=2, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=4, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0)),

           dbc.Col([dbc.Card(dbc.CardBody(
               [html.Div([power_button_div,html.Br()

                          ], style=dict(height=''))])
               , style=dict(backgroundColor='#20374c')), html.Br()
           ], xl=dict(size=2, offset=1), lg=dict(size=3, offset=0),
               md=dict(size=4, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0)) ,

           dbc.Col([dbc.Card(dbc.CardBody(
               [html.Div([heater_indicator, html.Br(), heater_buttons_div, html.Br()

                          ], style=dict())])
               , style=dict(backgroundColor='#20374c'),className='mycard'), html.Br()
           ], xl=dict(size=2, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=4, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0),style=dict()
           ),

           dbc.Col([
               html.Div([html.Br(),cycle_timer_div

                          ], style=dict())
              , html.Br()
           ], xl=dict(size=2, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=4, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0),style=dict()
           )
         ,

           dbc.Col([
               html.Div([html.Br(), emergency_stop_div

                         ], style=dict())
               , html.Br()
           ], xl=dict(size=2, offset=0), lg=dict(size=3, offset=0),
               md=dict(size=4, offset=0), sm=dict(size=6, offset=0), xs=dict(size=6, offset=0),
               style=dict()
           ),

           dbc.Col([
               html.Div([html.Br(), logo_img_div

                         ], style=dict())
               , html.Br()
           ], xl=dict(size=2, offset=5), lg=dict(size=3, offset=0),
               md=dict(size=4, offset=4), sm=dict(size=6, offset=3), xs=dict(size=6, offset=3),
               style=dict()
           )
            ,timer_update , html.Br(),




])

       ])

@app.callback([Output('presoaking_indicator','color'),Output('soap_indicator','color'),
               Output('degreaser_indicator','color'),Output('rinse_indicator','color'),
               Output('wax_indicator','color'),Output('power_button','on'),Output('heater_indicator','color')
               ],
              [Input('presoaking_button','n_clicks'),Input('soap_button','n_clicks'),
               Input('degreaser_button','n_clicks'),Input('rinse_button','n_clicks'),Input('wax_button','n_clicks'),
                Input('power_button','on'),Input('heater_button','n_clicks'),Input('emergency_stop','n_clicks')
               ],
               [State('presoaking_indicator','color'),State('soap_indicator','color'),
               State('degreaser_indicator','color'),State('rinse_indicator','color'),State('wax_indicator','color'),
               State('power_button','on'),State('heater_indicator','color')

               ],prevent_initial_call=True)
def cycle_control(presoaking_button,soap_button,degreaser_button,
                  rinse_button,wax_button,pressure_washer_button,heater_button,
                  emergency_stop,presoaking_state,soap_state,degreaser_state,rinse_state,wax_state,pressure_washer_state,heater_state
                  ):
    global idle_state ,washing_state ,system_state ,start_time ,seconds
    ctx = dash.callback_context
    button_pressed = ctx.triggered[0]['prop_id'].split('.')[0]

    if system_state==idle_state:
        if button_pressed=='power_button':
            if pressure_washer_state==True:
                system_state=washing_state
                start_time=time.time()
                # pressure_washer pin on
                return (dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,True,dash.no_update)
            else:
                raise PreventUpdate

        else:
            raise PreventUpdate



    elif system_state==washing_state:

        if  button_pressed=='emergency_stop':
            system_state=finished_washing_state
            # all pins off
            return (off,off,off,off,off,False,off)

        elif button_pressed=='power_button':
            if pressure_washer_state == False :
                system_state=finished_washing_state
                # all pins off
                return (off,off,off,off,off,False,off)

        elif button_pressed=='presoaking_button':

            if presoaking_state==on:
                # presoaking pin off
                return (off, dash.no_update, dash.no_update, dash.no_update,dash.no_update, dash.no_update, dash.no_update)

            elif presoaking_state ==off:
                # presoaking pin on and the other 3 pins on top off
                return (on, off, off, off,off, dash.no_update, dash.no_update)


        elif button_pressed == 'soap_button':

            if soap_state==on:
                # soap pin off
                return (dash.no_update, off, dash.no_update, dash.no_update, dash.no_update,dash.no_update, dash.no_update)

            elif soap_state==off:
                # soap pin on and the other 3 pins on top off
                return (off, on, off, off, off,dash.no_update, dash.no_update)


        elif button_pressed == 'degreaser_button':

            if degreaser_state == on:
                # degreaser pin off
                return (dash.no_update, dash.no_update, off, dash.no_update,dash.no_update, dash.no_update, dash.no_update)

            elif degreaser_state == off:
                # degreaser pin on and the other 3 pins on top off
                return (off, off, on, off,off, dash.no_update, dash.no_update)



        elif button_pressed == 'rinse_button':

            if rinse_state == on:
                # rinse pin off
                return (dash.no_update, dash.no_update, dash.no_update, off, dash.no_update,dash.no_update, dash.no_update)

            elif rinse_state == off:
                # rinse pin on and the other 3 pins on top off
                return (off, off, off, on,off, dash.no_update, dash.no_update)

        elif button_pressed == 'wax_button':

            if wax_state == on:
                # wax pin off
                return (dash.no_update, dash.no_update, dash.no_update, dash.no_update,off, dash.no_update, dash.no_update)

            elif wax_state == off:
                # wax pin on and the other 3 pins on top off
                return (off, off, off, off,on, dash.no_update, dash.no_update)

        elif button_pressed == 'heater_button':

            if heater_state == on:
                # heater pin off
                return (dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, dash.no_update, off)

            elif heater_state == off:
                # heater pin on
                return (dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, dash.no_update, on)

        else:
            raise PreventUpdate

    elif system_state==finished_washing_state:
        if button_pressed=='power_button':
            system_state=washing_state
            start_time=time.time()
            # pressure_washer pin on
            return (dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,True,dash.no_update)
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
    app.run_server(host='0.0.0.0',port=8055,debug=True,dev_tools_silence_routes_logging=True)










