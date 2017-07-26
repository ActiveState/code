#!/usr/bin/env ruby

require 'Qt4'

class Clock < Qt::Widget
   def initialize(parent=nil)
      super(parent)
      #timer
      timer = Qt::Timer.new(self)
      timer.connect(SIGNAL :timeout) {self.update}
      timer.start(1000)
      #window
      setWindowIcon(Qt::Icon.new('Default.png'))
      setWindowTitle('Clock')
      resize(200, 200)
      #hour pointer
      @hPointer = Qt::Polygon.new([
         Qt::Point.new(6, 7),
         Qt::Point.new(-6, 7),
         Qt::Point.new(0, -50)
      ])
      #minute pointer
      @mPointer = Qt::Polygon.new([
         Qt::Point.new(6, 7),
         Qt::Point.new(-6, 7),
         Qt::Point.new(0, -70)
      ])
      #second pointer
      @sPointer = Qt::Polygon.new([
         Qt::Point.new(1, 1),
         Qt::Point.new(-1, 1),
         Qt::Point.new(0, -90)
      ])
      #colors
      @bColor = Qt::Color.new('#0000aa') #hours and minutes
      @sColor = Qt::Color.new('#aa0087')

      def paintEvent(event)
         painter = Qt::Painter.new(self)
         drawFace(painter)
         painter.end
      end

      def drawFace(painter)
         rec = [self.width, self.height].min
         tik = Qt::Time::currentTime
         painter.setRenderHint(Qt::Painter::Antialiasing)
         painter.translate(self.width / 2, self.height / 2)
         painter.scale(rec / 200, rec / 200)
         painter.setPen(Qt::NoPen)

         drawPointer(painter, @bColor, (30 * (tik.hour + tik.minute / 60)), @hPointer)
         drawPointer(painter, @bColor, (6 * (tik.minute + tik.second / 60)), @mPointer)
         drawPointer(painter, @sColor, (6 * tik.second), @sPointer)

         painter.setPen(Qt::Pen.new(@bColor))
         for i in 0..59
            if (i % 5) != 6
               painter.drawLine(87, 0, 97, 0)
            end
            painter.rotate(6)
         end
      end

      def drawPointer(painter, color, rotation, pointer)
         painter.setBrush(Qt::Brush.new(color))
         painter.save
         painter.rotate(rotation)
         painter.drawConvexPolygon(pointer)
         painter.restore
      end
   end
end

app = Qt::Application.new(ARGV)
win = Clock.new
win.show
app.exec
