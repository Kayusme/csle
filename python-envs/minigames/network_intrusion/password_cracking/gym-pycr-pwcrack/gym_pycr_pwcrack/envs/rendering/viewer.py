"""
The viewer for rendering the gym-pycr-pwcrack environment.
"""
try:
    import pyglet
except ImportError as e:
    raise ImportError('''
    Cannot import pyglet.
    HINT: you can install pyglet directly via 'pip install pyglet'.
    But if you really just want to install all Gym dependencies and not have to think about it,
    'pip install -e .[all]' or 'pip install gym[all]' will do it.
    ''')

try:
    from pyglet.gl import *
except ImportError as e:
    raise ImportError('''
    Error occurred while running `from pyglet.gl import *`
    HINT: make sure you have OpenGL install. On Ubuntu, you can run 'apt-get install python-opengl'.
    If you're running on a server, you may need a virtual frame buffer; something like this should work:
    'xvfb-run -s \"-screen 0 1400x900x24\" python <your_script.py>'
    ''')
import numpy as np
import sys
from gym_pycr_pwcrack.envs.rendering.frames.main_frame import MainFrame

class Viewer():

    def __init__(self):
        self.isopen = True

    def start(self) -> None:
        self.mainframe = MainFrame()
        self.mainframe.on_close = self.window_closed_by_user
        self.isopen = True
        pyglet.app.run()

    def window_closed_by_user(self) -> None:
        """
        Callback when the frame is closed by the user

        :return: None
        """
        self.isopen = False
        self.mainframe.close()
        print("Window closed, exiting")
        sys.exit(0)

    def close(self) -> None:
        """
        Closes the frame

        :return: None
        """
        self.mainframe.close()

    def render_frame(self, return_rgb_array: bool = False):
        """
        Renders a frame manually.

        Using pyglet together with openAI gym means that we have to integrate OpenGL's event-loop
        with the event-loop of the RL agent and the gym framework. That's why we render things manually and dispatch
        events manually rather than just calling pyglet.app.run().

        :param return_rgb_array: if this is true it returns the RGB array for the rendered frame (for recording)
        :return: RGB array or bool
        """
        self.mainframe.clear()  # Clears the frame
        self.mainframe.switch_to()  # Make this window the current OpenGL rendering context
        self.mainframe.dispatch_events()  # Poll the OS for events and call related handlers for updating the frame
        self.mainframe.on_draw()  # Draw the frame
        if return_rgb_array:
            arr = self.extract_rgb_array()
        self.mainframe.flip()  # Swaps the OpenGL front and back buffers Updates the visible display with the back buffer
        return arr if return_rgb_array else self.isopen


    def render(self, return_rgb_array = False):
        """
        Renders a state of the env.

        :param return_rgb_array: boolean whether to return rgb array or not
        :return: RGB array or bool
        """
        arr = self.render_frame(return_rgb_array=return_rgb_array)
        return arr if return_rgb_array else self.isopen

    def extract_rgb_array(self) -> np.ndarray:
        """
        Extract RGB array from pyglet, this can then be used to record video of the rendering through gym's API

        :return: RGB Array [height, width, 3]
        """
        buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        image_data = buffer.get_image_data()
        arr = np.fromstring(image_data.get_data(), dtype=np.uint8, sep='')
        # In https://github.com/openai/gym-http-api/issues/2, we
        # discovered that someone using Xmonad on Arch was having
        # a window of size 598 x 398, though a 600 x 400 window
        # was requested. (Guess Xmonad was preserving a pixel for
        # the boundary.) So we use the buffer height/width rather
        # than the requested one.
        arr = arr.reshape(buffer.height, buffer.width, 4)
        arr = arr[::-1, :, 0:3]
        return arr

if __name__ == '__main__':
    viewer = Viewer()
    viewer.start()

# if __name__ == '__main__':
#     print("test")
#     viewer = Viewer()
#     viewer.start()
#     pyglet.clock.schedule_interval(viewer.mainframe.update, 1 / 100)
#     pyglet.app.run()