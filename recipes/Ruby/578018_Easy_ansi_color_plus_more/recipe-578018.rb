class String
  # Normal colors
  def black;       colorize(self, "\e[0m\e[30");     end
  def red;         colorize(self, "\e[0m\e[31");     end
  def green;       colorize(self, "\e[0m\e[32");     end
  def yellow;      colorize(self, "\e[0m\e[33");     end
  def blue;        colorize(self, "\e[0m\e[34");     end
  def purple;      colorize(self, "\e[0m\e[35");     end
  def cyan;        colorize(self, "\e[0m\e[36");     end
  def white;       colorize(self, "\e[0m\e[37");     end

  # Fun stuff
  def clean;       colorize(self, "\e[0");           end
  def bold;        colorize(self, "\e[1");           end
  def underline;   colorize(self, "\e[4");           end
  def blink;       colorize(self, "\e[5");           end
  def reverse;     colorize(self, "\e[7");           end
  def conceal;     colorize(self, "\e[8");           end

  # Blanking
  def clear_scr;   colorize(self, "\e[2", mode="J"); end

  # Placement
  def place(line, column)
    colorize(self, "\e[#{line};#{column}", mode='f')
  end

  def save_pos;    colorize(self, "\e[", mode='s');  end
  def return_pos;  colorize(self, "\e[", mode='u');  end

  def colorize(text, color_code, mode='m')
    "#{color_code}#{mode}#{text}\e[0m"
  end

end
