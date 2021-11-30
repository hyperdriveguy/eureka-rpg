--- /home/docs/checkouts/readthedocs.org/user_builds/arcade-library/checkouts/latest/doc/tutorials/views/01_views.py
+++ /home/docs/checkouts/readthedocs.org/user_builds/arcade-library/checkouts/latest/doc/tutorials/views/02_views.py
@@ -11,13 +11,13 @@
 SCREEN_TITLE = "Implement Views Example"
 
 
-class MyGame(arcade.Window):
+class GameView(arcade.View):
     """ Our custom Window Class"""
 
     def __init__(self):
         """ Initializer """
         # Call the parent class initializer
-        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
+        super().__init__()
 
         # Variables that will hold sprite lists
         self.player_list = None
@@ -28,7 +28,7 @@
         self.score = 0
 
         # Don't show the mouse cursor
-        self.set_mouse_visible(False)
+        self.window.set_mouse_visible(False)
 
         arcade.set_background_color(arcade.color.AMAZON)
 
@@ -100,8 +100,11 @@
 
 def main():
     """ Main function """
-    window = MyGame()
-    window.setup()
+
+    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
+    start_view = GameView()
+    window.show_view(start_view)
+    start_view.setup()
     arcade.run()