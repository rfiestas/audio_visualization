from sense_hat import SenseHat
import alsaaudio, audioop
from time import sleep
from colour import Color

def hex_to_rgb(colors_list):
  """Return (red, green, blue) for the color given as #rrggbb list."""
  rgb_colors_list=[]
  for colors in colors_list:
    value = str(colors.hex_l)
    value = value.lstrip('#')
    lv = len(value)
    rgb_colors_list.append(tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))
  return rgb_colors_list
  

if __name__ == "__main__":

  card = 'sysdefault:CARD=Device'  # Microphone card (check with alsaaudio.cards())
  max_audioop  = 32754             # Max value

  black        = (0, 0, 0)         # Empty
  ini_gradient = Color("yellow")   # Initial color gradient
  end_gradient = Color("red")      # End color gradient
  granularity  = 512               # Granularity level
  gradient     = [black] + hex_to_rgb(list(ini_gradient.range_to(end_gradient,granularity+1)))
  power        = 32

  # Initialize SenseHat
  sense = SenseHat()

  # Initialize Alsa Audio
  inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, card)
  inp.setchannels(1)
  inp.setrate(8000)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(160)
  quit(1)

  # Clean screen
  screen = [black] * ( 8 * 8 ) 
  sense.set_pixels(screen)

  # Read From microphone
  try:
    while True:
      l,data = inp.read()
      if l:
        # Avoid exceptions, audioop.error: not a whole number of frames 
        try:
          value = audioop.max(data, 2)
        except:
          continue
        else:
          # Move from Right to Left 
          screen = screen[1:] + [black]

          # Calcule sound level
          sound_level = ((granularity * value)/max_audioop)
          for x in range(7,-1,-1):
            color = max(min(granularity,sound_level-((7-x)*power)),0)
            screen[(x*8)+7] = gradient[color]
        
          sense.set_pixels(screen)
      sleep(.001)

  except (KeyboardInterrupt, SystemExit):

    # Clean screen
    screen  = [black] *( 8 * 8 )
    sense.set_pixels(screen)
