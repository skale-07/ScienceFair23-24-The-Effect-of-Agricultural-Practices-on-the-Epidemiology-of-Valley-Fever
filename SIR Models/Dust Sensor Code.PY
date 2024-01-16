import microbit 

def on_forever():
    print(Environment.read_dust(DigitalPin.P16, AnalogPin.P1))
    basic.pause(100)
    pass
basic.forever(on_forever)