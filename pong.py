from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from random import randint

class PongPaddle(Widget):

   score = NumericProperty(0)

   def bounce_ball(self, ball):
      if self.collide_widget(ball):
         vx, vy = ball.velocity
         offset = (ball.center_y - self.center_y) / (self.height / 2)
         bounced = Vector(-1 * vx, vy)
         vel = bounced * 1.1
         ball.velocity = vel.x, vel.y + offset

class PongGame(Widget):
   ball = ObjectProperty(None)
   player1 = ObjectProperty(None)
   player2 = ObjectProperty(None)

   def serve_ball(self, vel=(4, 0)):
      self.ball.center = self.center
      self.ball.velocity = vel


   def update(self, dt):
      self.ball.move()

       # Bounce off top and bottom
      if(self.ball.y < 0) or (self.ball.top > self.height):
        self.ball.vel_y *= -1
    
       # Bounce off paddles
      self.player1.bounce_ball(self.ball)
      self.player2.bounce_ball(self.ball)

      # went of to a side to score point?
      if self.ball.x < self.x:
         self.player2.score += 1
         self.serve_ball(vel=(4, 0))
      if self.ball.x > self.width:
         self.player1.score += 1
         self.serve_ball(vel=(-4, 0))


   def on_touch_move(self, touch):
      if touch.x < self.width / 3:
         self.player1.center_y = touch.y
      if touch.x > self.width - self.width - 3:
         self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


class PongBall(Widget):
	vel_x = NumericProperty(0)
	vel_y = NumericProperty(0)
	velocity = ReferenceListProperty(vel_x, vel_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


if __name__ == '__main__':
    PongApp().run()